"""Human-readable Markdown report. Designed to be read top-down:

  1. at-a-glance picks   2. ambiguities & assumptions   3. coverage   4. per-material vendor lists (3 tiers)
  5. not-located vendors  6. run log / failures / exclusions
"""
from __future__ import annotations

from .models import MatchClass, Provenance, Tier, Vendor
from .pipeline import RunResult

TIER_TITLES = {
    Tier.AHMEDABAD: "Ahmedabad vendors",
    Tier.INDIA_OTHER: "India-based vendors outside Ahmedabad",
    Tier.GLOBAL: "International / global vendors",
    Tier.UNRESOLVED: "Location not established",
}
TIERS = (Tier.AHMEDABAD, Tier.INDIA_OTHER, Tier.GLOBAL)


def _prov(p: Provenance) -> str:
    return f"[{p.value}]"


def _q(s: str, n: int = 200) -> str:
    s = " ".join(s.split())
    return (s[: n - 1] + "…") if len(s) > n else s


def _loc(v: Vendor) -> str:
    return ", ".join(x for x in (v.city, v.state, v.country) if x) or "unknown"


def _contact(v: Vendor) -> str:
    bits = ([v.contact.website] if v.contact.website else []) + v.contact.phones[:2] + v.contact.emails[:1]
    return "; ".join(bits) if bits else "none found in sources"


def _vendor_card(v: Vendor, mid: str, ev: dict) -> list[str]:
    a = v.assessments[mid]
    L = [f"#### {a.rank}. {v.name} — {a.match_class.value} · {a.confidence.value} confidence · score {a.score:.2f}",
         f"- **{v.vendor_type.value}** {_prov(v.vendor_type_prov)} · **{_loc(v)}** ({v.geo_status}: {_q(v.tier_reason, 150)})",
         f"- **Contact:** {_contact(v)}" + (f" · **Address:** {_q(v.contact.address, 120)}" if v.contact.address else ""),
         f"- **Match:** {'; '.join(a.match_reasons)}",
         f"- **Confidence:** {'; '.join(a.confidence_reasons)}",
         "- **Score:** " + ", ".join(f"{k.replace('_', ' ')} {x:.2f}" for k, x in a.score_breakdown.items()) + f" — {'; '.join(a.score_notes)}"]
    facts = []
    for key, label in (("standards", "Standards"), ("certifications", "Certs"), ("capacity", "Capacity"),
                       ("delivery", "Delivery"), ("export", "Export"), ("moq", "MOQ")):
        f = v.facts.get(key)
        if f and (f.provenance == Provenance.SOURCED or key in ("standards", "certifications", "capacity", "delivery")):
            facts.append(f"{label} {_prov(f.provenance)} {_q(f.value, 70)}")
    L.append("- **Facts:** " + " · ".join(facts) + " · Price/lead time [NEEDS_RFQ]")
    if a.bulk_feasibility:
        L.append(f"- **Bulk feasibility** {_prov(a.bulk_feasibility.provenance)}: {_q(a.bulk_feasibility.value, 260)}")
    if v.conflicts:
        L.append("- **Conflicts:** " + " | ".join(v.conflicts))
    if v.merged_from:
        L.append("- **Duplicates merged:** " + "; ".join(v.merged_from))
    used = [ev[i] for i in a.evidence_ids if i in ev]
    loc_ev = [ev[i] for i in (v.facts["location"].evidence_ids if v.facts.get("location") else []) if i in ev]
    shown = list({e.id: e for e in used + loc_ev}.values())[:4]
    if shown:
        L.append("- **Evidence:**")
        for e in shown:
            L.append(f"  - `{e.id}` ({'/'.join(e.claim_types[:3])}, {e.source_kind}) “{_q(e.quote, 170)}” — [source]({e.url})")
    else:
        L.append("- **Evidence:** none admitted by the evidence gate")
    L.append("- **Unresolved:** " + "; ".join(a.unresolved[:5]) + (f" (+{len(a.unresolved) - 5} more in JSON/CSV)" if len(a.unresolved) > 5 else ""))
    L.append(f"- **Next step:** {a.next_step}")
    L.append("")
    return L


