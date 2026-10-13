"""Agent mode with a scripted fake model: the REAL loop, tools, evidence gate and pipeline; only the model is faked."""
import json
from pathlib import Path

import pytest

from procure.agents.research import compact
from procure.config import load_config
from procure.fetch import Fetcher
from procure.llm import ChatResult, ToolCall
from procure.models import Page, ProcurementRequest, Tier
from procure.pipeline import run_pipeline
from procure.providers import search as search_mod

from tests.test_pipeline_offline import GANESH_URL, PAGES, StubProvider

ROOT = Path(__file__).resolve().parent.parent
REAL_QUOTE = "Size 50 NB | 60.3 mm OD | Thickness 5.5 mm | Heavy class"
FAKE_QUOTE = "BIS licence CM/L-9999999 valid until 2031"


def n_tool_msgs(messages):
    return sum(1 for m in messages if m["role"] == "tool")


class ScriptedChat:
    """Chooses the next tool call from how many tool results it has already seen (independent of compaction)."""
    available = True

    def __init__(self, policy):
        self.policy, self.seen, self.calls = policy, [], 0

    def chat(self, *, tier, messages, tools, max_tokens=1500, label=""):
        self.calls += 1
        self.seen.append(messages)
        name, args = self.policy(n_tool_msgs(messages))
        return ChatResult(None, [ToolCall(id=f"c{self.calls}", name=name, arguments=args)], "tool_calls")


def good_policy(step):
    return [
        ("search_web", {"query": "ERW pipe 50 NB IS 1239 Ahmedabad", "scope": "india"}),
        ("read_page", {"url": GANESH_URL}),
        ("record_evidence", {"vendor_id": "ganeshtubes.example", "url": GANESH_URL, "claim_type": "wall", "quote": REAL_QUOTE}),
        ("record_evidence", {"vendor_id": "ganeshtubes.example", "url": GANESH_URL, "claim_type": "certification", "quote": FAKE_QUOTE}),
        ("finish", {"summary": "done"}),
    ][min(step, 4)]


