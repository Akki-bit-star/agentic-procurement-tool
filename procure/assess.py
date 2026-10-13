"""Stage 8 - technical match, scoring, confidence, bulk feasibility, next steps (deterministic).

Everything here is derived from QUOTE-BACKED signals (signals.py). Nothing is read from a model's opinion,
so the same evidence always produces the same ranking, and every number can be traced to a rule below.
"""
from __future__ import annotations

import re
from collections import defaultdict

from .context import RunContext
from .geo import registrable_domain
from .models import (Confidence, Fact, MatchClass, MaterialAssessment, NormalisedMaterial, Provenance, Tier,
                     Vendor, VendorType)
from .signals import (RE_EMAIL, RE_PHONE, RE_STD, MaterialSignals, ReqPatterns, VendorSignals, analyze_text,
                      analyze_vendor_text, build_patterns, norm_standard)
from .state import State

SPEC_TYPES = {"product_match", "standard", "wall", "class"}


# --------------------------------------------------------------------------- vendor-level facts
def build_vendor_facts(state: State, v: Vendor, ctx: RunContext) -> VendorSignals:
    """Aggregate vendor-level facts from evidence quotes. Each fact keeps the ids of the quotes behind it."""
    agg = VendorSignals()
    ids: dict[str, list[str]] = defaultdict(list)
    stds: dict[str, list[str]] = defaultdict(list)
    evs = state.evidence_for(v.id)
    for e in evs:
        s = analyze_vendor_text(e.quote)
        for c in s.certs:
            agg.certs.add(c)
            ids["cert:" + c].append(e.id)
        if s.capacity and not agg.capacity:
            agg.capacity = s.capacity
            ids["capacity"].append(e.id)
        for key in ("stock", "manufacturer", "platform", "trader", "stockist", "delivery", "delivery_india_wide",
                    "delivery_ahmedabad_or_gujarat", "export", "export_india"):
            if getattr(s, key):
                setattr(agg, key, True)
                ids[key].append(e.id)
        if s.moq and not agg.moq:
            agg.moq = s.moq
            ids["moq"].append(e.id)
        for m in RE_STD.finditer(e.quote):
            stds[norm_standard(m)].append(e.id)
        for p in s.phones:
            if p not in agg.phones:
                agg.phones.append(p)
        for em in s.emails:
            if em not in agg.emails:
                agg.emails.append(em)

    def fact(key: str, value: str, ev_ids: list[str]) -> None:
        v.facts[key] = Fact(value=value, provenance=Provenance.SOURCED, evidence_ids=list(dict.fromkeys(ev_ids)))

    def missing(key: str, what: str) -> None:
        v.facts[key] = Fact(value=f"not found in sources - {what}", provenance=Provenance.NEEDS_RFQ)

    if stds:
        fact("standards", ", ".join(sorted(stds)), [i for x in stds.values() for i in x])
    else:
        missing("standards", "ask for the standard and BIS licence")
    if agg.certs:
        label = {"BIS/ISI": "BIS / ISI mark", "ISO": "ISO management-system certificate", "TEST_CERT": "test / inspection certificate"}
        fact("certifications", ", ".join(label[c] for c in sorted(agg.certs)) + " (mentioned; certificate numbers not verified)",
             [i for c in agg.certs for i in ids["cert:" + c]])
    else:
        missing("certifications", "request BIS licence number and mill test certificate")
    fact("capacity", agg.capacity, ids["capacity"]) if agg.capacity else missing("capacity", "ask for monthly capacity / stock at RFQ")
    if agg.stock:
        fact("stock", "stock / warehouse mentioned (quantity not stated)", ids["stock"])
    if agg.delivery:
        scope = ("Ahmedabad/Gujarat delivery stated" if agg.delivery_ahmedabad_or_gujarat
                 else "pan-India delivery stated" if agg.delivery_india_wide else "delivery mentioned (area not specific)")
        fact("delivery", scope, ids["delivery"] + ids["delivery_ahmedabad_or_gujarat"] + ids["delivery_india_wide"])
    else:
        missing("delivery", "confirm delivery to Ahmedabad and freight terms")
    if agg.export:
        fact("export", "export / overseas supply mentioned" + (" (India mentioned)" if agg.export_india else ""),
             ids["export"] + ids["export_india"])
    if agg.moq:
        fact("moq", agg.moq, ids["moq"])
    v.facts["price"] = Fact(value="not collected - request quotation", provenance=Provenance.NEEDS_RFQ)
    v.facts["lead_time"] = Fact(value="not collected - request quotation", provenance=Provenance.NEEDS_RFQ)

    # vendor type: only from quoted wording; marketplace-only vendors stay MARKETPLACE_LISTING unless a quote says otherwise
    if agg.platform and not agg.manufacturer:
        v.vendor_type, v.vendor_type_prov = VendorType.MARKETPLACE_LISTING, Provenance.SOURCED
        v.facts["vendor_type"] = Fact(value="aggregator / price-information site (not a producer or stockist itself)",
                                      provenance=Provenance.SOURCED, evidence_ids=ids["platform"][:3])
    elif agg.manufacturer:
        v.vendor_type, v.vendor_type_prov = VendorType.MANUFACTURER, Provenance.SOURCED
        v.facts["vendor_type"] = Fact(value="MANUFACTURER (self-declared on the source)", provenance=Provenance.SOURCED,
                                      evidence_ids=ids["manufacturer"][:3])
    elif agg.stockist:
        v.vendor_type, v.vendor_type_prov = VendorType.STOCKIST, Provenance.SOURCED
        v.facts["vendor_type"] = Fact(value="STOCKIST / dealer (self-declared)", provenance=Provenance.SOURCED,
                                      evidence_ids=ids["stockist"][:3])
    elif agg.trader:
        v.vendor_type, v.vendor_type_prov = VendorType.TRADER, Provenance.SOURCED
        v.facts["vendor_type"] = Fact(value="TRADER / supplier (self-declared)", provenance=Provenance.SOURCED,
                                      evidence_ids=ids["trader"][:3])
    # contacts - website is the vendor domain; phones/emails only if quoted
    if v.domain and not v.contact.website:
        v.contact.website = f"https://{v.domain}"
    for p in agg.phones:
        if p not in v.contact.phones:
            v.contact.phones.append(p)
    for em in agg.emails:
        if em not in v.contact.emails:
            v.contact.emails.append(em)
    v.contact.phones, v.contact.emails = v.contact.phones[:4], v.contact.emails[:3]
    return agg


