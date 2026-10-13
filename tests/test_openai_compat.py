"""OpenAI-compatible client against a mocked HTTP transport (no network, no keys)."""
import json

import httpx
import pytest

from procure.cache import Cache, CacheMiss
from procure.config import llm_preset_overrides, llm_preset_names, load_config
from procure.context import RunContext
from procure.llm import LLMError, OpenAICompatLLM, extract_json

OV = {"llm.provider": "openai_compat", "llm.base_url": "http://x/v1", "llm.api_key_env": "X_KEY",
      "llm.fast_model": "fast-m", "llm.strong_model": "strong-m"}
SCHEMA = {"type": "object", "properties": {"a": {"type": "string"}}}


def make(tmp_path, handler, mode="auto", **extra):
    cfg = load_config(overrides={**OV, **extra})
    ctx = RunContext(cfg)
    client = httpx.Client(transport=httpx.MockTransport(handler))
    return OpenAICompatLLM(ctx, Cache(tmp_path, mode), api_key="k", client=client), ctx


def reply(content=None, tool_calls=None, finish="stop"):
    return httpx.Response(200, json={"choices": [{"message": {"content": content, "tool_calls": tool_calls}, "finish_reason": finish}]})


TOOL_TOOLS = [{"type": "function", "function": {"name": "finish", "parameters": {"type": "object", "properties": {}}}}]


def test_tool_calls_are_parsed_and_the_request_is_openai_shaped(tmp_path):
    seen = {}

    def handler(req):
        seen["url"], seen["auth"], seen["body"] = str(req.url), req.headers.get("authorization"), json.loads(req.content)
        return reply(None, [{"id": "t1", "type": "function", "function": {"name": "finish", "arguments": '{"summary": "ok"}'}}], "tool_calls")

    llm, _ = make(tmp_path, handler)
    res = llm.chat(tier="strong", messages=[{"role": "user", "content": "hi"}], tools=TOOL_TOOLS)
    assert res.tool_calls[0].name == "finish" and res.tool_calls[0].arguments == {"summary": "ok"}
    assert seen["url"] == "http://x/v1/chat/completions" and seen["auth"] == "Bearer k"
    assert seen["body"]["model"] == "strong-m" and seen["body"]["tools"] == TOOL_TOOLS
    assert "temperature" not in seen["body"]


def test_provider_extension_on_tool_calls_is_captured_cached_and_echoed(tmp_path):
    """Regression (found live): Gemini 3 returns extra_content.google.thought_signature on a tool call and 400s if the next
    request's assistant message does not carry it back."""
    sig = {"google": {"thought_signature": "SIG123"}}
    llm, _ = make(tmp_path, lambda r: reply(None, [{"id": "t1", "function": {"name": "finish", "arguments": "{}"}, "extra_content": sig}], "tool_calls"))
    res = llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert res.tool_calls[0].extra == sig
    again, _ = make(tmp_path, lambda r: (_ for _ in ()).throw(AssertionError("network")), mode="replay")
    assert again.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS).tool_calls[0].extra == sig


def test_agent_echoes_the_extension_in_the_next_request():
    from procure.agents.research import ResearchAgent  # noqa: F401  (import check)
    import json as _json
    from procure.llm import ChatResult, ToolCall
    from tests.test_agent import ScriptedChat
    sig = {"google": {"thought_signature": "SIG"}}

    class SigChat(ScriptedChat):
        def chat(self, **kw):
            self.calls += 1
            self.seen.append(kw["messages"])
            name, args = self.policy(sum(1 for m in kw["messages"] if m["role"] == "tool"))
            return ChatResult(None, [ToolCall(id=f"c{self.calls}", name=name, arguments=args, extra=sig)], "tool_calls")

    # drive one agent through the public run() with a stub environment
    from tests.test_agent import PAGES, StubProvider, GANESH_URL
    from procure.config import load_config
    from procure.context import RunContext
    from procure.cache import Cache
    from procure.fetch import Fetcher
    from procure.models import MaterialInput, Page, Tier
    from procure.normalize import normalise
    from procure.providers.search import SearchService
    from procure.state import State
    import tempfile
    cfg = load_config(overrides={"llm.agent.enabled": True, "llm.agent.max_steps": 3})
    ctx = RunContext(cfg)
    nm = normalise(MaterialInput(id="M", description_raw="ERW pipe, DN 50, 60.3 x 5.5 mm, IS 1239", quantity=1, unit="t"), cfg)
    cache = Cache(tempfile.mkdtemp(), "auto")
    search = SearchService(ctx, cache, StubProvider())
    fetcher = Fetcher(ctx, cache)
    model = SigChat(lambda step: ("status", {}))
    ResearchAgent(ctx, State([nm]), search, fetcher, model, nm, Tier.AHMEDABAD).run()
    last = model.seen[-1]
    calls = [c for m in last if m["role"] == "assistant" for c in m.get("tool_calls", [])]
    assert calls and all(c.get("extra_content") == sig for c in calls)


