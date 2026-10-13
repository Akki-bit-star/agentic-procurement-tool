"""Core data models.

Design rule: every fact attached to a vendor carries a `Provenance` label so the
report can always separate SOURCED facts from DERIVED / ASSUMED / NEEDS_RFQ ones.
"""
from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


def utcnow() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# --------------------------------------------------------------------------- enums
class Provenance(str, Enum):
    SOURCED = "SOURCED"          # backed by a verbatim quote + URL in the evidence ledger
    DERIVED = "DERIVED"          # computed deterministically from other facts (e.g. kg/m)
    REFERENCE = "REFERENCE"      # from our bundled standards table (secondary source, verify vs BIS)
    ASSUMED = "ASSUMED"          # a stated assumption the user can override
    NEEDS_RFQ = "NEEDS_RFQ"      # cannot be known without asking the vendor


class Severity(str, Enum):
    CRITICAL = "CRITICAL"  # changes who can supply it / what is bought
    WARNING = "WARNING"    # likely technical inconsistency
    INFO = "INFO"


class Tier(str, Enum):
    AHMEDABAD = "AHMEDABAD"
    INDIA_OTHER = "INDIA_OTHER"
    GLOBAL = "GLOBAL"
    UNRESOLVED = "UNRESOLVED"  # location could not be determined -> never forced into a tier


class MatchClass(str, Enum):
    EXACT = "EXACT"
    NEAR = "NEAR"
    CATEGORY = "CATEGORY"
    UNVERIFIED = "UNVERIFIED"