# --------------------------------------------------------------------------- technical match
def classify_match(evs, nm: NormalisedMaterial, pat: ReqPatterns) -> tuple[MatchClass, list[str], list[str], MaterialSignals]:
    """Returns (class, reasons, evidence_ids used, merged signals)."""
    r = nm.resolved
    per = [(e, analyze_text(e.quote, pat)) for e in evs]
    merged = MaterialSignals()
    for _, s in per:
        merged.erw |= s.erw
        merged.standards |= s.standards
        merged.size_strong |= s.size_strong
        merged.size_weak |= s.size_weak
        merged.size_range |= s.size_range
        merged.od_hit |= s.od_hit
        merged.walls_hit.update(s.walls_hit)
        merged.class_letters |= s.class_letters
        merged.class_words |= s.class_words
    used: list[str] = []
    reasons: list[str] = []
    wants_is1239 = bool(r.standard and r.standard.startswith("IS 1239"))
    has_is1239 = "IS 1239" in merged.standards
    other_stds = sorted(s for s in merged.standards if s != "IS 1239")
    primary_wall = r.wall_mm
    series_ok = ((r.class_meaning and r.class_meaning in merged.class_words)
                 or (nm.spec.pipe_class and nm.spec.pipe_class in merged.class_letters))

    def ids_for(pred) -> list[str]:
        return [e.id for e, s in per if pred(s)]

    # a "row" = size and the required wall (or the required series) inside ONE quote, e.g. a table row
    row_hit_ids = []
    std_urls = {e.url for e, s in per if "IS 1239" in s.standards}      # pages that state IS 1239 somewhere
    erw_urls = {e.url for e, s in per if s.erw}                          # pages that state the ERW process
    wants_erw = nm.spec.process == "ERW"
    conflicting_rows = 0
    process_gap = 0
    for e, s in per:
        size_here = s.size_strong or (s.od_hit and (s.erw or s.standards))
        wall_here = primary_wall in s.walls_hit if primary_wall else False
        series_here = bool(r.class_meaning and r.class_meaning in s.class_words) or bool(
            nm.spec.pipe_class and nm.spec.pipe_class in s.class_letters)
        if size_here and (wall_here or (not nm.spec.wall_mm and series_here) or (series_here and r.basis.get("wall_mm") == Provenance.REFERENCE)):
            # the row must not be attributed to a DIFFERENT standard (e.g. "48.3 x 3.2 mm, medium class, IS 1161"),
            # and the required standard must be stated on the same page
            if wants_is1239 and (s.standards - {"IS 1239"} or e.url not in std_urls):
                conflicting_rows += 1
                continue
            # the manufacturing process must match too: a 'seamless' listing is not an ERW listing, and a page that never
            # says ERW does not show the product is ERW (IS 1239 permits seamless and welded)
            if wants_erw and ((re.search(r"seamless", e.quote, re.I) and not s.erw) or e.url not in erw_urls):
                process_gap += 1
                continue
            row_hit_ids.append(e.id)
    product_cat = merged.erw or bool(merged.standards) or merged.size_strong or merged.od_hit
    size_ok = merged.size_strong or (merged.od_hit and (merged.erw or bool(merged.standards)))

    if product_cat and size_ok and (has_is1239 or not wants_is1239) and row_hit_ids:
        used = row_hit_ids + ids_for(lambda s: any(x == "IS 1239" for x in s.standards))
        reasons.append(f"Size and required wall/series appear together in one source quote ({', '.join(row_hit_ids[:2])})")
        if has_is1239:
            reasons.append("IS 1239 stated")
        return MatchClass.EXACT, reasons, used, merged

    if product_cat and (size_ok or merged.size_range or merged.size_weak):
        why = []
        if size_ok:
            used += ids_for(lambda s: s.size_strong or s.od_hit)
            why.append(f"DN{r.dn} / OD size stated")
        elif merged.size_range:
            used += ids_for(lambda s: s.size_range)
            why.append(f"a size range covering DN{r.dn} is listed, but not this exact product")
        else:
            used += ids_for(lambda s: s.size_weak)
            why.append(f"'{r.dn} mm' mentioned (nominal bore vs OD not stated)")
        if has_is1239:
            used += ids_for(lambda s: "IS 1239" in s.standards)
            why.append("IS 1239 stated")
        elif other_stds:
            used += ids_for(lambda s: bool(s.standards))
            why.append(f"standard stated is {', '.join(other_stds)}, not IS 1239")
        else:
            why.append("no standard stated")
        if primary_wall and primary_wall in merged.walls_hit:
            used += ids_for(lambda s: primary_wall in s.walls_hit)
            why.append(f"{primary_wall:g} mm wall mentioned but not tied to this size in one quote")
        else:
            alt = [w for w in merged.walls_hit if w != primary_wall]
            if alt:
                used += ids_for(lambda s: any(w in s.walls_hit for w in alt))
                why.append("only the nearest IS 1239 wall (" + ", ".join(f"{w:g} mm" for w in alt) + ") is listed, not the required one")
            elif primary_wall:
                why.append(f"required wall {primary_wall:g} mm not confirmed")
        if series_ok:
            why.append(f"series '{r.class_meaning or nm.spec.pipe_class}' mentioned")
        if conflicting_rows:
            why.append("the matching size/wall row is attributed to a different standard (not IS 1239), so it cannot be treated as an exact match")
            used += [e.id for e, s in per if (s.size_strong or s.od_hit) and (s.standards - {"IS 1239"})]
        if process_gap:
            why.append("the matching row is a seamless listing or the page never states ERW, so the ERW process is not confirmed")
            used += [e.id for e, s in per if (s.size_strong or s.od_hit)][:2]
        return MatchClass.NEAR, why, list(dict.fromkeys(used)), merged

    if product_cat:
        used = ids_for(lambda s: s.erw or bool(s.standards))
        what = "ERW pipe supply" if merged.erw else "steel pipe standard"
        return MatchClass.CATEGORY, [f"{what} mentioned; no size evidence for DN{r.dn or '?'}"], used, merged

    return MatchClass.UNVERIFIED, ["no quote showing a matching product, size or standard"], [], merged


