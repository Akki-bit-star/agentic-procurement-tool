"""Exports: JSON (source of truth), CSV (one row per material x vendor), Markdown (human report)."""
from __future__ import annotations

import csv
import io
import json
from pathlib import Path

from .models import MatchClass, Provenance, Tier, Vendor
from .pipeline import RunResult
from .report_md import to_markdown  # noqa: F401  (re-exported)

TIER_TITLES = {
    Tier.AHMEDABAD: "Ahmedabad vendors",
    Tier.INDIA_OTHER: "India-based vendors outside Ahmedabad",
    Tier.GLOBAL: "International / global vendors",
    Tier.UNRESOLVED: "Location could not be determined",
}
MATCH_ORDER = {MatchClass.EXACT: 0, MatchClass.NEAR: 1, MatchClass.CATEGORY: 2, MatchClass.UNVERIFIED: 3}


def _prov(p: Provenance) -> str:
    return f"[{p.value}]"


def _evmap(res: RunResult):
    return {e.id: e for e in res.evidence}


def _q(s: str, n: int = 220) -> str:
    s = " ".join(s.split())
    return (s[: n - 1] + "…") if len(s) > n else s


def rows(res: RunResult) -> list[dict]:
    ev = _evmap(res)
    mats = {nm.original.id: nm for nm in res.materials}
    out = []
    for v in res.vendors:
        for mid, a in v.assessments.items():
            def fv(key):
                f = v.facts.get(key)
                return f"{f.value} {_prov(f.provenance)}" if f else ""
            used = [ev[i] for i in a.evidence_ids if i in ev]
            out.append({
                "material_id": mid, "material": mats[mid].original.description_raw, "tier": v.tier.value, "rank": a.rank,
                "shortlisted": a.shortlisted, "vendor": v.name, "vendor_type": v.vendor_type.value,
                "vendor_type_provenance": v.vendor_type_prov.value,
                "city": v.city or "", "state": v.state or "", "country": v.country or "", "geo_status": v.geo_status,
                "geo_reason": v.tier_reason, "website": v.contact.website or "", "phones": "; ".join(v.contact.phones),
                "emails": "; ".join(v.contact.emails), "address": v.contact.address or "",
                "match_class": a.match_class.value, "match_reasons": " | ".join(a.match_reasons),
                "confidence": a.confidence.value, "confidence_reasons": " | ".join(a.confidence_reasons),
                "score": a.score, **{f"score_{k}": x for k, x in a.score_breakdown.items()},
                "standards": fv("standards"), "certifications": fv("certifications"), "capacity": fv("capacity"),
                "delivery": fv("delivery"), "export": fv("export"), "moq": fv("moq"),
                "price": fv("price"), "lead_time": fv("lead_time"),
                "bulk_feasibility": f"{a.bulk_feasibility.value} {_prov(a.bulk_feasibility.provenance)}" if a.bulk_feasibility else "",
                "evidence": " || ".join(f"[{e.id}] ({e.source_kind}) \"{_q(e.quote, 160)}\" <{e.url}>" for e in used[:6]),
                "source_urls": " ; ".join(v.source_urls[:6]), "unresolved": " | ".join(a.unresolved),
                "conflicts": " | ".join(v.conflicts), "next_step": a.next_step,
                "exclusion_reason": a.exclusion_reason or "", "merged_duplicates": " | ".join(v.merged_from),
            })
    out.sort(key=lambda r: (r["material_id"], r["tier"], r["rank"] or 999))
    return out


def to_csv(res: RunResult, tier: Tier | None = None) -> str:
    rs = [r for r in rows(res) if tier is None or r["tier"] == tier.value]
    if not rs:
        return ""
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rs[0].keys()))
    w.writeheader()
    w.writerows(rs)
    return buf.getvalue()


def to_json(res: RunResult) -> str:
    return res.model_dump_json(indent=1)


def write_outputs(res: RunResult, out_dir: str | Path) -> dict[str, Path]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    files = {"result.json": to_json(res), "report.md": to_markdown(res), "vendors_all.csv": to_csv(res)}
    for tier, name in ((Tier.AHMEDABAD, "vendors_ahmedabad.csv"), (Tier.INDIA_OTHER, "vendors_india_outside_ahmedabad.csv"),
                       (Tier.GLOBAL, "vendors_global.csv")):
        files[name] = to_csv(res, tier)
    paths = {}
    for name, text in files.items():
        p = out / name
        p.write_text(text, encoding="utf-8", newline="")
        paths[name] = p
    return paths
