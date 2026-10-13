"""A fresh clone has no SERPER_API_KEY: the committed demo input must still run from recorded searches."""
import json
from pathlib import Path

import pytest

from procure.cache import Cache
from procure.config import load_config
from procure.context import RunContext
from procure.providers.search import ProviderError, SearchService, build_search_service

from tests.test_pipeline_offline import StubProvider

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture()
def no_key(monkeypatch):
    monkeypatch.delenv("SERPER_API_KEY", raising=False)
    monkeypatch.setattr("procure.config.load_dotenv_file", lambda path=None: None)


def test_no_key_auto_mode_serves_recorded_searches_and_reports_unrecorded(tmp_path, no_key):
    cfg = load_config(overrides={"llm.provider": "none"})
    # 1) record one search with a stub provider (stands in for an earlier live run)
    rec = SearchService(RunContext(cfg), Cache(tmp_path, "auto"), StubProvider())
    recorded = rec.search("recorded query", country="in")
    assert recorded
    # 2) a new "machine" with no key, same cache
    ctx = RunContext(cfg)
    svc = build_search_service(ctx, Cache(tmp_path, "auto"))
    assert [r.url for r in svc.search("recorded query", country="in")] == [r.url for r in recorded]   # served from the record
    assert svc.search("never recorded", country="in") == []                                           # reported, not fatal
    msgs = [lg.message for lg in ctx.logs]
    assert any("recorded searches only" in m for m in msgs) and any("no recorded response" in m for m in msgs)
    assert ctx.budget.used["search"] == 0                                                              # no paid call was attempted


def test_refresh_mode_without_a_key_still_fails_loudly(tmp_path, no_key):
    cfg = load_config(overrides={"llm.provider": "none"})
    with pytest.raises(ProviderError):
        build_search_service(RunContext(cfg), Cache(tmp_path, "refresh"))