# --------------------------------------------------------------------------- scoring
def bulk_profile(v: Vendor, agg: VendorSignals) -> str:
    if v.vendor_type == VendorType.MANUFACTURER:
        return "manufacturer_with_capacity" if agg.capacity else "manufacturer"
    if v.vendor_type == VendorType.STOCKIST:
        return "stockist_with_stock" if agg.stock else "stockist"
    if v.vendor_type == VendorType.TRADER:
        return "trader"
    if v.vendor_type == VendorType.MARKETPLACE_LISTING:
        return "marketplace_listing"
    return "unknown"


def geography_component(v: Vendor, agg: VendorSignals) -> tuple[float, str]:
    if v.tier == Tier.AHMEDABAD:
        return (1.0, "Ahmedabad presence verified") if v.geo_status == "VERIFIED" else (0.6, "Ahmedabad only claimed by a marketplace")
    if v.tier == Tier.INDIA_OTHER:
        if agg.delivery_ahmedabad_or_gujarat:
            base, why = 0.9, "delivery to Ahmedabad/Gujarat stated"
        elif v.state == "Gujarat":
            base, why = 0.8, "based in Gujarat (nearby), delivery not confirmed"
        elif agg.delivery_india_wide:
            base, why = 0.7, "pan-India delivery stated"
        else:
            base, why = 0.4, "India-based; delivery to Ahmedabad plausible but unconfirmed"
        return (base if v.geo_status == "VERIFIED" else base * 0.8), why
    if v.tier == Tier.GLOBAL:
        if agg.export_india:
            return 0.7, "export to India mentioned"
        if agg.export:
            return 0.45, "export mentioned (India not named)"
        return 0.15, "no export evidence"
    return 0.0, "location unresolved"


