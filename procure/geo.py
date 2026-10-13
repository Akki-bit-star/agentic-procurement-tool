"""Deterministic geography: locate places in text, classify a vendor into a tier.

Rule of the road: a tier is only ever derived from QUOTED evidence. A location that appears only in a
marketplace city filter is recorded as geo_status=CLAIMED, never VERIFIED.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from urllib.parse import urlparse

from .config import load_gazetteer
from .models import Tier

_ADDR_CTX = re.compile(r"\b(address|office|registered|head\s*office|works|plant|factory|unit|godown|warehouse|"
                       r"depot|branch|located|situated|based in|survey no|plot no|gidc|industrial (?:area|estate)|"
                       r"road|pin ?code|pincode|\b\d{6}\b)", re.I)
_FACILITY_CTX = re.compile(r"\b(warehouse|godown|depot|branch|stockyard|stock yard|plant|factory|works|office|unit)\b", re.I)


_LOCATIVE = re.compile(r"\b(?:in|from|at|based in|located in|situated in)\s+(?:[A-Za-z.]+\s+){0,2}$", re.I)


@dataclass
class Place:
    city: str | None
    state: str | None
    country: str | None
    matched: str
    in_address_context: bool
    facility: bool
    locative: bool = False   # written as "in/from/at <place>" - i.e. where the vendor IS, not where it ships to


def _word(term: str) -> re.Pattern:
    return re.compile(r"(?<![A-Za-z])" + re.escape(term) + r"(?![A-Za-z])", re.I)


def _compile():
    g = load_gazetteer()
    abad = [(n, "Ahmedabad", "Gujarat", "India") for n in g["ahmedabad"]["names"]]
    abad += [(n, "Ahmedabad", "Gujarat", "India") for n in g["ahmedabad"]["localities"]]
    cities = [(c, c, s, "India") for c, s in g["india_cities"].items()]
    states = [(s, None, s, "India") for s in g["india_states"]]
    countries = [(alias, None, None, country) for country, aliases in g["countries"].items() for alias in aliases]
    out = []
    for term, city, state, country in abad + cities + states + countries:
        out.append((_word(term), term, city, state, country))
    return out


_PATTERNS = None


def find_places(text: str) -> list[Place]:
    global _PATTERNS
    if _PATTERNS is None:
        _PATTERNS = _compile()
    places: list[Place] = []
    for line in re.split(r"\n|(?<=[.;])\s", text):
        if not line.strip():
            continue
        addr = bool(_ADDR_CTX.search(line))
        fac = bool(_FACILITY_CTX.search(line))
        for pat, term, city, state, country in _PATTERNS:
            m = pat.search(line)
            if m:
                loc = bool(_LOCATIVE.search(line[max(0, m.start() - 30):m.start()]))
                places.append(Place(city, state, country, term, addr, fac, loc))
        if addr and re.search(r"\bIndia\b", line):          # bare "India" only counts inside an address line
            places.append(Place(None, None, "India", "India", True, fac, False))
    return places


def tld_country(url: str) -> str | None:
    host = (urlparse(url).hostname or "").lower()
    tld = host.rsplit(".", 1)[-1]
    return load_gazetteer()["tld_country"].get(tld)


def registrable_domain(url_or_host: str) -> str | None:
    host = urlparse(url_or_host).hostname if "://" in url_or_host else url_or_host
    if not host:
        return None
    host = host.lower().removeprefix("www.")
    parts = host.split(".")
    if len(parts) >= 3 and parts[-2] in ("co", "com", "org", "net", "gov", "ac") and len(parts[-1]) == 2:
        return ".".join(parts[-3:])
    return ".".join(parts[-2:]) if len(parts) >= 2 else host


def domain_matches(domain: str | None, listed: list[str]) -> bool:
    if not domain:
        return False
    d = domain.lower()
    return any(d == x or d.endswith("." + x) for x in listed)


def tier_from_place(city: str | None, country: str | None) -> Tier:
    if country is None:
        return Tier.UNRESOLVED
    if country != "India":
        return Tier.GLOBAL
    return Tier.AHMEDABAD if city == "Ahmedabad" else Tier.INDIA_OTHER