def to_markdown(res: RunResult) -> str:
    ev = {e.id: e for e in res.evidence}
    m = res.meta
    L: list[str] = []
    L.append(f"# Procurement shortlist — {m['procurement_location']['city']}, {m['procurement_location']['state']}")
    L.append(f"_Generated {m['generated_at']} · search: {m['search_provider']} · LLM: {m['llm_mode']} · cache: {m['cache_mode']} · "
             f"config {m['config_hash']} · calls used: {m['budget_used']}_\n")
    L.append("> **How to read this.** Every vendor fact is labelled `[SOURCED]` (backed by a verbatim quote + URL), `[DERIVED]` (calculated), "
             "`[REFERENCE]` (BIS table), `[ASSUMED]` (an assumption you can override) or `[NEEDS_RFQ]` (must be confirmed with the vendor). "
             "Prices, lead times, stock and certifications are never stated unless quoted from a source "
             "(a quote may contain an indicative price the vendor published; that is **not** a verified quotation). "
             "**Match** says how well the evidence fits the requirement (EXACT / NEAR / CATEGORY / UNVERIFIED); "
             "**confidence** says how well-supported that assessment is (own-site evidence, verified location, reachable contact, no conflicts) — "
             "a NEAR match with HIGH confidence is a *well-evidenced near match*, not a perfect one.\n")

    # ------------------------------------------------------------ 1. at a glance
    L.append("## 1. At a glance — top picks per material and geography\n")
    L.append("| Material | " + " | ".join(TIER_TITLES[t] for t in TIERS) + " |\n|---|" + "---|" * len(TIERS))
    for nm in res.materials:
        mid = nm.original.id
        cells = []
        for t in TIERS:
            vs = sorted([v for v in res.vendors if v.tier == t and mid in v.assessments and v.assessments[mid].shortlisted],
                        key=lambda v: v.assessments[mid].rank or 99)[:3]
            cells.append("<br>".join(f"{v.assessments[mid].rank}. **{v.name[:34]}** — {v.assessments[mid].match_class.value}/"
                                     f"{v.assessments[mid].confidence.value}" for v in vs) or "_none found_")
        L.append(f"| **{mid}** {nm.original.description_raw[:46]} | " + " | ".join(cells) + " |")
    L.append("")

    # ------------------------------------------------------------ 2. ambiguities
    L.append("## 2. Requirement ambiguities and assumptions (read before sending any RFQ)\n")
    common = {}
    for nm in res.materials:
        for f in nm.flags:
            if f.severity.value == "INFO" and f.code == "STANDARD_SCOPE_NOTE":
                common.setdefault(f.code, f)
    for f in common.values():
        L.append(f"**Applies to all items — {f.code}:** {f.message} _Assumption {_prov(f.provenance)}: {f.assumption}_ "
                 f"_Ask for:_ {f.action}\n")
    for nm in res.materials:
        o = nm.original
        r = nm.resolved
        L.append(f"### {o.id} — `{o.description_raw}` · qty {o.quantity:g} {o.unit or '(no unit)'} · {o.location_raw}")
        L.append(f"- **Resolved for search** (original never overwritten): DN{r.dn or '?'}, OD {r.od_mm or '?'} mm "
                 f"{_prov(r.basis.get('od_mm', Provenance.ASSUMED))}, wall {r.wall_mm or '?'} mm {_prov(r.basis.get('wall_mm', Provenance.ASSUMED))}, "
                 f"standard {r.standard or 'not stated'}, series {r.class_meaning or 'n/a'}")
        d = nm.derived
        if d.kg_per_m:
            L.append(f"- **Derived** {_prov(d.provenance)}: {d.kg_per_m} kg/m ({d.kg_per_m_basis}); "
                     f"{nm.quantity_tonnes:,.0f} t ≈ {d.quantity_metres:,} m ≈ {d.approx_6m_lengths:,} × 6 m lengths")
        for f in nm.flags:
            if f.code == "STANDARD_SCOPE_NOTE":
                continue
            L.append(f"- **{f.severity.value} · {f.code}** — {f.message}")
            if f.candidates:
                L.append(f"  - Interpretations considered: {'; '.join(f.candidates)}")
            if f.assumption:
                L.append(f"  - Assumption used {_prov(f.provenance)}: {f.assumption}")
            if f.action:
                L.append(f"  - **Please confirm:** {f.action}")
        L.append("")

    # ------------------------------------------------------------ 3. coverage
    L.append("## 3. Coverage\n")
    L.append("| Material | Geography | Found | Shortlisted | By match class | Status |\n|---|---|---|---|---|---|")
    for c in res.coverage:
        L.append(f"| {c['material_id']} | {TIER_TITLES[Tier(c['tier'])]} | {c['found']} | {c['shortlisted']} | "
                 f"{', '.join(f'{k} {v}' for k, v in c['by_match_class'].items()) or '-'} | {c['status']} |")
    L.append("")

    # ------------------------------------------------------------ 4. per material
    for i, nm in enumerate(res.materials, start=4):
        mid = nm.original.id
        L.append(f"## {i}. {mid} — {nm.original.description_raw}\n")
        for tier in TIERS:
            vs = sorted([v for v in res.vendors if mid in v.assessments and v.tier == tier],
                        key=lambda v: v.assessments[mid].rank or 999)
            L.append(f"### {TIER_TITLES[tier]}\n")
            if not vs:
                L.append("_No vendors found for this geography (see coverage and run log)._\n")
                continue
            L.append("| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |\n|---|---|---|---|---|---|---|---|")
            for v in vs:
                a = v.assessments[mid]
                L.append(f"| {a.rank} | {v.name[:48]} | {v.vendor_type.value} | {', '.join(x for x in (v.city, v.country) if x) or '?'} "
                         f"({v.geo_status}) | {a.match_class.value} | {a.confidence.value} | {a.score:.2f} | {'yes' if a.shortlisted else 'no'} |")
            L.append("")
            for v in vs:
                if v.assessments[mid].shortlisted:
                    L += _vendor_card(v, mid, ev)
            rest = [v for v in vs if not v.assessments[mid].shortlisted]
            if rest:
                L.append("**Not shortlisted:** " + "; ".join(f"{v.name[:40]} — {v.assessments[mid].exclusion_reason}" for v in rest[:10])
                         + (f" (+{len(rest) - 10} more)" if len(rest) > 10 else "") + "\n")

    # ------------------------------------------------------------ 5. not located
    unl = [v for v in res.vendors if v.tier == Tier.UNRESOLVED]
    L.append(f"## {4 + len(res.materials)}. Leads whose location could not be established ({len(unl)})\n")
    L.append("These were surfaced by a search but no source quote gave an address (page blocked, JS-rendered, or not fetched within the "
             "verification budget). They are **not placed in any geography** — the 'surfaced by' column is only the search that found them, "
             "not their location. Verify the address before treating any as Ahmedabad / India / global.\n")
    L.append("| Vendor | Surfaced by | Site | Best match class | Why not located |\n|---|---|---|---|---|")
    def best(v: Vendor) -> int:
        order = {MatchClass.EXACT: 0, MatchClass.NEAR: 1, MatchClass.CATEGORY: 2, MatchClass.UNVERIFIED: 3}
        return min((order[a.match_class] for a in v.assessments.values()), default=4)
    for v in sorted(unl, key=lambda v: (best(v), v.name.lower()))[:60]:
        bm = min(v.assessments.values(), key=lambda a: {"EXACT": 0, "NEAR": 1, "CATEGORY": 2, "UNVERIFIED": 3}[a.match_class.value]).match_class.value if v.assessments else "-"
        L.append(f"| {v.name[:44]} | {', '.join(t.lower() for t in v.found_via)} | {v.contact.website or v.id[:30]} | {bm} | {_q(v.tier_reason, 70)} |")
    L.append("")

    # ------------------------------------------------------------ 6. log
    L.append("## Run log, failures and exclusions\n")
    L.append(f"- **Page fetch failures:** {len(res.fetch_failures)}" + "".join(
        f"\n  - {f['url'][:100]} — {f['error']}" for f in res.fetch_failures[:12])
        + ("\n  - … (full list in result.json)" if len(res.fetch_failures) > 12 else ""))
    L.append(f"- **Claims dropped by the evidence gate:** {len(res.dropped_claims)}" + "".join(
        f"\n  - {d['vendor_id']}: “{d['quote']}” ({d['reason']})" for d in res.dropped_claims[:10]))
    ex = {}
    for x in res.excluded_candidates:
        ex.setdefault(x["reason"], []).append(x)
    L.append(f"- **Search results excluded before becoming vendors:** {len(res.excluded_candidates)}")
    for reason, items in ex.items():
        L.append(f"  - {reason} — {len(items)}: " + "; ".join(sorted({(i['title'] or i['url'])[:40] for i in items})[:4]))
    errs = [lg for lg in res.logs if lg.level in ("warn", "error") and not lg.message.startswith("fetch failed")]
    L.append(f"- **Warnings / errors:** {len(errs)}" + "".join(f"\n  - [{lg.stage}] {lg.message[:160]}" for lg in errs[:20]))
    L.append("\n## Assumptions in force\n")
    L += [f"- {a}" for a in res.assumptions]
    return "\n".join(L) + "\n"
