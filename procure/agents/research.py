"""Model-directed research agent (agent mode).

One agent per (material x geography). The MODEL decides the next action by calling tools:

    search_web / search_places  -> candidate vendors (registered with the same filters/dedupe as rules mode)
    read_page                   -> a compact digest of a page (key passages, contact links)
    record_evidence             -> adds a claim to the ledger *through the evidence gate* (verbatim quote or rejected)
    status / finish

What the model does NOT decide: whether a quote is admitted (the gate), where a vendor is (geography rules), how it
ranks (scoring). A rejected quote is returned to the model as feedback so it can retry with an exact copy; an invented
quote can never enter the ledger. Budgets (steps, searches, reads, global search quota) bound every loop.
"""
from __future__ import annotations

import itertools
import json
import threading
from dataclasses import dataclass, field
from typing import Any

from ..config import load_standards
from ..context import BudgetExceeded, RunContext
from ..fetch import Fetcher
from ..geo import registrable_domain
from ..llm import ChatResult, LLMError, NullLLM
from ..models import Evidence, NormalisedMaterial, Tier
from ..providers.search import SearchService
from ..signals import extract_evidence_rules, quote_in_text
from ..state import State
from .discovery import PLACES_QUERIES, discover_tier, drafts_from_results, register_drafts, tier_queries
from .verify import CLAIM_TYPES, source_kind

_ev_counter = itertools.count(1)
_ev_lock = threading.Lock()