def certification_component(agg: VendorSignals, v: Vendor, merged: MaterialSignals) -> float:
    s = 0.0
    if "BIS/ISI" in agg.certs:
        s = 1.0
    if "TEST_CERT" in agg.certs:
        s = max(s, 0.6)
    if "ISO" in agg.certs:
        s = max(s, 0.5)
    if s == 0 and v.tier == Tier.GLOBAL and merged.standards:
        s = 0.4   # international standard named (EN/ASTM/BS) but no certification evidence
    return s


def assess_vendor_material(state: State, ctx: RunContext, v: Vendor, nm: NormalisedMaterial,
                           agg: VendorSignals) -> MaterialAssessment:
    cfg = ctx.cfg
    pat = build_patterns(nm)
    evs = state.evidence_for(v.id, nm.original.id)
    mclass, reasons, used, merged = classify_match(evs, nm, pat)
    a = MaterialAssessment(material_id=nm.original.id, match_class=mclass, match_reasons=reasons, evidence_ids=used)

    solid_spec = [e for e in evs if e.source_kind in ("vendor_site", "maps") and e.id in used]
    # independence: distinct KINDS of fact (standard / size / wall / series) found in the vendor's own sources.
    # Counting quotes would let one passage vouch for itself several times.
    kinds: set[str] = set()
    for e in solid_spec:
        s = analyze_text(e.quote, pat)
        if s.standards:
            kinds.add("standard")
        if s.size_strong or s.od_hit:
            kinds.add("size")
        if s.walls_hit:
            kinds.add("wall")
        if s.class_words or s.class_letters:
            kinds.add("series")
    n_urls = len({e.url for e in solid_spec})
    # EXACT already required size+wall/series+standard together, so two kinds/pages suffice; a NEAR match is only
    # HIGH-confidence when the vendor's own sources independently evidence three kinds of fact (e.g. standard + size + series),
    # or two kinds across two pages.
    if mclass == MatchClass.EXACT:
        independent = len(kinds) >= 2 or n_urls >= 2
    else:
        independent = len(kinds) >= 3 or (len(kinds) >= 2 and n_urls >= 2)

    # ---- component scores (0..1)
    tech = cfg.match_score[mclass.value]
    profile = bulk_profile(v, agg)
    bulk = cfg.bulk_scores.get(profile, 0.2)
    big = (nm.quantity_tonnes or 0) >= cfg.large_order_tonnes
    if big and profile in ("stockist_with_stock", "stockist", "trader", "marketplace_listing"):
        bulk *= 0.75     # mill-direct is the realistic route at this tonnage
    geo, geo_why = geography_component(v, agg)
    cert = certification_component(agg, v, merged)
    rel = cfg.source_reliability
    srcq = max((rel.get(e.source_kind, rel.get("unknown", 0.2)) for e in evs), default=0.0)
    if len({registrable_domain(e.url) for e in evs}) >= 2:
        srcq = min(1.0, srcq + 0.2)          # corroboration by an independent domain
    has_site = bool(v.contact.website)
    has_reach = bool(v.contact.phones or v.contact.emails)
    contact = 1.0 if (has_site and has_reach) else 0.5 if (has_site or has_reach) else 0.0
    comps = {"technical_match": tech, "bulk_relevance": bulk, "geography_delivery": geo,
             "certification": cert, "source_quality": srcq, "contactability": contact}
    a.score_breakdown = {k: round(x, 3) for k, x in comps.items()}
    a.score = round(sum(cfg.weights[k] * x for k, x in comps.items()), 4)

    # ---- confidence
    reasons_c: list[str] = []
    conf = Confidence.LOW
    strong_match = mclass in (MatchClass.EXACT, MatchClass.NEAR)
    reachable = bool(v.contact.phones or v.contact.emails)
    if strong_match and independent and v.geo_status == "VERIFIED" and not v.conflicts and reachable:
        conf = Confidence.HIGH
        reasons_c.append(f"vendor's own site/maps evidences {', '.join(sorted(kinds)) or 'the match'} "
                         f"({len(solid_spec)} quote(s), {n_urls} page(s)); location verified; no conflicts; phone/email found")
    elif strong_match and v.geo_status in ("VERIFIED", "CLAIMED"):
        conf = Confidence.MEDIUM
        if not solid_spec:
            reasons_c.append("match rests on marketplace / search-snippet text only")
        elif not independent:
            reasons_c.append("own-source support is thin: " + (", ".join(sorted(kinds)) or "no fact kinds") +
                             f" on {n_urls} page(s) (NEAR needs 3 kinds, or 2 kinds on 2 pages, for HIGH)")
        if solid_spec and independent and not reachable:
            reasons_c.append("no phone or email found in any source, so the vendor cannot yet be contacted from this output")
        if v.geo_status != "VERIFIED":
            reasons_c.append("location is only claimed, not verified")
        if v.conflicts:
            reasons_c.append("conflicting information was found (see conflicts)")
    elif mclass == MatchClass.CATEGORY and v.geo_status == "VERIFIED" and solid_spec and not v.conflicts:
        conf = Confidence.MEDIUM
        reasons_c.append("category-level only: supplies ERW/steel pipe but no size evidence")
    else:
        reasons_c.append({MatchClass.UNVERIFIED: "no spec evidence found", MatchClass.CATEGORY: "category-level lead only",
                          MatchClass.NEAR: "near match without a verified location", MatchClass.EXACT: "exact match without a verified location"}[mclass])
    a.confidence, a.confidence_reasons = conf, reasons_c
    a.score_notes = [f"geography/delivery: {geo_why}", f"bulk relevance: {profile.replace('_', ' ')}"
                     + (" (x0.75: large order, mill-direct realistic)" if big and profile in (
                         "stockist_with_stock", "stockist", "trader", "marketplace_listing") else "")]

    # ---- bulk feasibility (inference, labelled)
    qty = nm.quantity_tonnes
    req = (f"required {qty:,.0f} t" + (f" (~{nm.derived.quantity_metres:,} m)" if nm.derived.quantity_metres else "")
           + (" - unit ASSUMED to be tonnes" if nm.unit_assumed else ""))
    cap_ids = v.facts["capacity"].evidence_ids if v.facts.get("capacity") and v.facts["capacity"].provenance == Provenance.SOURCED else []
    prof_label = {"manufacturer_with_capacity": "manufacturer with a stated capacity", "manufacturer": "manufacturer (self-declared), capacity not stated",
                  "stockist_with_stock": "stockist/dealer mentioning stock", "stockist": "stockist/dealer, stock not stated",
                  "trader": "trader/supplier", "marketplace_listing": "marketplace listing only", "unknown": "business type not established"}[profile]
    note = f"{prof_label}; {req}."
    if big and profile in ("stockist_with_stock", "stockist", "trader", "marketplace_listing"):
        note += " At this tonnage a mill-direct or large-stock source is more realistic."
    note += " Monthly capacity, ready stock and lead time must be confirmed by RFQ."
    a.bulk_feasibility = Fact(value=note, provenance=Provenance.SOURCED if cap_ids else Provenance.NEEDS_RFQ, evidence_ids=cap_ids)

    # ---- unresolved + next step
    un: list[str] = []
    for f in nm.flags:
        if f.severity.value in ("CRITICAL", "WARNING") and f.code in ("WALL_NOT_IN_STANDARD", "SIZE_BARE_MM", "CLASS_MEANING"):
            un.append(f"requirement ambiguity {f.code}: {f.action or f.message}")
    if mclass != MatchClass.EXACT:
        un.append("exact product (size + wall + standard in one specification) not confirmed by a source")
    if "BIS/ISI" not in agg.certs:
        un.append("BIS licence / ISI mark not evidenced")
    if v.vendor_type_prov == Provenance.SOURCED and v.vendor_type in (VendorType.MANUFACTURER,):
        un.append("manufacturer status is self-declared - verify via BIS licence / plant details")
    if not cap_ids:
        un.append("capacity / ready stock not stated")
    un.append("price, lead time and MOQ require an RFQ")
    if v.geo_status != "VERIFIED":
        un.append(f"location {v.geo_status.lower()} - confirm the address")
    if v.conflicts:
        un.extend(f"conflict: {c}" for c in v.conflicts)
    if v.tier == Tier.GLOBAL:
        un.extend(f"import check: {c}" for c in cfg.global_import_checks)
    a.unresolved = un

    pieces = {
        MatchClass.EXACT: f"Issue an RFQ for {qty:,.0f} t of {nm.original.description_raw}: request price, MOQ, lead time, delivery to Ahmedabad, BIS licence no. and mill test certificate.",
        MatchClass.NEAR: "Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.",
        MatchClass.CATEGORY: f"Request their product list / catalogue for DN{nm.resolved.dn or '?'} and the BIS licence before any RFQ.",
        MatchClass.UNVERIFIED: "Verify the vendor exists and supplies ERW pipe (website / phone check) before spending effort; not shortlisted.",
    }
    step = pieces[mclass]
    if v.tier == Tier.GLOBAL:
        step += " Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first."
    if v.tier == Tier.INDIA_OTHER:
        step += " Ask for freight cost and transit time to Ahmedabad."
    a.next_step = step
    return a


