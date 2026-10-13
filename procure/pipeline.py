"""Orchestrator: wires the stages together. The API/UI and the CLI both call `run_pipeline` - one code path."""
from __future__ import annotations

import hashlib
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from .agents.discovery import run_discovery
from .agents.research import run_agents
from .agents.verify import run_verification
from .assess import assess_all
from .cache import Cache
from .config import RunConfig, ROOT
from .context import RunContext
from .fetch import Fetcher
from .llm import NullLLM, build_llm
from .models import (Evidence, NormalisedMaterial, ProcurementRequest, RunLog, Severity, Tier, Vendor, utcnow)
from .normalize import normalise
from .providers.search import ProviderError, build_search_service
from .resolve import decide_geography, dedupe
from .state import State


class NeedsClarification(RuntimeError):
    """Raised in --strict mode when a CRITICAL ambiguity exists."""

    def __init__(self, flags: list[dict]):
        super().__init__("critical ambiguities need confirmation before the search can run")
        self.flags = flags


class RunResult(BaseModel):
    meta: dict[str, Any]
    assumptions: list[str]
    materials: list[NormalisedMaterial]
    vendors: list[Vendor]
    evidence: list[Evidence]
    coverage: list[dict[str, Any]]
    discovery: list[dict[str, Any]] = Field(default_factory=list)
    excluded_candidates: list[dict[str, Any]] = Field(default_factory=list)
    dropped_claims: list[dict[str, Any]] = Field(default_factory=list)
    fetch_failures: list[dict[str, Any]] = Field(default_factory=list)
    logs: list[RunLog] = Field(default_factory=list)


def normalise_request(req: ProcurementRequest, cfg: RunConfig) -> list[NormalisedMaterial]:
    return [normalise(m, cfg) for m in req.materials]


def collect_assumptions(nms: list[NormalisedMaterial], cfg: RunConfig) -> list[str]:
    out = []
    for nm in nms:
        for f in nm.flags:
            if f.assumption:
                out.append(f"[{nm.original.id}] {f.code}: {f.assumption}")
    out += [
        "Evidence is limited to public web sources found by the search provider; absence of evidence is reported as 'not found', never as a negative fact.",
        "Manufacturer / trader status comes from the vendor's own wording and is self-declared.",
        "Prices, lead times, stock and MOQ are never estimated; they are marked NEEDS_RFQ.",
        f"Ranking weights and confidence rules are those in config ({', '.join(f'{k} {v:.0%}' for k, v in cfg.weights.items())}).",
    ]
    return out


def coverage_table(state: State, cfg: RunConfig) -> list[dict[str, Any]]:
    rows = []
    for nm in state.materials:
        for tier in (Tier.AHMEDABAD, Tier.INDIA_OTHER, Tier.GLOBAL, Tier.UNRESOLVED):
            vs = [v for v in state.vendors.values() if nm.original.id in v.assessments and v.tier == tier]
            short = [v for v in vs if v.assessments[nm.original.id].shortlisted]
            counts: dict[str, int] = {}
            for v in vs:
                k = v.assessments[nm.original.id].match_class.value
                counts[k] = counts.get(k, 0) + 1
            status = "OK" if short else ("NO_VENDORS_FOUND" if not vs else "ONLY_UNVERIFIED_LEADS")
            if tier == Tier.UNRESOLVED and not vs:
                continue
            rows.append({"material_id": nm.original.id, "tier": tier.value, "found": len(vs), "shortlisted": len(short),
                         "by_match_class": counts, "status": status})
    return rows