class Confidence(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class VendorType(str, Enum):
    MANUFACTURER = "MANUFACTURER"
    STOCKIST = "STOCKIST"          # stockist / distributor / dealer
    TRADER = "TRADER"
    MARKETPLACE_LISTING = "MARKETPLACE_LISTING"
    UNKNOWN = "UNKNOWN"


# --------------------------------------------------------------------------- input
class MaterialInput(BaseModel):
    """One line item exactly as the user typed it. Never mutated."""
    id: str
    description_raw: str
    quantity: float | None = None
    unit: str | None = None            # None => ambiguous, resolved by assumption
    location_raw: str = "Ahmedabad, Gujarat, India"
    standard_hint: str | None = None


class ProcurementRequest(BaseModel):
    materials: list[MaterialInput]


class Location(BaseModel):
    raw: str
    city: str | None = None
    state: str | None = None
    country: str | None = None


# --------------------------------------------------------------------------- normalised requirement
class Flag(BaseModel):
    code: str
    severity: Severity
    field: str
    message: str
    candidates: list[str] = Field(default_factory=list)   # alternative interpretations
    assumption: str | None = None                         # what the system proceeds with
    provenance: Provenance = Provenance.ASSUMED
    action: str | None = None                             # what the buyer should confirm


class PipeSpec(BaseModel):
    """Structured spec. Values are what the user *wrote* unless `Provenance` says otherwise."""
    product: str | None = None            # e.g. "ERW pipe"
    process: str | None = None            # ERW
    material: str | None = None           # MS / GI
    dn: int | None = None                 # nominal bore, mm
    bare_mm: float | None = None          # a size written as "40 mm" with no DN / OD marker
    od_mm: float | None = None
    wall_mm: float | None = None
    standards: list[str] = Field(default_factory=list)   # ["IS 1239"]
    pipe_class: str | None = None         # "B"
    class_meaning: str | None = None      # "medium" (trade convention) - ASSUMED


class ResolvedSpec(BaseModel):
    """What the system will actually search / match against. Every field says where it came from,
    so the user's original wording is never silently replaced."""
    dn: int | None = None
    od_mm: float | None = None
    wall_mm: float | None = None
    standard: str | None = None            # "IS 1239 (Part 1)"
    class_meaning: str | None = None       # light | medium | heavy
    basis: dict[str, Provenance] = Field(default_factory=dict)   # field -> provenance
    notes: list[str] = Field(default_factory=list)


class DerivedFigures(BaseModel):
    kg_per_m: float | None = None
    kg_per_m_basis: str | None = None      # explains which OD/wall was used
    quantity_tonnes: float | None = None
    quantity_metres: float | None = None
    approx_6m_lengths: int | None = None
    provenance: Provenance = Provenance.DERIVED


class NormalisedMaterial(BaseModel):
    original: MaterialInput                 # preserved verbatim
    location: Location
    spec: PipeSpec
    resolved: ResolvedSpec = Field(default_factory=ResolvedSpec)
    quantity_tonnes: float | None
    unit_assumed: bool
    derived: DerivedFigures
    flags: list[Flag] = Field(default_factory=list)
    # Interpretations the discovery agents search for (primary first).
    search_interpretations: list[str] = Field(default_factory=list)


# --------------------------------------------------------------------------- evidence
class Evidence(BaseModel):
    """A single quote-backed claim. The ONLY way a sourced fact enters the report."""
    id: str
    vendor_id: str
    claim_type: str          # primary type: product_match | standard | class | wall | certification | location | capacity | ...
    claim_types: list[str] = Field(default_factory=list)   # ALL types this one quote supports (merged, see verify.admit)
    claim: str               # short statement, e.g. "Lists IS 1239 ERW pipe"
    quote: str               # verbatim text from the page
    url: str
    fetched_at: str = Field(default_factory=utcnow)
    source_kind: str = "unknown"   # vendor_site | marketplace | maps | directory | other
    material_ids: list[str] = Field(default_factory=list)

    def model_post_init(self, _ctx) -> None:
        if self.claim_type not in self.claim_types:
            self.claim_types.insert(0, self.claim_type)


class SearchResult(BaseModel):
    title: str
    url: str
    snippet: str = ""
    position: int = 0
    # Optional structured business data (Maps/places endpoint)
    address: str | None = None
    phone: str | None = None
    website: str | None = None
    rating: float | None = None
    query: str = ""
    provider: str = ""


class Page(BaseModel):
    url: str
    ok: bool
    status: int | None = None
    text: str = ""
    title: str | None = None
    site_name: str | None = None            # og:site_name when present - the best source for a vendor's real name
    links: list[str] = Field(default_factory=list)   # same-site contact/about links (for the location follow-up)
    error: str | None = None
    fetched_at: str = Field(default_factory=utcnow)


# --------------------------------------------------------------------------- vendor
class Contact(BaseModel):
    website: str | None = None
    phones: list[str] = Field(default_factory=list)
    emails: list[str] = Field(default_factory=list)
    address: str | None = None


class Fact(BaseModel):
    """A labelled value shown to the buyer."""
    value: str
    provenance: Provenance
    evidence_ids: list[str] = Field(default_factory=list)


class MaterialAssessment(BaseModel):
    material_id: str
    match_class: MatchClass = MatchClass.UNVERIFIED
    match_reasons: list[str] = Field(default_factory=list)
    score: float = 0.0
    score_breakdown: dict[str, float] = Field(default_factory=dict)
    score_notes: list[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW
    confidence_reasons: list[str] = Field(default_factory=list)
    bulk_feasibility: Fact | None = None
    unresolved: list[str] = Field(default_factory=list)
    next_step: str = ""
    shortlisted: bool = False
    rank: int | None = None                 # rank within (material, tier), 1 = best
    exclusion_reason: str | None = None
    evidence_ids: list[str] = Field(default_factory=list)


class Vendor(BaseModel):
    id: str
    name: str
    aliases: list[str] = Field(default_factory=list)
    domain: str | None = None
    vendor_type: VendorType = VendorType.UNKNOWN
    vendor_type_prov: Provenance = Provenance.ASSUMED
    city: str | None = None
    state: str | None = None
    country: str | None = None
    tier: Tier = Tier.UNRESOLVED
    tier_reason: str = ""
    geo_status: str = "UNKNOWN"      # VERIFIED (vendor site / maps) | CLAIMED (marketplace only) | WEAK (domain hint) | UNKNOWN
    contact: Contact = Field(default_factory=Contact)
    source_urls: list[str] = Field(default_factory=list)
    facts: dict[str, Fact] = Field(default_factory=dict)   # standards, certifications, delivery, export, capacity, ...
    conflicts: list[str] = Field(default_factory=list)
    merged_from: list[str] = Field(default_factory=list)
    discovered_for: list[str] = Field(default_factory=list)  # material ids
    found_via: list[str] = Field(default_factory=list)       # tiers of the searches that surfaced it (a hint, NOT its location)
    assessments: dict[str, MaterialAssessment] = Field(default_factory=dict)  # by material id


class RunLog(BaseModel):
    """Everything that went wrong or was decided - surfaced in the report."""
    stage: str
    level: str   # info | warn | error
    message: str
    data: dict[str, Any] = Field(default_factory=dict)
    at: str = Field(default_factory=utcnow)