def test_bad_json_arguments_are_reported_not_crashed(tmp_path):
    llm, _ = make(tmp_path, lambda r: reply(None, [{"id": "t", "function": {"name": "finish", "arguments": "{oops"}}], "tool_calls"))
    res = llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert res.tool_calls[0].arguments_error and res.tool_calls[0].arguments == {}


def test_chat_steps_are_cached_and_replayable(tmp_path):
    llm, ctx = make(tmp_path, lambda r: reply("hello"))
    llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert ctx.budget.used["llm"] == 1
    again, _ = make(tmp_path, lambda r: (_ for _ in ()).throw(AssertionError("network used")), mode="replay")
    assert again.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS).content == "hello"
    with pytest.raises(CacheMiss):
        again.chat(tier="strong", messages=[{"role": "user", "content": "different"}], tools=TOOL_TOOLS)


def test_rate_limit_429_is_retried_using_retry_after(tmp_path, monkeypatch):
    sleeps, calls = [], {"n": 0}
    monkeypatch.setattr("procure.llm.time.sleep", lambda s: sleeps.append(s))

    def handler(req):
        calls["n"] += 1
        return httpx.Response(429, headers={"retry-after": "3"}, text="slow down") if calls["n"] == 1 else reply("ok")

    llm, _ = make(tmp_path, handler)
    assert llm.chat(tier="fast", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS).content == "ok"
    assert calls["n"] == 2 and 3.0 in sleeps


def test_daily_quota_429_trips_the_breaker_instead_of_sleeping_for_hours(tmp_path, monkeypatch):
    monkeypatch.setattr("procure.llm.time.sleep", lambda s: pytest.fail("must not sleep"))
    llm, ctx = make(tmp_path, lambda r: httpx.Response(429, headers={"retry-after": "7200"}, text="quota"))
    with pytest.raises(LLMError):
        llm.chat(tier="fast", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert llm.available is False and any("disabled" in lg.message for lg in ctx.logs)


GEMINI_DAILY = ('[{"error": {"code": 429, "message": "Quota exceeded ... limit: 20, model: m1. Please retry in 12h45m.", '
                '"details": [{"violations": [{"quotaId": "GenerateRequestsPerDayPerProjectPerModel-FreeTier"}]}, {"retryDelay": "45914s"}]}}]')


def test_daily_quota_rotates_to_the_next_model_and_remembers_it(tmp_path, monkeypatch):
    """Regression (found live): Gemini free tier = 20 requests/day/model. Do not sleep on it - switch model."""
    monkeypatch.setattr("procure.llm.time.sleep", lambda s: pytest.fail("must not sleep on a daily quota"))
    models = []

    def handler(req):
        body = json.loads(req.content)
        models.append(body["model"])
        return httpx.Response(429, text=GEMINI_DAILY) if body["model"] == "strong-m" else reply("served by " + body["model"])

    llm, ctx = make(tmp_path, handler, **{"llm.fallback_models": ["backup-1", "backup-2"]})
    out = llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert out.content == "served by backup-1" and models == ["strong-m", "backup-1"]
    assert llm.available and any("switching to backup-1" in lg.message for lg in ctx.logs)
    # a NEW client (next run) reads the persisted state and does not waste a call on the exhausted model
    models.clear()
    llm2, _ = make(tmp_path, handler, **{"llm.fallback_models": ["backup-1", "backup-2"]})
    llm2.chat(tier="strong", messages=[{"role": "user", "content": "y"}], tools=TOOL_TOOLS)
    assert models == ["backup-1"]


def test_flaky_model_is_benched_after_two_failures_and_the_next_one_is_used(tmp_path, monkeypatch):
    """Regression (found live): a model returning 503s / read timeouts cost ~7 minutes of retries and killed the agent."""
    monkeypatch.setattr("procure.llm.time.sleep", lambda s: None)
    seen = []

    def handler(req):
        model = json.loads(req.content)["model"]
        seen.append(model)
        if model == "strong-m":
            return httpx.Response(503, text="overloaded")
        return reply("from " + model)

    llm, ctx = make(tmp_path, handler, **{"llm.fallback_models": ["backup"]})
    out = llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert out.content == "from backup" and seen == ["strong-m", "strong-m", "backup"]       # 2 tries, then fail over
    assert llm.available and any("benched" in lg.message for lg in ctx.logs)


def test_retired_model_404_is_benched_for_a_day_and_skipped(tmp_path):
    """Regression (found live): 'gemini-2.5-flash is no longer available to new users' (HTTP 404) must rotate, not end the agent."""
    seen = []

    def handler(req):
        m = json.loads(req.content)["model"]
        seen.append(m)
        return httpx.Response(404, text="This model models/x is no longer available to new users.") if m == "strong-m" else reply("ok")

    llm, _ = make(tmp_path, handler, **{"llm.fallback_models": ["backup"]})
    assert llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS).content == "ok"
    assert seen == ["strong-m", "backup"]
    assert llm._exhausted["strong-m"] - __import__("time").time() > 80000           # ~24 h
    seen.clear()
    llm2, _ = make(tmp_path, handler, **{"llm.fallback_models": ["backup"]})
    llm2.chat(tier="strong", messages=[{"role": "user", "content": "y"}], tools=TOOL_TOOLS)
    assert seen == ["backup"]                                                         # remembered across runs


