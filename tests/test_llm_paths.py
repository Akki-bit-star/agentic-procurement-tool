"""LLM code paths exercised with fakes (no API key needed): grounding, evidence gate, and failure containment."""
import json
from types import SimpleNamespace

import pytest

from procure.agents.discovery import Draft, llm_refine_names
from procure.agents.verify import llm_extract_evidence
from procure.cache import Cache, CacheMiss
from procure.config import load_config
from procure.context import RunContext
from procure.llm import AnthropicLLM, LLMError
from procure.models import MaterialInput, SearchResult
from procure.normalize import normalise
from procure.state import State

CFG = load_config(overrides={"llm.provider": "anthropic"})


class FakeLLM:
    available = True

    def __init__(self, payload=None, exc=None):
        self.payload, self.exc, self.calls = payload, exc, 0

    def complete_json(self, **kw):
        self.calls += 1
        if self.exc:
            raise self.exc
        return self.payload


def test_llm_name_is_ignored_unless_it_appears_in_the_result_text():
    ctx = RunContext(CFG)
    r = SearchResult(title="MS ERW Pipe at best price", snippet="Sold by Sai Steel Industries in Pune", url="https://x.example")
    d = Draft(name="Rules Name", url=r.url, domain="x.example", result=r, from_places=False, marketplace=False)
    llm_refine_names([d], FakeLLM({"items": [{"i": 0, "vendor_name": "Totally Invented Pvt Ltd", "is_vendor": True, "vendor_type": "MANUFACTURER"}]}), ctx)
    assert d.name == "Rules Name"                               # hallucinated name rejected by the grounding check
    llm_refine_names([d], FakeLLM({"items": [{"i": 0, "vendor_name": "Sai Steel Industries", "is_vendor": True, "vendor_type": "STOCKIST"}]}), ctx)
    assert d.name == "Sai Steel Industries" and d.vendor_type.value == "STOCKIST"


def test_llm_failure_degrades_to_rules_and_is_logged():
    ctx = RunContext(CFG)
    r = SearchResult(title="t", snippet="s", url="https://x.example")
    d = Draft(name="Keep Me", url=r.url, domain="x.example", result=r, from_places=False, marketplace=False)
    llm_refine_names([d], FakeLLM(exc=LLMError("boom")), ctx)
    assert d.name == "Keep Me" and any("skipped" in lg.message for lg in ctx.logs)


def test_fabricated_llm_quote_never_reaches_the_ledger():
    ctx = RunContext(CFG)
    nm = normalise(MaterialInput(id="M", description_raw="ERW pipe, DN 50, 60.3 x 3.6 mm, IS 1239", quantity=1, unit="t"), CFG)
    page = "Acme Tubes makes ERW pipe 50 NB to IS 1239 in Surat, Gujarat."
    fake = FakeLLM({"claims": [
        {"claim_type": "standard", "claim": "IS 1239", "quote": "ERW pipe 50 NB to IS 1239", "material_ids": ["M"]},
        {"claim_type": "certification", "claim": "BIS licence", "quote": "BIS licence CM/L-9999999 valid till 2030", "material_ids": []}]})
    items = llm_extract_evidence(fake, ctx, page, "https://acme.example", "acme", "vendor_site", [nm])
    assert len(items) == 2                                       # the LLM returned both ...
    st = State([nm])
    st.add_source_text("https://acme.example", page)
    admitted = [e for e in items if st.gate(e)]
    assert [e.claim_type for e in admitted] == ["standard"]      # ... the gate admitted only the quote that exists
    assert st.dropped_claims[0]["claim"] == "BIS licence"


def _resp(stop, text=None):
    blocks = [SimpleNamespace(type="text", text=text)] if text is not None else []
    return SimpleNamespace(stop_reason=stop, content=blocks)


def _llm(tmp_path, response, mode="auto"):
    ctx = RunContext(CFG)
    llm = AnthropicLLM(ctx, Cache(tmp_path, mode), api_key="test")
    created = {}

    def create(**kw):
        created.update(kw)
        return response

    llm._client = SimpleNamespace(messages=SimpleNamespace(create=create))
    return llm, created


SCHEMA = {"type": "object", "additionalProperties": False, "required": ["a"], "properties": {"a": {"type": "string"}}}


def test_request_shape_has_no_sampling_params_and_uses_structured_output(tmp_path):
    llm, sent = _llm(tmp_path, _resp("end_turn", '{"a": "x"}'))
    assert llm.complete_json(tier="fast", system="s", user="u", schema=SCHEMA) == {"a": "x"}
    assert "temperature" not in sent and "top_p" not in sent and "tool_choice" not in sent
    assert sent["output_config"]["format"]["type"] == "json_schema" and sent["output_config"]["effort"] == "low"
    assert sent["model"] == CFG.llm.fast_model


def test_response_is_cached_and_replayable(tmp_path):
    llm, _ = _llm(tmp_path, _resp("end_turn", '{"a": "x"}'))
    llm.complete_json(tier="fast", system="s", user="u", schema=SCHEMA)
    assert llm.ctx.budget.used["llm"] == 1
    again = AnthropicLLM(RunContext(CFG), Cache(tmp_path, "replay"), api_key=None)
    assert again.complete_json(tier="fast", system="s", user="u", schema=SCHEMA) == {"a": "x"}   # no key, no network
    with pytest.raises(CacheMiss):
        again.complete_json(tier="fast", system="s", user="DIFFERENT", schema=SCHEMA)


def test_billing_error_trips_the_circuit_breaker_after_one_call(tmp_path):
    """A key with no credit must cost ONE failed call, not one per stage, and the run continues rules-only."""
    import anthropic
    import httpx
    ctx = RunContext(CFG)
    llm = AnthropicLLM(ctx, Cache(tmp_path, "auto"), api_key="test")
    calls = {"n": 0}

    def create(**kw):
        calls["n"] += 1
        raise anthropic.BadRequestError("Your credit balance is too low to access the Anthropic API.",
                                        response=httpx.Response(400, request=httpx.Request("POST", "http://x")), body=None)

    llm._client = SimpleNamespace(messages=SimpleNamespace(create=create))
    with pytest.raises(LLMError):
        llm.complete_json(tier="fast", system="s", user="u", schema=SCHEMA)
    assert llm.available is False and any("disabled" in lg.message for lg in ctx.logs)
    with pytest.raises(LLMError):
        llm.complete_json(tier="fast", system="s", user="u2", schema=SCHEMA)
    assert calls["n"] == 1                                       # the second call never reached the API


@pytest.mark.parametrize("stop,text", [("refusal", None), ("max_tokens", '{"a": "x'), ("end_turn", "not json")])
def test_refusal_truncation_and_bad_json_are_errors_not_answers(tmp_path, stop, text):
    llm, _ = _llm(tmp_path, _resp(stop, text))
    with pytest.raises(LLMError):
        llm.complete_json(tier="strong", system="s", user="u", schema=SCHEMA)
    assert Cache(tmp_path, "auto").get("llm", {"model": CFG.llm.strong_model, "effort": "medium", "system": "s", "user": "u", "schema": SCHEMA}) is None