def _tool(name: str, description: str, props: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {"type": "function", "function": {"name": name, "description": description,
                                             "parameters": {"type": "object", "properties": props, "required": required}}}


TOOLS = [
    _tool("search_web", "Web search. Returns candidate vendors (vendor_id, name, url, snippet). Costs one search from your budget "
                        "unless the same query was run before.",
          {"query": {"type": "string"}, "scope": {"type": "string", "enum": ["india", "global"],
                                                   "description": "india = Indian results, global = worldwide"}}, ["query", "scope"]),
    _tool("search_places", "Google-Maps style business search (address, phone, website). Best for local dealers/stockists. Costs one search.",
          {"query": {"type": "string"}}, ["query"]),
    _tool("read_page", "Fetch a page and return a compact digest: key passages (size/standard/wall/address/contact/capacity), "
                       "contact links. Quote evidence ONLY from text you have seen in a digest or search snippet.",
          {"url": {"type": "string"}}, ["url"]),
    _tool("record_evidence", "Record one fact about a vendor. `quote` MUST be copied verbatim (<=250 chars) from a read_page digest or a "
                             "search snippet of that exact `url`. Rejected if the quote is not found in that source.",
          {"vendor_id": {"type": "string"}, "url": {"type": "string"}, "claim_type": {"type": "string", "enum": CLAIM_TYPES},
           "quote": {"type": "string"}}, ["vendor_id", "url", "claim_type", "quote"]),
    _tool("status", "Show remaining budget and your candidates with how much evidence each has.", {}, []),
    _tool("finish", "End your research (when you have examined the promising vendors or are out of budget).",
          {"summary": {"type": "string"}}, ["summary"]),
]

TIER_BRIEF = {
    Tier.AHMEDABAD: ("Find vendors with an office, plant, warehouse or stock yard in AHMEDABAD (Gujarat) - dealers, stockists and mills. "
                     "Use search_places for local businesses and search_web with 'Ahmedabad'. Location evidence = a quote containing the address."),
    Tier.INDIA_OTHER: ("Find INDIAN vendors OUTSIDE Ahmedabad that could supply or deliver to Ahmedabad; prefer manufacturers (mills) because "
                       "the order is large. Record their address, any delivery / pan-India statement and BIS/ISI mention."),
    Tier.GLOBAL: ("Find NON-INDIAN manufacturers/exporters. They rarely cite IS 1239: search by OD x wall and international equivalents "
                  "(EN 10255 / BS 1387 / ASTM A53). Record address/country and any export-to-India, MOQ, lead-time or port statement exactly as written."),
}


def system_prompt(nm: NormalisedMaterial, tier: Tier, cfg, suggested: list[str]) -> str:
    r = nm.resolved
    flags = "; ".join(f"{f.code}: {f.assumption}" for f in nm.flags if f.assumption and f.code != "STANDARD_SCOPE_NOTE")
    a = cfg.llm.agent
    return (
        "You are a procurement research agent. Find real vendors for ONE requirement in ONE geography and record verbatim-quote "
        "evidence about them. A separate program ranks vendors; you only gather evidence.\n\n"
        f"REQUIREMENT {nm.original.id}: \"{nm.original.description_raw}\", {nm.quantity_tonnes:,.0f} t (unit assumed), to {nm.original.location_raw}.\n"
        f"Resolved: DN{r.dn}, OD {r.od_mm} mm, wall {r.wall_mm} mm, standard {r.standard}, series {r.class_meaning or 'n/a'}. "
        f"Ambiguities/assumptions: {flags or 'none'}. Search for BOTH the as-written reading and the alternates.\n\n"
        f"GEOGRAPHY: {TIER_BRIEF[tier]}\n\n"
        "WHAT TO RECORD per promising vendor (record_evidence, quote <=250 chars, copied EXACTLY, from the right url): "
        "(1) a passage showing the product: size / wall / standard / ERW (a table row is ideal); (2) an address quote; "
        "(3) a phone/email quote; (4) certification (BIS/ISI), capacity, stock, delivery or export statements if present.\n"
        "RULES: never invent or paraphrase a quote; do not record facts you did not see; prefer vendor-owned pages over marketplaces; "
        "if a page has no address, read its contact/about link; one vendor_id per company.\n"
        "EFFICIENCY: your step budget is small. In ONE turn you may call several tools at once (e.g. read_page for 3 urls, or "
        "several record_evidence calls) - batch them.\n"
        f"BUDGET: {a.max_steps} steps, {a.max_searches} searches, {a.max_reads} page reads. Suggested starting queries (already cached, free): "
        + " | ".join(suggested) + "\nStop with finish() once ~5 promising vendors have product + address evidence, or when the budget is nearly used."
    )


def compact(messages: list[dict[str, Any]], keep_last: int = 6) -> list[dict[str, Any]]:
    """Elide old tool outputs to stay inside small tokens-per-minute plans; `status` restores the candidate ledger."""
    cut = len(messages) - keep_last
    out = []
    for i, m in enumerate(messages):
        if m["role"] == "tool" and i < cut and len(m.get("content", "")) > 120:
            out.append({**m, "content": '{"elided":"older tool result omitted; call status() for your candidate list"}'})
        else:
            out.append(m)
    return out


@dataclass
class ResearchAgent:
    ctx: RunContext
    state: State
    search: SearchService
    fetcher: Fetcher
    llm: Any
    nm: NormalisedMaterial
    tier: Tier
    steps: int = 0
    searches: int = 0
    reads: int = 0
    accepted: int = 0
    rejected: int = 0
    finished: str | None = None
    queries: list[str] = field(default_factory=list)

    # ------------------------------------------------------------------ tool implementations
    @property
    def mid(self) -> str:
        return self.nm.original.id

    def _budget(self) -> dict[str, int]:
        a = self.ctx.cfg.llm.agent
        return {"steps_left": max(0, a.max_steps - self.steps), "searches_left": max(0, a.max_searches - self.searches),
                "reads_left": max(0, a.max_reads - self.reads)}

    def _entries(self, touched: list[str], query: str) -> list[dict[str, Any]]:
        out = []
        for vid in dict.fromkeys(touched):
            v = self.state.vendors[vid]
            hit = next((h for h in reversed(self.state.hits.get(vid, [])) if h.result.query == query), None) or self.state.hits[vid][-1]
            e = {"vendor_id": vid, "name": v.name[:60], "url": hit.result.url or v.contact.website}
            if hit.from_places:
                e.update(address=(hit.result.address or "")[:140], phone=hit.result.phone, website=hit.result.website)
            else:
                e["snippet"] = hit.result.snippet[:170]
            out.append(e)
        return out[:8]

    def search_web(self, query: str, scope: str = "india") -> dict[str, Any]:
        if self.searches >= self.ctx.cfg.llm.agent.max_searches:
            return {"error": "search budget for this agent is used up; use read_page / record_evidence / finish"}
        self.searches += 1
        self.queries.append(query)
        country = None if scope == "global" else self.ctx.cfg.search.country
        results = self.search.search(query, country=country, stage=f"agent:{self.mid}:{self.tier.value}")
        drafts = drafts_from_results(results, self.ctx.cfg, False, self.ctx, self.state, self.tier, self.mid)
        touched = register_drafts(drafts, self.state, self.tier, self.mid, self.ctx)
        return {"results": self._entries(touched, query), "filtered_out": len(results) - len(drafts)}

    def search_places(self, query: str) -> dict[str, Any]:
        if self.searches >= self.ctx.cfg.llm.agent.max_searches:
            return {"error": "search budget for this agent is used up"}
        self.searches += 1
        self.queries.append(query)
        results = self.search.places(query, country=self.ctx.cfg.search.country, stage=f"agent:{self.mid}:{self.tier.value}")
        drafts = drafts_from_results(results, self.ctx.cfg, True, self.ctx, self.state, self.tier, self.mid)
        touched = register_drafts(drafts, self.state, self.tier, self.mid, self.ctx)
        return {"results": self._entries(touched, query)}

    def read_page(self, url: str) -> dict[str, Any]:
        a = self.ctx.cfg.llm.agent
        if self.reads >= a.max_reads:
            return {"error": "page-read budget used up"}
        self.reads += 1
        page = self.fetcher.fetch(url)
        if not page.ok:
            self.state.fetch_failures.append({"vendor_id": "agent", "url": url, "error": page.error})
            return {"ok": False, "error": page.error}
        self.state.add_source_text(url, page.text)
        if page.url != url:
            self.state.add_source_text(page.url, page.text)
        kind = source_kind(url, False, self.ctx.cfg)
        items = extract_evidence_rules(page.text, url, "digest", kind, [self.nm])
        passages, used, seen = [], 0, set()
        for e in items:
            q = " ".join(e.quote.split())[:230]
            if q in seen:
                continue
            seen.add(q)
            if used + len(q) > a.digest_chars:
                break
            passages.append({"type": "/".join(e.claim_types[:2]), "text": q})
            used += len(q) + 20
        dom = registrable_domain(url)
        owner = next((vid for vid, v in self.state.vendors.items() if v.domain and v.domain == dom), None)
        return {"ok": True, "vendor_id": owner, "title": (page.title or "")[:90], "key_passages": passages,
                "contact_links": page.links[:3], "chars": len(page.text)}

    def record_evidence(self, vendor_id: str, url: str, claim_type: str, quote: str) -> dict[str, Any]:
        v = self.state.vendors.get(vendor_id)
        if v is None:
            return {"accepted": False, "reason": "unknown vendor_id - use an id returned by search_web / search_places"}
        if claim_type not in CLAIM_TYPES:
            return {"accepted": False, "reason": f"claim_type must be one of {CLAIM_TYPES}"}
        quote = " ".join(quote.split())[:300]
        key = " ".join(quote.lower().split())
        for e in self.state.evidence.values():           # same passage already recorded -> merge the claim type, don't double count
            if e.vendor_id == vendor_id and e.url == url and " ".join(e.quote.lower().split()) == key:
                if claim_type not in e.claim_types:
                    e.claim_types.append(claim_type)
                return {"accepted": True, "note": "already recorded; claim type added"}
        from_places = "google.com/maps" in url or any(h.from_places and h.result.url == url for h in self.state.hits.get(vendor_id, []))
        with _ev_lock:
            n = next(_ev_counter)
        ev = Evidence(id=f"{vendor_id}#A{n}", vendor_id=vendor_id, claim_type=claim_type, claim=f"agent-recorded {claim_type}",
                      quote=quote, url=url, source_kind=source_kind(url, from_places, self.ctx.cfg), material_ids=[self.mid])
        if self.state.gate(ev):
            self.accepted += 1
            if self.mid not in v.discovered_for:
                v.discovered_for.append(self.mid)
            if url not in v.source_urls:
                v.source_urls.append(url)
            return {"accepted": True}
        self.rejected += 1
        return {"accepted": False, "reason": "quote not found in the recorded text of that URL. Copy it EXACTLY from a read_page "
                                             "key_passages entry or a search snippet for the same url (or read the page first)."}

    def status(self) -> dict[str, Any]:
        rows = []
        for vid in self.state.found.get((self.mid, self.tier.value), ()):
            v = self.state.vendors.get(vid)
            if v is not None:
                evs = self.state.evidence_for(vid)
                rows.append({"vendor_id": vid, "name": v.name[:40], "evidence": len(evs),
                             "has_address": any("location" in e.claim_types for e in evs)})
        rows.sort(key=lambda r: -r["evidence"])
        return {"queries_run": self.queries, "candidates": rows[:12], "n_candidates": len(rows)}

    # ------------------------------------------------------------------ dispatch + loop
    def dispatch(self, name: str, args: dict[str, Any]) -> dict[str, Any]:
        try:
            if name == "search_web":
                return self.search_web(str(args.get("query", "")), str(args.get("scope", "india")))
            if name == "search_places":
                return self.search_places(str(args.get("query", "")))
            if name == "read_page":
                return self.read_page(str(args.get("url", "")))
            if name == "record_evidence":
                return self.record_evidence(str(args.get("vendor_id", "")), str(args.get("url", "")),
                                            str(args.get("claim_type", "")), str(args.get("quote", "")))
            if name == "status":
                return self.status()
            if name == "finish":
                self.finished = "model"
                return {"ok": True}
            return {"error": f"unknown tool {name!r}"}
        except BudgetExceeded as e:
            return {"error": f"global quota guard: {e}"}
        except TypeError as e:
            return {"error": f"bad arguments: {e}"}

    def run(self) -> dict[str, Any]:
        cfg = self.ctx.cfg
        a = cfg.llm.agent
        suggested = tier_queries(self.nm, self.tier, 1)[: max(1, a.max_searches - 1)]
        if self.tier == Tier.AHMEDABAD:
            suggested.append(PLACES_QUERIES[0] + " (search_places)")
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt(self.nm, self.tier, cfg, suggested)},
            {"role": "user", "content": "Begin. Call tools; finish() when done."}]
        nudged = False
        while self.steps < a.max_steps and not self.finished:
            self.steps += 1
            try:
                res: ChatResult = self.llm.chat(tier="strong", messages=compact(messages), tools=TOOLS,
                                                max_tokens=a.max_output_tokens, label=f"{self.mid}:{self.tier.value}:{self.steps}")
            except (LLMError, BudgetExceeded) as e:
                self.ctx.log("agent", "warn", f"{self.mid}/{self.tier.value}: model call failed at step {self.steps}: {e}")
                self.finished = "llm_error"
                break
            assistant: dict[str, Any] = {"role": "assistant", "content": res.content or ""}
            if res.tool_calls:
                assistant["tool_calls"] = []
                for t in res.tool_calls:
                    call = {"id": t.id, "type": "function", "function": {"name": t.name, "arguments": json.dumps(t.arguments)}}
                    if t.extra:                      # e.g. Gemini 3 thought_signature: required on the next request or it 400s
                        call["extra_content"] = t.extra
                    assistant["tool_calls"].append(call)
            messages.append(assistant)
            if not res.tool_calls:
                if nudged:
                    self.finished = "no_tool_call"
                    break
                nudged = True
                messages.append({"role": "user", "content": "Use the tools to continue, or call finish()."})
                continue
            for t in res.tool_calls:
                out = {"error": t.arguments_error} if t.arguments_error else self.dispatch(t.name, t.arguments)
                out["budget"] = self._budget()
                body = json.dumps(out, ensure_ascii=False)
                messages.append({"role": "tool", "tool_call_id": t.id, "content": body[:3000]})
                self.ctx.emit({"type": "agent_step", "material": self.mid, "tier": self.tier.value, "step": self.steps,
                               "tool": t.name, "args": {k: str(v)[:80] for k, v in t.arguments.items()}})
                if self.finished:
                    break
        if not self.finished:
            self.finished = "max_steps"
        summary = {"material": self.mid, "tier": self.tier.value, "steps": self.steps, "searches": self.searches,
                   "reads": self.reads, "evidence_accepted": self.accepted, "evidence_rejected": self.rejected,
                   "finished_by": self.finished, "queries": self.queries}
        self.ctx.log("agent", "info", f"{self.mid}/{self.tier.value}: {self.steps} steps, {self.searches} searches, {self.reads} reads, "
                                      f"{self.accepted} evidence accepted / {self.rejected} rejected by the gate ({self.finished})")
        return summary


