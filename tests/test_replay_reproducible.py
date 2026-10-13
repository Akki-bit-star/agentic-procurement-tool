"""The committed demo must be reproducible offline from the committed cache (data/cache), byte-for-byte on the decisions.

If you change scoring/matching code, regenerate the demo:
    python -m procure run demo/input.json --out demo/output --llm none        (cache hits are free)
"""
import json
from pathlib import Path

import pytest

from procure.config import load_config
from procure.models import ProcurementRequest
from procure.pipeline import run_pipeline

ROOT = Path(__file__).resolve().parent.parent
COMMITTED = ROOT / "demo" / "output" / "result.json"

pytestmark = pytest.mark.skipif(not COMMITTED.exists() or not (ROOT / "data" / "cache").exists(),
                                reason="demo output / cache not present")


def decisions(r: dict) -> dict:
    return {(v["id"], mid): (v["tier"], v["name"], a["match_class"], a["confidence"], a["score"], a["rank"], a["shortlisted"])
            for v in r["vendors"] for mid, a in v["assessments"].items()}


def test_replay_reproduces_committed_demo_with_no_network_and_no_keys(monkeypatch):
    for k in ("SERPER_API_KEY", "ANTHROPIC_API_KEY"):
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setattr("procure.config.load_dotenv_file", lambda path=None: None)   # prove no secrets are needed
    cfg = load_config(overrides={"llm.provider": "none"})
    req = ProcurementRequest(**json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8")))
    res = run_pipeline(req, cfg, cache_dir=ROOT / "data" / "cache", cache_mode="replay")
    committed = json.loads(COMMITTED.read_text(encoding="utf-8"))
    assert res.meta["budget_used"]["search"] == "0/60"
    assert decisions(json.loads(res.model_dump_json())) == decisions(committed)
    assert sorted(e.id for e in res.evidence) == sorted(e["id"] for e in committed["evidence"])