# --------------------------------------------------------------------------- ranking + shortlist
def assess_all(state: State, ctx: RunContext) -> None:
    ctx.stage("assessment")
    cfg = ctx.cfg
    for v in state.vendors.values():
        agg = build_vendor_facts(state, v, ctx)
        for nm in state.materials:
            a = assess_vendor_material(state, ctx, v, nm, agg)
            # a vendor only appears under a material it was discovered for, or if its evidence matches that material
            if nm.original.id in v.discovered_for or a.match_class in (MatchClass.EXACT, MatchClass.NEAR):
                v.assessments[nm.original.id] = a

    for nm in state.materials:
        mid = nm.original.id
        groups: dict[Tier, list[Vendor]] = defaultdict(list)
        for v in state.vendors.values():
            if mid in v.assessments:
                groups[v.tier].append(v)
        for tier, vs in groups.items():
            vs.sort(key=lambda x: (-x.assessments[mid].score, x.name.lower()))
            n_short = 0
            for i, v in enumerate(vs, start=1):
                a = v.assessments[mid]
                a.rank = i
                if tier == Tier.UNRESOLVED:
                    a.exclusion_reason = "location could not be determined from any source - cannot be placed in a geographic group"
                elif a.match_class == MatchClass.UNVERIFIED:
                    a.exclusion_reason = "unverified lead: no quote shows a matching product - listed for follow-up, not shortlisted"
                elif n_short >= cfg.shortlist.per_tier_per_material:
                    a.exclusion_reason = f"ranked below the top {cfg.shortlist.per_tier_per_material} for this tier (score {a.score:.2f})"
                else:
                    a.shortlisted = True
                    n_short += 1