def run_agents(ctx: RunContext, state: State, search: SearchService, fetcher: Fetcher, llm: Any) -> list[dict[str, Any]]:
    ctx.stage("discovery")
    summaries = []
    for nm in state.materials:
        for tier in (Tier.AHMEDABAD, Tier.INDIA_OTHER, Tier.GLOBAL):
            if not getattr(llm, "available", False):
                ctx.log("agent", "error", f"LLM unavailable - agent for {nm.original.id}/{tier.value} skipped "
                                          "(the rules backstop covers whatever candidates exist)")
                continue
            summary = ResearchAgent(ctx, state, search, fetcher, llm, nm, tier).run()
            # Recall floor: agent mode must never do WORSE than the workflow. If the agent produced too few candidates for this
            # geography (died early on a quota, wandered, or found little), the rule-driven discovery also runs for it
            # (its queries are mostly cached, so this is nearly free).
            have = len(state.found.get((nm.original.id, tier.value), ()))      # per (material, geography) pair
            floor = ctx.cfg.llm.agent.min_vendors_per_tier
            if have < floor:
                ctx.log("agent", "warn", f"{nm.original.id}/{tier.value}: agent surfaced only {have} candidates (<{floor}) - "
                                         "running the rule-driven discovery as a backstop for this geography")
                summary["rules_backstop"] = discover_tier(ctx, state, search, NullLLM(), nm, tier)["vendors_found"]
            ctx.emit({"type": "discovery", **summary})
            summaries.append(summary)
    return summaries
