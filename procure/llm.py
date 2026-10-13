"""LLM access behind a tiny interface.

Design notes (current Claude API behaviour):
  * no sampling parameters are sent - current models reject non-default temperature/top_p;
    reproducibility comes from the response cache, not from sampling settings
  * structured output via `output_config.format` (JSON schema), not forced tool_choice
  * `effort` is set low for extraction work and medium for judgement
  * thinking counts toward max_tokens, so max_tokens is generous
  * `refusal` / `max_tokens` stop reasons are surfaced as errors, never parsed as answers
"""
from __future__ import annotations

import json
import re
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

import httpx

from .cache import Cache, CacheMiss
from .config import secret
from .context import RunContext


class LLMError(RuntimeError):
    pass


class ModelUnavailable(LLMError):
    """A model keeps failing (5xx / timeouts). Treated like an exhausted model: rotate instead of retrying for minutes."""

    def __init__(self, model: str, reason: str, bench_seconds: float = 600.0):
        super().__init__(f"{model} unavailable ({reason})")
        self.model, self.reason, self.bench_seconds = model, reason, bench_seconds


class QuotaExhausted(LLMError):
    """A model's (daily) quota is used up. Not fatal for the run if another model is configured."""

    def __init__(self, model: str, retry_seconds: float):
        super().__init__(f"quota exhausted for {model} (resets in ~{retry_seconds / 3600:.1f} h)")
        self.model, self.retry_seconds = model, retry_seconds


class LLMClient(Protocol):
    available: bool

    def complete_json(self, *, tier: str, system: str, user: str, schema: dict[str, Any],
                      max_tokens: int = 6000, label: str = "") -> dict[str, Any]: ...


class NullLLM:
    """Used when no key is configured: the pipeline falls back to deterministic rules only."""
    available = False

    def complete_json(self, **_: Any) -> dict[str, Any]:
        raise LLMError("LLM disabled")


class AnthropicLLM:
    def __init__(self, ctx: RunContext, cache: Cache, api_key: str | None):
        self.available = True            # flips to False after a fatal API error (circuit breaker)
        self.ctx, self.cache = ctx, cache
        self._key = api_key
        self._client = None

    def _models(self, tier: str) -> tuple[str, str]:
        cfg = self.ctx.cfg.llm
        return (cfg.fast_model, "low") if tier == "fast" else (cfg.strong_model, "medium")

    def _get_client(self):
        if self._client is None:
            import anthropic  # lazy: replay mode must work without the SDK configured
            self._client = anthropic.Anthropic(api_key=self._key)
        return self._client

    def complete_json(self, *, tier: str, system: str, user: str, schema: dict[str, Any],
                      max_tokens: int = 6000, label: str = "") -> dict[str, Any]:
        model, effort = self._models(tier)
        params = {"model": model, "effort": effort, "system": system, "user": user, "schema": schema}
        cached = self.cache.get("llm", params)
        if cached is not None:
            return cached
        self.cache.require_network_allowed(f"llm {label or model}")   # CacheMiss in replay mode
        if not self._key:
            raise LLMError("ANTHROPIC_API_KEY not set")
        if not self.available:
            raise LLMError("LLM disabled after an earlier fatal error")
        self.ctx.budget.spend("llm")
        import anthropic
        client = self._get_client()
        output_config: dict[str, Any] = {"format": {"type": "json_schema", "schema": schema}, "effort": effort}
        try:
            try:
                resp = client.messages.create(model=model, max_tokens=max_tokens, system=system,
                                              messages=[{"role": "user", "content": user}],
                                              output_config=output_config)
            except anthropic.BadRequestError as e:
                if "effort" not in str(e).lower():
                    raise
                output_config.pop("effort")      # a model that does not accept `effort`
                resp = client.messages.create(model=model, max_tokens=max_tokens, system=system,
                                              messages=[{"role": "user", "content": user}],
                                              output_config=output_config)
        except anthropic.APIStatusError as e:
            msg = str(getattr(e, "message", e))
            # Fatal for the whole run (billing / auth / permission): stop calling instead of failing 100+ more times.
            if e.status_code in (401, 403) or (e.status_code == 400 and "credit balance" in msg.lower()):
                self.available = False
                self.ctx.log("llm", "error", f"LLM disabled for the rest of this run ({e.status_code}: {msg[:140]}). "
                                              "Continuing in rules-only mode.")
            raise LLMError(f"API error {e.status_code}: {msg}") from e
        except anthropic.APIConnectionError as e:
            raise LLMError(f"connection error: {e}") from e

        if resp.stop_reason == "refusal":
            raise LLMError("model refused this request")
        if resp.stop_reason == "max_tokens":
            raise LLMError("response truncated (max_tokens) - not parsed")
        text = next((b.text for b in resp.content if getattr(b, "type", "") == "text"), None)
        if not text:
            raise LLMError("no text block in response")
        try:
            data = json.loads(text)
        except ValueError as e:
            raise LLMError(f"invalid JSON from model: {e}") from e
        self.cache.put("llm", params, data)
        return data


