"""Stage 5/7 - entity resolution (dedupe) and geography decision. Deterministic and fully logged."""
from __future__ import annotations

import re
from dataclasses import dataclass

from rapidfuzz import fuzz

from .context import RunContext
from .geo import Place, find_places, tld_country, tier_from_place
from .models import Fact, Provenance, Tier, Vendor, VendorType
from .signals import RE_PHONE
from .state import State

_LEGAL = re.compile(r"\b(pvt|private|ltd|limited|llp|inc|co|company|corp|corporation|pte|llc|gmbh|sa|bv)\b\.?", re.I)


def norm_name(name: str) -> str:
    n = _LEGAL.sub(" ", name.lower())
    n = re.sub(r"[^a-z0-9 ]+", " ", n)
    return re.sub(r"\s+", " ", n).strip()


def phone_keys(v: Vendor) -> set[str]:
    return {re.sub(r"\D", "", p)[-10:] for p in v.contact.phones if len(re.sub(r"\D", "", p)) >= 10}


# --------------------------------------------------------------------------- dedupe
def merge(state: State, ctx: RunContext, keep: str, drop: str, reason: str) -> None:
    a, b = state.vendors[keep], state.vendors.pop(drop)
    a.merged_from.append(f"{b.name} ({drop})")
    if b.name != a.name and b.name not in a.aliases:
        a.aliases.append(b.name)
    for m in b.discovered_for:
        if m not in a.discovered_for:
            a.discovered_for.append(m)
    a.found_via = list(dict.fromkeys(a.found_via + b.found_via))
    for ids in state.found.values():                 # keep per-(material, geography) coverage pointing at the surviving record
        if drop in ids:
            ids.discard(drop)
            ids.add(keep)
    for u in b.source_urls:
        if u not in a.source_urls:
            a.source_urls.append(u)
    c, bc = a.contact, b.contact
    c.website = c.website or bc.website
    c.address = c.address or bc.address
    c.phones = list(dict.fromkeys(c.phones + bc.phones))
    c.emails = list(dict.fromkeys(c.emails + bc.emails))
    if a.vendor_type in (VendorType.UNKNOWN, VendorType.MARKETPLACE_LISTING) and b.vendor_type not in (VendorType.UNKNOWN, VendorType.MARKETPLACE_LISTING):
        a.vendor_type = b.vendor_type
    for h in state.hits.pop(drop, []):
        state.hits.setdefault(keep, []).append(h)
    for e in state.evidence.values():
        if e.vendor_id == drop:
            e.vendor_id = keep
    ctx.log("resolve", "info", f"merged duplicate '{b.name}' into '{a.name}': {reason}")


def dedupe(state: State, ctx: RunContext) -> int:
    merges = 0
    changed = True
    while changed:
        changed = False
        ids = list(state.vendors)
        for i, ia in enumerate(ids):
            for ib in ids[i + 1:]:
                if ia not in state.vendors or ib not in state.vendors:
                    continue
                a, b = state.vendors[ia], state.vendors[ib]
                if a.name.startswith("[") or b.name.startswith("["):   # unnamed marketplace listings are never fuzzy-merged
                    continue
                reason = None
                if phone_keys(a) & phone_keys(b):
                    reason = "same phone number"
                else:
                    score = fuzz.token_sort_ratio(norm_name(a.name), norm_name(b.name))
                    if score >= 95 and norm_name(a.name):
                        reason = f"name similarity {score:.0f}%"
                if reason:
                    # prefer the vendor-owned domain as the canonical record
                    keep, drop = (ia, ib) if (a.domain or not b.domain) else (ib, ia)
                    merge(state, ctx, keep, drop, reason)
                    merges += 1
                    changed = True
    return merges


# --------------------------------------------------------------------------- geography
@dataclass
class GeoEntry:
    place: Place
    reliability: float
    kind: str                 # maps | vendor_site | marketplace
    evidence_id: str | None
    quote: str


