"""Mutable pipeline state shared by the stages."""
from __future__ import annotations

import threading
from dataclasses import dataclass, field

from .models import Evidence, NormalisedMaterial, SearchResult, Tier, Vendor
from .signals import quote_in_text


@dataclass
class Hit:
    """One search result that led to a vendor candidate (kept for traceability)."""
    result: SearchResult
    material_id: str
    tier_searched: Tier
    from_places: bool = False


@dataclass
class State:
    materials: list[NormalisedMaterial]
    vendors: dict[str, Vendor] = field(default_factory=dict)
    hits: dict[str, list[Hit]] = field(default_factory=dict)             # vendor_id -> hits
    evidence: dict[str, Evidence] = field(default_factory=dict)          # evidence id -> evidence
    sources: dict[str, list[str]] = field(default_factory=dict)          # url -> texts the quotes must appear in
    excluded: list[dict] = field(default_factory=list)                   # candidates that never became vendors
    dropped_claims: list[dict] = field(default_factory=list)             # claims rejected by the evidence gate
    fetch_failures: list[dict] = field(default_factory=list)
    found: dict[tuple[str, str], set[str]] = field(default_factory=dict)  # (material_id, tier) -> vendor ids surfaced for exactly that pair
    _lock: threading.Lock = field(default_factory=threading.Lock)

    # ------------------------------------------------------------------ sources + evidence gate
    def add_source_text(self, url: str, text: str) -> None:
        with self._lock:
            self.sources.setdefault(url, [])
            if text not in self.sources[url]:
                self.sources[url].append(text)

    def gate(self, ev: Evidence) -> bool:
        """THE evidence gate: a claim is admitted only with a URL and a quote found in that URL's recorded text."""
        texts = self.sources.get(ev.url, [])
        ok = bool(ev.url) and bool(ev.quote.strip()) and any(quote_in_text(ev.quote, t) for t in texts)
        with self._lock:
            if ok:
                self.evidence[ev.id] = ev
            else:
                self.dropped_claims.append({"vendor_id": ev.vendor_id, "claim": ev.claim, "url": ev.url,
                                            "quote": ev.quote[:160], "reason": "quote not found in recorded source text"})
        return ok

    def evidence_for(self, vendor_id: str, material_id: str | None = None) -> list[Evidence]:
        out = [e for e in self.evidence.values() if e.vendor_id == vendor_id]
        if material_id is not None:
            out = [e for e in out if not e.material_ids or material_id in e.material_ids]
        return out