def test_read_timeouts_also_fail_over(tmp_path, monkeypatch):
    monkeypatch.setattr("procure.llm.time.sleep", lambda s: None)

    def handler(req):
        if json.loads(req.content)["model"] == "strong-m":
            raise httpx.ReadTimeout("slow", request=req)
        return reply("ok")

    llm, _ = make(tmp_path, handler, **{"llm.fallback_models": ["backup"]})
    assert llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS).content == "ok"


def test_unsupported_tuning_param_is_dropped_and_the_call_retried(tmp_path):
    bodies = []

    def handler(req):
        body = json.loads(req.content)
        bodies.append(body)
        return httpx.Response(400, text="Unknown field: reasoning_effort") if "reasoning_effort" in body else reply("ok")

    llm, _ = make(tmp_path, handler, **{"llm.extra_params": {"reasoning_effort": "low"}})
    assert llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS).content == "ok"
    assert "reasoning_effort" in bodies[0] and "reasoning_effort" not in bodies[1]
    llm.chat(tier="strong", messages=[{"role": "user", "content": "y"}], tools=TOOL_TOOLS)
    assert "reasoning_effort" not in bodies[-1]                      # remembered: not sent again


def test_extra_params_are_sent_when_supported(tmp_path):
    bodies = []
    llm, _ = make(tmp_path, lambda r: (bodies.append(json.loads(r.content)), reply("ok"))[1], **{"llm.extra_params": {"reasoning_effort": "low"}})
    llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert bodies[0]["reasoning_effort"] == "low"


def test_every_model_exhausted_disables_the_llm_once(tmp_path):
    llm, ctx = make(tmp_path, lambda r: httpx.Response(429, text=GEMINI_DAILY), **{"llm.fallback_models": ["b1"]})
    with pytest.raises(LLMError):
        llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    assert llm.available is False and any("every configured model" in lg.message for lg in ctx.logs)