def collect_geo(state: State, v: Vendor, ctx: RunContext) -> list[GeoEntry]:
    rel = ctx.cfg.source_reliability
    out: list[GeoEntry] = []
    for e in state.evidence_for(v.id):
        for pl in find_places(e.quote):
            if not (pl.city or pl.state or pl.country):
                continue
            if e.source_kind == "marketplace":
                ok = pl.locative or pl.in_address_context          # "ships to UAE" is not "is in UAE"
            else:
                ok = "location" in e.claim_types or pl.in_address_context or pl.facility
            if ok:
                out.append(GeoEntry(pl, rel.get(e.source_kind, 0.3), e.source_kind, e.id, e.quote))
    return out


def decide_geography(state: State, v: Vendor, ctx: RunContext) -> None:
    entries = collect_geo(state, v, ctx)
    solid = [g for g in entries if g.kind in ("maps", "vendor_site")]
    claimed = [g for g in entries if g.kind == "marketplace"]
    note_parts: list[str] = []

    def facts(entry: GeoEntry | None, value: str, prov: Provenance):
        v.facts["location"] = Fact(value=value, provenance=prov, evidence_ids=[entry.evidence_id] if entry and entry.evidence_id else [])

    def pick(pool: list[GeoEntry]) -> GeoEntry | None:
        # Ahmedabad presence (own address, branch, warehouse, plant) beats an HQ elsewhere; else strongest city, else country
        for g in pool:
            if g.place.city == "Ahmedabad":
                return g
        for g in sorted(pool, key=lambda g: (-g.reliability, g.place.city is None)):
            if g.place.city:
                return g
        for g in pool:
            if g.place.state:
                return g
        for g in pool:
            if g.place.country:
                return g
        return None

    def assign(g: GeoEntry, status: str, why: str) -> None:
        pl = g.place
        v.city = "Ahmedabad" if pl.city == "Ahmedabad" else pl.city
        v.state = pl.state
        v.country = pl.country
        v.tier = tier_from_place(v.city, v.country)
        v.geo_status = status
        v.tier_reason = why
        facts(g, f"{pl.matched}" + (f", {pl.state}" if pl.state and pl.state != pl.matched else "") + f", {pl.country}",
              Provenance.SOURCED)

    chosen = pick(solid)
    if chosen:
        status = "VERIFIED"
        where = chosen.place.matched
        assign(chosen, status, f"{chosen.kind.replace('_', ' ')} states '{where}' (evidence {chosen.evidence_id})")
        # conflicts: a more-reliable source and a lower-reliability one disagree about Ahmedabad / country
        for g in claimed:
            if g.place.country and chosen.place.country and g.place.country != chosen.place.country:
                v.conflicts.append(f"marketplace text implies {g.place.country} but the vendor site/maps implies {chosen.place.country}; "
                                   f"used the higher-reliability source")
            elif (g.place.city == "Ahmedabad") != (chosen.place.city == "Ahmedabad") and g.place.city:
                v.conflicts.append(f"marketplace text says {g.place.matched} but the vendor site/maps says {chosen.place.matched}; "
                                   f"used the higher-reliability source")
        v.conflicts = list(dict.fromkeys(v.conflicts))      # one line per distinct conflict
        others = {g.place.city for g in solid if g.place.city and g.place.city != chosen.place.city}
        if others:
            v.tier_reason += f"; also located in {', '.join(sorted(others))}"
        return
    chosen = pick(claimed)
    if chosen:
        assign(chosen, "CLAIMED", f"only a marketplace listing states '{chosen.place.matched}' (evidence {chosen.evidence_id}); "
                                  "not confirmed on a vendor site or map listing")
        v.facts["location"].provenance = Provenance.SOURCED
        return
    country = tld_country(v.domain or "") if v.domain else None
    if country:
        v.country, v.tier, v.geo_status = country, tier_from_place(None, country), "WEAK"
        v.tier_reason = f"no address found; country inferred from the .{(v.domain or '').rsplit('.', 1)[-1]} domain only"
        v.facts["location"] = Fact(value=f"{country} (inferred from domain)", provenance=Provenance.ASSUMED)
        return
    v.tier, v.geo_status = Tier.UNRESOLVED, "UNKNOWN"
    v.tier_reason = "no location evidence found"
    v.facts["location"] = Fact(value="unknown", provenance=Provenance.NEEDS_RFQ)