def run_pipeline(req: ProcurementRequest, cfg: RunConfig, *, cache_dir: str | Path | None = None,
                 cache_mode: str = "auto", on_event: Callable[[dict[str, Any]], None] | None = None,
                 strict: bool | None = None) -> RunResult:
    ctx = RunContext(cfg, on_event=on_event)
    cache = Cache(cache_dir or ROOT / "data" / "cache", cache_mode)
    strict = cfg.strict if strict is None else strict

    # ---- 1. intake & normalisation
    ctx.stage("normalise")
    nms = normalise_request(req, cfg)
    crit = [{"material": nm.original.id, **f.model_dump(mode="json")} for nm in nms for f in nm.flags
            if f.severity == Severity.CRITICAL]
    if crit:
        ctx.log("normalise", "warn", f"{len(crit)} critical ambiguities - proceeding with logged assumptions" if not strict
                else f"{len(crit)} critical ambiguities - strict mode: stopping")
    if strict and crit:
        raise NeedsClarification(crit)

    state = State(nms)
    try:
        search = build_search_service(ctx, cache)
    except ProviderError as e:
        ctx.log("setup", "error", str(e))
        raise
    fetcher = Fetcher(ctx, cache)
    llm = build_llm(ctx, cache)
    agent_mode = bool(cfg.llm.agent.enabled)
    if agent_mode and not (llm.available and hasattr(llm, "chat")):
        ctx.log("setup", "warn", "agent mode requested but no tool-calling LLM is available (provider 'anthropic' has no agent adapter, "
                                 "or the key is missing) - falling back to the rule-driven workflow")
        agent_mode = False

    if agent_mode:
        # ---- 3+5 (agent mode): the model directs search / reading / evidence recording through gated tools
        discovery = run_agents(ctx, state, search, fetcher, llm)
        ctx.stage("resolve")
        n = dedupe(state, ctx)
        ctx.log("resolve", "info", f"{len(state.vendors)} distinct vendors after {n} duplicate merges")
        # Backstop: vendors the agent never gathered evidence for still get the deterministic page verification, so a weak
        # or rate-limited model can lower recall but never silently drop candidates. (No LLM calls in the backstop.)
        thin = {vid for vid in state.vendors if len(state.evidence_for(vid)) < 2}
        ctx.log("verify", "info", f"agent mode: rules backstop for {len(thin)} vendors with <2 agent-recorded evidence items")
        run_verification(ctx, state, fetcher, NullLLM(), only=thin)
        dedupe(state, ctx)
    else:
        # ---- 4. discovery (rule-driven loops)
        discovery = run_discovery(ctx, state, search, llm)
        # ---- 5. entity resolution
        ctx.stage("resolve")
        n = dedupe(state, ctx)
        ctx.log("resolve", "info", f"{len(state.vendors)} distinct vendors after {n} duplicate merges")
        # ---- 6. verification (fetch + evidence + evidence gate)
        run_verification(ctx, state, fetcher, llm)
        dedupe(state, ctx)   # second pass: phone numbers found on pages can reveal duplicates
    if ctx.budget.used.get("llm", 0) > 0 or (llm.available and cfg.llm.provider != "none"):
        llm_mode = f"{cfg.llm.provider}:{cfg.llm.strong_model}" + (" +agent" if agent_mode else "") \
                   + ("" if llm.available else " (disabled mid-run after an error)")
    elif cfg.llm.provider == "none":
        llm_mode = "rules-only"
    else:
        llm_mode = "rules-only (LLM unavailable)"

    # ---- 7. geography, 8. assessment
    ctx.stage("geography")
    for v in state.vendors.values():
        decide_geography(state, v, ctx)
    assess_all(state, ctx)

    ctx.stage("report")
    ev = sorted(state.evidence.values(), key=lambda e: e.id)
    cov = coverage_table(state, cfg)
    for row in cov:
        if row["status"] != "OK":
            ctx.log("coverage", "warn", f"{row['material_id']}/{row['tier']}: {row['status']} (found {row['found']})")
    cfg_json = json.dumps(cfg.model_dump(mode="json"), sort_keys=True)
    meta = {
        "generated_at": utcnow(),
        "procurement_location": cfg.procurement_location.model_dump(),
        "search_provider": cfg.search.provider,
        "llm_mode": llm_mode,
        "cache_mode": cache_mode,
        "cache_hits": cache.hits, "network_calls_for_uncached": cache.misses,
        "budget_used": ctx.budget.snapshot(),
        "config_hash": hashlib.sha256(cfg_json.encode()).hexdigest()[:12],
        "weights": cfg.weights,
        "strict": strict,
    }
    return RunResult(
        meta=meta, assumptions=collect_assumptions(nms, cfg), materials=nms,
        vendors=sorted(state.vendors.values(), key=lambda v: v.name.lower()), evidence=ev, coverage=cov,
        discovery=discovery, excluded_candidates=state.excluded, dropped_claims=state.dropped_claims,
        fetch_failures=state.fetch_failures, logs=ctx.logs)