def test_rotation_replaces_signatures_that_belong_to_the_previous_model(tmp_path):
    sent = []

    def handler(req):
        body = json.loads(req.content)
        sent.append(body)
        return httpx.Response(429, text=GEMINI_DAILY) if body["model"] == "strong-m" else reply("ok")

    llm, _ = make(tmp_path, handler, **{"llm.fallback_models": ["backup"]})
    hist = [{"role": "user", "content": "x"},
            {"role": "assistant", "content": "", "tool_calls": [{"id": "1", "type": "function", "function": {"name": "finish", "arguments": "{}"},
                                                                 "extra_content": {"google": {"thought_signature": "REAL"}}}]},
            {"role": "tool", "tool_call_id": "1", "content": "{}"}]
    llm.chat(tier="strong", messages=hist, tools=TOOL_TOOLS)
    assert sent[0]["messages"][1]["tool_calls"][0]["extra_content"]["google"]["thought_signature"] == "REAL"      # primary model: original
    assert sent[1]["messages"][1]["tool_calls"][0]["extra_content"]["google"]["thought_signature"] == "skip_thought_signature_validator"
    assert hist[1]["tool_calls"][0]["extra_content"]["google"]["thought_signature"] == "REAL"                   # caller's history untouched


def test_replay_works_regardless_of_which_model_served_the_call(tmp_path):
    llm, _ = make(tmp_path, lambda r: httpx.Response(429, text=GEMINI_DAILY) if json.loads(r.content)["model"] == "strong-m" else reply("hi"),
                  **{"llm.fallback_models": ["backup"]})
    llm.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS)
    again, _ = make(tmp_path, lambda r: (_ for _ in ()).throw(AssertionError("network")), mode="replay", **{"llm.fallback_models": ["backup"]})
    assert again.chat(tier="strong", messages=[{"role": "user", "content": "x"}], tools=TOOL_TOOLS).content == "hi"


def test_auth_failure_disables_after_one_call(tmp_path):
    calls = {"n": 0}

    def handler(req):
        calls["n"] += 1
        return httpx.Response(401, text="bad key")

    llm, _ = make(tmp_path, handler)
    for msg in ("a", "b"):
        with pytest.raises(LLMError):
            llm.chat(tier="fast", messages=[{"role": "user", "content": msg}], tools=TOOL_TOOLS)
    assert calls["n"] == 1 and llm.available is False


def test_json_mode_and_fence_stripping(tmp_path):
    bodies = []

    def handler(req):
        bodies.append(json.loads(req.content))
        return reply('```json\n{"a": "x"}\n```')

    llm, _ = make(tmp_path, handler)
    assert llm.complete_json(tier="fast", system="s", user="u", schema=SCHEMA) == {"a": "x"}
    assert bodies[0]["response_format"] == {"type": "json_object"} and "JSON Schema" in bodies[0]["messages"][0]["content"]


def test_provider_without_json_mode_falls_back_to_prompt_only(tmp_path):
    calls = []

    def handler(req):
        body = json.loads(req.content)
        calls.append("response_format" in body)
        if "response_format" in body:
            return httpx.Response(400, text="response_format is not supported")
        return reply('{"a": "y"}')

    llm, _ = make(tmp_path, handler)
    assert llm.complete_json(tier="fast", system="s", user="u", schema=SCHEMA) == {"a": "y"}
    assert calls == [True, False]


def test_truncated_response_is_an_error(tmp_path):
    llm, _ = make(tmp_path, lambda r: reply('{"a": "x', finish="length"))
    with pytest.raises(LLMError):
        llm.complete_json(tier="fast", system="s", user="u", schema=SCHEMA)


def test_extract_json_variants():
    assert extract_json('Sure! {"a": 1} hope that helps') == {"a": 1}
    assert extract_json('```\n{"a": 2}\n```') == {"a": 2}
    with pytest.raises(ValueError):
        extract_json("no json here")


def test_presets_are_complete_and_never_contain_secrets():
    names = llm_preset_names()
    assert {"gemini", "groq", "openrouter", "ollama", "anthropic", "none"} <= set(names)
    for n in names:
        ov = llm_preset_overrides(n)
        if ov["llm.provider"] == "openai_compat":
            assert ov["llm.base_url"].startswith("http") and ov["llm.fast_model"] and ov["llm.strong_model"]
            assert "key" not in " ".join(str(v) for k, v in ov.items() if k != "llm.api_key_env").lower()
            assert not str(ov.get("llm.api_key_env") or "").startswith(("sk-", "AIza"))   # an env var NAME, not a key
    cfg = load_config(overrides=llm_preset_overrides("groq"))
    assert cfg.llm.provider == "openai_compat" and cfg.llm.api_key_env == "GROQ_API_KEY"