@pytest.fixture()
def env(tmp_path, monkeypatch):
    monkeypatch.setitem(search_mod.PROVIDERS, "serper", lambda: StubProvider())
    monkeypatch.setattr(Fetcher, "_fetch_network",
                        lambda self, url: Page(url=url, ok=True, status=200, text=PAGES[url]) if url in PAGES else Page(url=url, ok=False, error="HTTP 404"))
    monkeypatch.setattr(Fetcher, "_polite_wait", lambda self, host: None)
    req = ProcurementRequest(**json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8")))

    def run(policy, **ov):
        model = ScriptedChat(policy)
        monkeypatch.setattr("procure.pipeline.build_llm", lambda ctx, cache: model)
        cfg = load_config(overrides={"llm.provider": "openai_compat", "llm.agent.enabled": True, **ov})
        return run_pipeline(req, cfg, cache_dir=tmp_path / "c", cache_mode="auto"), model

    return run


def vendor(res, needle):
    return next(v for v in res.vendors if needle.lower() in v.name.lower() or needle in v.id)


def test_model_directs_the_loop_and_the_gate_stays_in_charge(env):
    res, model = env(good_policy)
    assert "+agent" in res.meta["llm_mode"]
    # the real quote is in the ledger, attributed to the vendor, recorded by the agent
    g = vendor(res, "ganeshtubes")
    quotes = [e.quote for e in res.evidence if e.vendor_id == g.id and "agent-recorded" in e.claim]
    assert any(REAL_QUOTE.split("|")[0].strip() in q for q in quotes)
    # the fabricated certification quote never entered the ledger ...
    assert not any("CM/L-9999999" in e.quote for e in res.evidence)
    assert any("CM/L-9999999" in d["quote"] for d in res.dropped_claims)
    # ... and the model was TOLD it was rejected (feedback loop), in the very next tool result it saw
    last = model.seen[-1]
    assert any(m["role"] == "tool" and '"accepted": false' in m["content"] for m in last)
    # per-agent summaries are reported
    assert len(res.discovery) == 9 and all(d["finished_by"] == "model" for d in res.discovery)
    assert all(d["evidence_rejected"] == 1 for d in res.discovery)
    assert sum(d["evidence_accepted"] for d in res.discovery) >= 1     # later agents re-recording the same passage merge, not double-count


def test_agent_evidence_drives_the_same_deterministic_assessment(env):
    res, _ = env(good_policy)
    g = vendor(res, "ganeshtubes")
    assert g.tier == Tier.AHMEDABAD                         # address came from the (rules) backstop on Ganesh's pages / maps
    a = g.assessments["M-01"]
    assert a.match_class.value in ("EXACT", "NEAR") and a.shortlisted


def test_backstop_covers_vendors_the_agent_never_examined(env):
    res, _ = env(good_policy)
    sai = vendor(res, "Sai Steel")                           # the agent never read or recorded anything for this vendor
    assert not any("agent-recorded" in e.claim for e in res.evidence if e.vendor_id == sai.id)
    assert res.evidence and any(e.vendor_id == sai.id for e in res.evidence)   # rules backstop gathered evidence
    assert sai.city == "Mumbai"


def test_recall_floor_agent_that_finds_nothing_triggers_the_rules_backstop(env):
    """Regression (found live): an agent killed by a quota before searching left a geography with 0 vendors."""
    res, _ = env(lambda step: ("finish", {"summary": "gave up"}))           # never searches
    assert all(d.get("rules_backstop", 0) > 0 for d in res.discovery)        # rule-driven discovery filled every geography
    assert any(v.tier == Tier.GLOBAL for v in res.vendors) and any(v.tier == Tier.AHMEDABAD for v in res.vendors)
    assert any("backstop" in lg.message for lg in res.logs)


def test_step_budget_stops_a_model_that_never_finishes(env):
    res, model = env(lambda step: ("status", {}), **{"llm.agent.max_steps": 3})
    assert all(d["finished_by"] == "max_steps" and d["steps"] == 3 for d in res.discovery)
    assert model.calls == 9 * 3


def test_search_budget_is_enforced_per_agent(env):
    res, _ = env(lambda step: ("search_web", {"query": f"q{step}", "scope": "india"}), **{"llm.agent.max_searches": 2, "llm.agent.max_steps": 5})
    assert all(d["searches"] == 2 for d in res.discovery)


def test_unknown_vendor_and_bad_arguments_are_handled_not_fatal(env):
    def policy(step):
        return [("record_evidence", {"vendor_id": "nope", "url": "u", "claim_type": "standard", "quote": "q"}),
                ("record_evidence", {"vendor_id": "x"}),                      # missing args
                ("no_such_tool", {}), ("finish", {"summary": "ok"})][min(step, 3)]
    res, _ = env(policy)
    assert all(d["finished_by"] == "model" for d in res.discovery)


def test_falls_back_to_rules_workflow_when_no_tool_calling_llm(tmp_path, monkeypatch):
    monkeypatch.setitem(search_mod.PROVIDERS, "serper", lambda: StubProvider())
    monkeypatch.setattr(Fetcher, "_fetch_network",
                        lambda self, url: Page(url=url, ok=True, status=200, text=PAGES[url]) if url in PAGES else Page(url=url, ok=False, error="HTTP 404"))
    monkeypatch.setattr(Fetcher, "_polite_wait", lambda self, host: None)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    monkeypatch.setattr("procure.config.load_dotenv_file", lambda path=None: None)
    from procure.config import llm_preset_overrides
    cfg = load_config(overrides={**llm_preset_overrides("gemini"), "llm.agent.enabled": True})
    req = ProcurementRequest(**json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8")))
    res = run_pipeline(req, cfg, cache_dir=tmp_path / "c")
    assert res.meta["llm_mode"].startswith("rules-only") and res.vendors
    assert any("falling back" in lg.message for lg in res.logs) and res.discovery[0]["queries"]   # rule-driven discovery ran


def test_history_compaction_elides_old_tool_results_but_keeps_recent_ones():
    msgs = [{"role": "system", "content": "s"}, {"role": "user", "content": "u"}]
    for i in range(10):
        msgs += [{"role": "assistant", "content": ""}, {"role": "tool", "tool_call_id": str(i), "content": "x" * 500 + str(i)}]
    out = compact(msgs, keep_last=6)
    assert len(out) == len(msgs)
    assert "elided" in out[3]["content"] and out[-1]["content"].endswith("9")
    assert out[0]["content"] == "s"