# --------------------------------------------------------------------------- OpenAI-compatible providers
@dataclass
class ToolCall:
    id: str
    name: str
    arguments: dict[str, Any]
    arguments_error: str | None = None       # set when the model sent unparseable JSON arguments
    extra: dict[str, Any] | None = None      # provider extension that MUST be echoed back (Gemini 3: thought_signature)


@dataclass
class ChatResult:
    content: str | None
    tool_calls: list[ToolCall]
    finish_reason: str | None = None

    def to_cache(self) -> dict[str, Any]:
        return {"content": self.content, "finish_reason": self.finish_reason,
                "tool_calls": [{"id": t.id, "name": t.name, "arguments": t.arguments, "arguments_error": t.arguments_error,
                                "extra": t.extra} for t in self.tool_calls]}

    @staticmethod
    def from_cache(d: dict[str, Any]) -> "ChatResult":
        return ChatResult(d.get("content"), [ToolCall(**t) for t in d.get("tool_calls", [])], d.get("finish_reason"))


def extract_json(text: str) -> dict[str, Any]:
    """Models sometimes wrap JSON in prose or code fences; take the outermost object."""
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*\s*|\s*```$", "", text).strip()
    try:
        return json.loads(text)
    except ValueError:
        a, b = text.find("{"), text.rfind("}")
        if a >= 0 and b > a:
            return json.loads(text[a:b + 1])
        raise


class OpenAICompatLLM:
    """Any OpenAI-compatible chat-completions endpoint (Gemini, Groq, OpenRouter, Ollama, OpenAI, ...).

    * `complete_json` - JSON-mode call for the labelling / quote-picking stages
    * `chat`          - tool-calling turn for the research agent
    Both are cached by request hash (replay), paced to `requests_per_minute`, retried on 429/5xx, and a fatal auth /
    quota error disables the client for the rest of the run (circuit breaker).
    """
    supports_tools = True
    DUMMY_SIGNATURE = "skip_thought_signature_validator"   # Gemini's documented value for tool calls produced by another model

    def __init__(self, ctx: RunContext, cache: Cache, api_key: str | None, client: httpx.Client | None = None):
        self.available = True
        self.ctx, self.cache, self._key = ctx, cache, api_key
        self._client = client or httpx.Client(timeout=90.0)
        self._lock = threading.Lock()
        self._next_slot = 0.0
        self._json_mode = True
        self._extra: dict[str, Any] = dict(ctx.cfg.llm.extra_params)
        self._state_path = Path(cache.root) / ".llm_state.json"      # git-ignored: which models are out of quota, until when
        self._exhausted: dict[str, float] = self._load_state()

    # ---- quota state (daily limits are per model; remember them so a re-run does not waste calls)
    def _load_state(self) -> dict[str, float]:
        try:
            raw = json.loads(self._state_path.read_text(encoding="utf-8"))
            now = time.time()
            return {m: t for m, t in raw.items() if t > now}
        except (OSError, ValueError):
            return {}

    def _save_state(self) -> None:
        try:
            self._state_path.parent.mkdir(parents=True, exist_ok=True)
            self._state_path.write_text(json.dumps(self._exhausted), encoding="utf-8")
        except OSError:
            pass

    def _mark_exhausted(self, model: str, seconds: float) -> None:
        self._exhausted[model] = time.time() + max(60.0, seconds)
        self._save_state()

    # ---- plumbing
    def _primary(self, tier: str) -> str:
        cfg = self.ctx.cfg.llm
        return cfg.fast_model if tier == "fast" else cfg.strong_model

    def _active_model(self, tier: str) -> str | None:
        """First model of [primary, *fallbacks] that is not out of quota."""
        cfg = self.ctx.cfg.llm
        for m in [self._primary(tier), *[x for x in cfg.fallback_models if x != self._primary(tier)]]:
            if self._exhausted.get(m, 0) <= time.time():
                return m
        return None

    @classmethod
    def _resign(cls, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """After rotating models, tool-call signatures from the previous model are not valid for the new one."""
        out = []
        for m in messages:
            if m.get("tool_calls"):
                calls = []
                for c in m["tool_calls"]:
                    c = dict(c)
                    if (c.get("extra_content") or {}).get("google", {}).get("thought_signature"):
                        c["extra_content"] = {"google": {"thought_signature": cls.DUMMY_SIGNATURE}}
                    calls.append(c)
                m = {**m, "tool_calls": calls}
            out.append(m)
        return out

    def _pace(self) -> None:
        rpm = self.ctx.cfg.llm.requests_per_minute
        if not rpm:
            return
        with self._lock:
            now = time.monotonic()
            wait = max(0.0, self._next_slot - now)
            self._next_slot = max(now, self._next_slot) + 60.0 / rpm
        if wait:
            time.sleep(wait)

    def _disable(self, why: str) -> None:
        self.available = False
        self.ctx.log("llm", "error", f"LLM disabled for the rest of this run ({why[:200]}). Continuing without it.")

    def _post(self, payload: dict[str, Any]) -> dict[str, Any]:
        cfg = self.ctx.cfg.llm
        url = cfg.base_url.rstrip("/") + "/chat/completions"
        headers = {"Content-Type": "application/json"}
        if self._key:
            headers["Authorization"] = f"Bearer {self._key}"
        last = "no attempt"
        server_fails = 0
        for attempt in range(5):
            self._pace()
            try:
                r = self._client.post(url, headers=headers, json=payload)
            except httpx.TransportError as e:
                last = f"transport error: {e}"
                server_fails += 1
                if server_fails >= 2:                           # slow / dead model: fail over, do not wait minutes on it
                    raise ModelUnavailable(payload.get("model", "?"), last) from e
                time.sleep(2)
                continue
            if r.status_code == 429:
                ra = r.headers.get("retry-after")
                body = r.text
                m = re.search(r'"retryDelay"\s*:\s*"(\d+(?:\.\d+)?)s"', body)      # Gemini puts the delay in the body
                if ra and re.fullmatch(r"\d+(\.\d+)?", ra):
                    wait = float(ra)
                elif m:
                    wait = float(m.group(1))
                else:
                    wait = 5.0 * (attempt + 1)
                if wait > 90 or re.search(r"PerDay|per day|daily", body, re.I):
                    # a DAILY quota is not a blip: do not sleep on it. The caller rotates to another model if it can.
                    raise QuotaExhausted(payload.get("model", "?"), max(wait, 3600.0 if wait <= 90 else wait))
                last = f"429 rate limited; waited {wait:.0f}s"
                time.sleep(wait)
                continue
            if r.status_code in (500, 502, 503, 504):
                last = f"HTTP {r.status_code}"
                server_fails += 1
                if server_fails >= 2:
                    raise ModelUnavailable(payload.get("model", "?"), last)
                time.sleep(2)
                continue
            if r.status_code == 404 and re.search(r"no longer available|not found|not supported|does not exist", r.text, re.I):
                # retired / unknown model id: bench it for a day and move on (found live: gemini-2.5-flash returned this)
                raise ModelUnavailable(payload.get("model", "?"), "model not available to this key (HTTP 404)", bench_seconds=86400.0)
            if r.status_code in (401, 402, 403):
                self._disable(f"HTTP {r.status_code}: {r.text[:160]}")
                raise LLMError(f"HTTP {r.status_code}: {r.text[:200]}")
            if r.status_code >= 400:
                raise LLMError(f"HTTP {r.status_code}: {r.text[:300]}")
            return r.json()
        raise LLMError(f"gave up after retries ({last})")

    def _base_payload(self, tier: str, messages: list[dict], max_tokens: int) -> dict[str, Any]:
        # `model` is chosen per attempt by _send(); extra_params are provider tuning knobs (e.g. reasoning_effort: low)
        return {"messages": messages, "max_tokens": max_tokens, **self._extra}

    def _send(self, tier: str, payload: dict[str, Any]) -> dict[str, Any]:
        """POST, rotating to the next configured model whenever one runs out of (daily) quota."""
        primary = self._primary(tier)
        while True:
            model = self._active_model(tier)
            if model is None:
                self._disable("daily quota exhausted on every configured model")
                raise LLMError("daily quota exhausted on every configured model")
            body = {**payload, "model": model}
            if model != primary and "messages" in body:
                body["messages"] = self._resign(body["messages"])
            try:
                return self._post(body)
            except QuotaExhausted as q:
                self._mark_exhausted(model, q.retry_seconds)
                nxt = self._active_model(tier)
                self.ctx.log("llm", "warn", f"{model}: daily quota exhausted (resets in ~{q.retry_seconds / 3600:.1f} h) - "
                                            + (f"switching to {nxt}" if nxt else "no fallback model left"))
            except ModelUnavailable as u:
                self._mark_exhausted(model, u.bench_seconds)
                nxt = self._active_model(tier)
                self.ctx.log("llm", "warn", f"{model}: {u.reason} - benched for {u.bench_seconds / 60:.0f} min, "
                                            + (f"switching to {nxt}" if nxt else "no fallback model left"))
            except LLMError as e:
                bad = [k for k in list(self._extra) if k in str(e)]
                if "HTTP 400" in str(e) and bad:                  # provider rejects a tuning knob: drop it and retry once
                    for k in bad:
                        self._extra.pop(k, None)
                        payload.pop(k, None)
                    self.ctx.log("llm", "info", f"provider rejected {bad}; continuing without")
                    continue
                raise

    def _guard(self, what: str) -> None:
        if not self._key and self.ctx.cfg.llm.api_key_env:
            raise LLMError(f"{self.ctx.cfg.llm.api_key_env} is not set")
        if not self.available:
            raise LLMError("LLM disabled after an earlier fatal error")
        self.cache.require_network_allowed(what)            # CacheMiss in replay mode
        self.ctx.budget.spend("llm")

    # ---- JSON mode
    def complete_json(self, *, tier: str, system: str, user: str, schema: dict[str, Any],
                      max_tokens: int = 6000, label: str = "") -> dict[str, Any]:
        model = self._primary(tier)      # cache key uses the CONFIGURED model, so rotation does not break replay
        params = {"model": model, "system": system, "user": user, "schema": schema, "kind": "json"}
        cached = self.cache.get("llm", params)
        if cached is not None:
            return cached
        self._guard(f"llm {label or model}")
        sys_msg = (system + "\n\nReply with ONE JSON object only (no prose, no code fences) matching this JSON Schema:\n"
                   + json.dumps(schema))
        payload = self._base_payload(tier, [{"role": "system", "content": sys_msg}, {"role": "user", "content": user}], max_tokens)
        if self._json_mode:
            payload["response_format"] = {"type": "json_object"}
        try:
            data = self._send(tier, payload)
        except LLMError as e:
            if self._json_mode and "HTTP 400" in str(e) and "response_format" in str(e).lower():
                self._json_mode = False                          # provider does not support JSON mode: ask in the prompt only
                payload.pop("response_format", None)
                data = self._send(tier, payload)
            else:
                raise
        choice = (data.get("choices") or [{}])[0]
        text = (choice.get("message") or {}).get("content")
        if choice.get("finish_reason") == "length":
            raise LLMError("response truncated (max_tokens) - not parsed")
        if not text:
            raise LLMError("empty response")
        try:
            out = extract_json(text)
        except ValueError as e:
            raise LLMError(f"invalid JSON from model: {e}") from e
        self.cache.put("llm", params, out)
        return out

    # ---- tool-calling turn (agent)
    def chat(self, *, tier: str, messages: list[dict[str, Any]], tools: list[dict[str, Any]], max_tokens: int = 1500,
             label: str = "agent") -> ChatResult:
        model = self._primary(tier)
        params = {"model": model, "messages": messages, "tools": tools, "kind": "chat", "v": 2}   # v2: tool-call extras round-trip
        cached = self.cache.get("llm", params)
        if cached is not None:
            return ChatResult.from_cache(cached)
        self._guard(f"llm chat {label}")
        payload = self._base_payload(tier, messages, max_tokens)
        payload["tools"] = tools
        payload["tool_choice"] = "auto"
        data = self._send(tier, payload)
        choice = (data.get("choices") or [{}])[0]
        msg = choice.get("message") or {}
        calls = []
        for i, tc in enumerate(msg.get("tool_calls") or []):
            fn = tc.get("function") or {}
            raw = fn.get("arguments")
            args, err = {}, None
            if isinstance(raw, dict):
                args = raw
            else:
                try:
                    args = json.loads(raw) if raw else {}
                except ValueError as e:
                    err = f"arguments were not valid JSON: {e}"
            calls.append(ToolCall(id=tc.get("id") or f"call_{i}", name=fn.get("name", ""), arguments=args if isinstance(args, dict) else {},
                                  arguments_error=err, extra=tc.get("extra_content")))
        res = ChatResult(msg.get("content"), calls, choice.get("finish_reason"))
        self.cache.put("llm", params, res.to_cache())
        return res


def build_llm(ctx: RunContext, cache: Cache) -> LLMClient:
    cfg = ctx.cfg.llm
    if cfg.provider == "none":
        return NullLLM()
    if cfg.provider == "openai_compat":
        if not cfg.base_url:
            ctx.log("setup", "warn", "llm.base_url is not set - running without an LLM")
            return NullLLM()
        key = secret(cfg.api_key_env) if cfg.api_key_env else None
        if cfg.api_key_env and not key and cache.mode != "replay":
            ctx.log("setup", "warn", f"{cfg.api_key_env} is not set - running without an LLM (rules-only)")
            return NullLLM()
        return OpenAICompatLLM(ctx, cache, key)
    key = secret("ANTHROPIC_API_KEY")
    if not key and cache.mode != "replay":
        ctx.log("setup", "warn", "ANTHROPIC_API_KEY not set - running in rules-only mode "
                                 "(deterministic evidence extraction, no LLM judgement)")
        return NullLLM()
    return AnthropicLLM(ctx, cache, key)
