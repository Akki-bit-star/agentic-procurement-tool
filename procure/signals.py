"""Quote -> typed signals (deterministic).

The evidence ledger stores verbatim QUOTES. Everything the assessor believes about a vendor is
re-derived from those quotes by the regexes below, so:
  * a quote picker (rules or LLM) can only *select* text, never assert a fact the text doesn't show;
  * results are reproducible and explainable ("matched pattern X in quote Y").
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .models import Evidence, NormalisedMaterial

# --------------------------------------------------------------------------- generic patterns
RE_ERW = re.compile(r"\bERW\b|electric\s+resistance\s+weld|\bHFW\b|high\s+frequency\s+weld", re.I)
RE_STD = re.compile(
    r"\b(IS)\s*[:\-]?\s*(1239|3589|1161|4270|4923|3601|1387|2062)\b"
    r"|\b(BS)\s*[:\-]?\s*(1387)\b|\b(EN)\s*[:\-]?\s*(10255|10219|10217)\b"
    r"|\b(ASTM)\s*[:\-]?\s*(A\s?53|A\s?500|A\s?120|A\s?135|A\s?106)\b|\b(API)\s*[:\-]?\s*(5L)\b", re.I)
RE_CLASS_ABC = re.compile(r"\bclass\s*[-:]?\s*([ABC])\b", re.I)
RE_CLASS_WORD = re.compile(r"\b(light|medium|heavy)\b(?=[^\n]{0,24}(?:pipe|tube|class|series|grade|duty|weight))"
                           r"|(?:pipe|tube|class|series|grade)[^\n]{0,16}\b(light|medium|heavy)\b", re.I)
RE_BIS = re.compile(r"\bBIS\b|\bISI\b|bureau of indian standards|\bCM/L\b", re.I)
RE_ISO = re.compile(r"\bISO\s*[-:]?\s*(9001|14001|45001)\b", re.I)
RE_TESTCERT = re.compile(r"test certificate|mill test|\bMTC\b|third[- ]party inspection|\bTPI\b|EN\s*10204|inspection certificate", re.I)
RE_CAPACITY = re.compile(
    r"\bcapacity\b[^\n]{0,80}?\d[\d,\.]*\s*(?:MT|MTPA|TPA|TPM|tonnes?|tons?|metric)"
    r"|\d[\d,\.]*\s*(?:\+\s*)?(?:MTPA|TPA|TPM|(?:MT|tonnes?|tons?|metric tons?)\s*(?:per|/|a)\s*(?:month|annum|year|day))", re.I)
RE_STOCK = re.compile(r"ready stock|in stock|stock available|large stock|bulk stock|stockyard|stock yard|warehouse|godown", re.I)
# Manufacturer status must be SELF-DECLARED ("we are a manufacturer", "our plant", "Manufacturer & Supplier of ...");
# the bare word also appears in "buy from manufacturers like X", which says nothing about the page owner.
RE_MANUF = re.compile(
    r"\bwe (?:are|have|operate)\b[^.\n|]{0,80}\bmanufactur"
    r"|\bour (?:plant|factory|unit|mill|manufacturing|production|facility|facilities)\b"
    r"|\bmanufacturing (?:unit|facility|plant|company|capacity|process)\b"
    r"|\bmanufacturers?\s*(?:,|and|&)\s*(?:suppliers?|exporters?|traders?|dealers?|stockists?)\b"
    r"|\b(?:leading|largest|prominent|reputed|renowned|trusted) (?:\w+ ){0,2}manufacturers?\b"
    r"|\bproduction capacity\b|\bmanufactured (?:by us|in our)\b", re.I)
# Price-information / B2B aggregator sites: they list prices or brokers, they do not make or stock the pipe.
RE_PLATFORM = re.compile(
    r"\bmarketplace\b|\bb2b (?:platform|rates?|marketplace)\b|compare (?:prices|suppliers|quotes)|verified suppliers|"
    r"get (?:free )?quotes? from (?:multiple|verified|top)|best b2b|price trends?\b", re.I)   # NOT 'price list': vendors have those
RE_TRADER = re.compile(r"\btrader|\btrading\b|\bdealer|\bdistributor|\bsupplier|\bstockist|\bwholesal|\bretail", re.I)
RE_STOCKIST = re.compile(r"\bstockist|\bdealer|\bdistributor", re.I)
RE_DELIVERY = re.compile(r"pan[- ]?india|all over india|across india|throughout india|nationwide|pan india|"
                         r"\bdeliver(?:y|ies|ed|s)?\b|\bdispatch|we supply|supply(?:ing)? to|serv(?:e|ing|ice)s? (?:area|across)", re.I)
RE_EXPORT = re.compile(r"\bexport(?:er|ers|s|ing)?\b|worldwide|globally|\bFOB\b|\bCIF\b|\bCFR\b|ship(?:s|ping)? to|overseas", re.I)
RE_MOQ = re.compile(r"\b(?:MOQ|minimum order(?: quantity)?|min\.? order)\b[^\n]{0,60}", re.I)
RE_PHONE = re.compile(r"(?<![\d])(?:\+?91[\s-]?)?[6-9]\d{4}[\s-]?\d{5}(?![\d])|\+\d{1,3}[\s-]?\(?\d{1,4}\)?[\s-]?\d{3,4}[\s-]?\d{3,5}")
RE_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
RE_RANGE = re.compile(r"(\d+(?:\.\d+)?)\s*(?:-|–|to)\s*(\d+(?:\.\d+)?)\s*(mm|nb|inch(?:es)?|\"|”)", re.I)

INCH_FOR_DN = {15: r"1/2", 20: r"3/4", 25: r"1", 32: r"1\s*1/4|1\.25|1¼", 40: r"1\s*1/2|1\.5|1½",
               50: r"2", 65: r"2\s*1/2|2\.5|2½", 80: r"3", 100: r"4", 125: r"5", 150: r"6"}
INCH_VALUE_FOR_DN = {15: 0.5, 20: 0.75, 25: 1, 32: 1.25, 40: 1.5, 50: 2, 65: 2.5, 80: 3, 100: 4, 125: 5, 150: 6}


def _fmt(v: float) -> str:
    return f"{v:g}"


def norm_standard(m: re.Match) -> str:
    groups = [g for g in m.groups() if g]
    return f"{groups[0].upper()} {groups[1].upper().replace(' ', '')}"


# --------------------------------------------------------------------------- per-material patterns
@dataclass
class ReqPatterns:
    material_id: str
    dn: int | None
    size_strong: list[re.Pattern]
    size_weak: list[re.Pattern]
    od_values: list[float]
    od_pat: list[re.Pattern]
    walls: dict[float, str]            # wall value -> label ("as written" / "IS 1239 heavy" / ...)
    wall_pats: dict[float, re.Pattern]
    required_standards: list[str]
    class_letters: set[str]
    class_words: set[str]


def build_patterns(nm: NormalisedMaterial) -> ReqPatterns:
    from .config import load_standards
    r, s = nm.resolved, nm.spec
    dn = r.dn
    strong, weak = [], []
    if dn:
        strong.append(re.compile(rf"\b(?:DN|NB)\s*[-:.]?\s*{dn}\b", re.I))
        strong.append(re.compile(rf"(?<![\d./])\b{dn}\s*(?:NB|N\.B\.?|mm\s*NB|mm\s*\(?\s*NB)\b", re.I))
        inch = INCH_FOR_DN.get(dn)
        if inch:
            strong.append(re.compile(rf"(?<![\d./.])(?:{inch})\s*(?:\"|”|''|inch(?:es)?\b|in\b)", re.I))
        weak.append(re.compile(rf"(?<![\d.])\b{dn}\s*mm\b", re.I))
    if s.bare_mm and not dn:
        weak.append(re.compile(rf"(?<![\d.])\b{s.bare_mm:g}\s*mm\b", re.I))
    ods = sorted({v for v in [r.od_mm] if v})
    ref = load_standards()["sizes"].get(dn) if dn else None
    if ref:
        ods = sorted(set(ods) | {ref["od"]})
    od_pat = [re.compile(rf"(?<![\d.]){re.escape(_fmt(v))}0?(?![\d])") for v in ods]
    walls: dict[float, str] = {}
    if r.wall_mm:
        walls[r.wall_mm] = "as written" if r.basis.get("wall_mm") and r.basis["wall_mm"].value == "SOURCED" else "resolved (IS 1239 reference)"
    if ref and r.wall_mm and any(f.code == "WALL_NOT_IN_STANDARD" for f in nm.flags):
        from .normalize import available_walls
        avail = available_walls(ref)
        series = min(avail, key=lambda k: abs(avail[k] - r.wall_mm))
        walls.setdefault(avail[series], f"nearest IS 1239 series ({series})")
    wall_pats = {w: re.compile(rf"(?<![\d.]){re.escape(_fmt(w))}0?\s*(?:mm|thk)|(?:thick\w*|thk|wt|wall)[^\n]{{0,28}}(?<![\d.]){re.escape(_fmt(w))}(?![\d])", re.I)
                 for w in walls}
    req_std = [x for x in s.standards if x]
    if r.standard and r.standard.startswith("IS 1239") and "IS 1239" not in req_std:
        req_std.append("IS 1239")
    letters = {s.pipe_class} if s.pipe_class else set()
    words = {r.class_meaning} if r.class_meaning else set()
    return ReqPatterns(nm.original.id, dn, strong, weak, ods, od_pat, walls, wall_pats, req_std, letters, words)


# --------------------------------------------------------------------------- signals from text
@dataclass
class MaterialSignals:
    erw: bool = False
    standards: set[str] = field(default_factory=set)
    size_strong: bool = False
    size_weak: bool = False
    size_range: bool = False
    od_hit: bool = False
    walls_hit: dict[float, str] = field(default_factory=dict)
    class_letters: set[str] = field(default_factory=set)
    class_words: set[str] = field(default_factory=set)
    notes: list[str] = field(default_factory=list)


def _range_covers(text: str, dn: int | None) -> bool:
    if not dn:
        return False
    for m in RE_RANGE.finditer(text):
        lo, hi, unit = float(m.group(1)), float(m.group(2)), m.group(3).lower()
        if unit in ("mm", "nb") and lo <= dn <= hi:
            return True
        if unit.startswith("inch") or unit in ('"', "”"):
            iv = INCH_VALUE_FOR_DN.get(dn)
            if iv and lo <= iv <= hi:
                return True
    return False


def analyze_text(text: str, pat: ReqPatterns) -> MaterialSignals:
    sig = MaterialSignals()
    sig.erw = bool(RE_ERW.search(text))
    for m in RE_STD.finditer(text):
        sig.standards.add(norm_standard(m))
    sig.size_strong = any(p.search(text) for p in pat.size_strong)
    sig.size_weak = any(p.search(text) for p in pat.size_weak)
    sig.size_range = _range_covers(text, pat.dn)
    sig.od_hit = any(p.search(text) for p in pat.od_pat)
    for w, p in pat.wall_pats.items():
        if p.search(text):
            sig.walls_hit[w] = pat.walls[w]
    sig.class_letters = {m.group(1).upper() for m in RE_CLASS_ABC.finditer(text)}
    for m in RE_CLASS_WORD.finditer(text):
        sig.class_words.add((m.group(1) or m.group(2)).lower())
    return sig


@dataclass
class VendorSignals:
    certs: set[str] = field(default_factory=set)       # BIS / ISO / TESTCERT
    capacity: str | None = None
    stock: bool = False
    manufacturer: bool = False
    platform: bool = False
    trader: bool = False
    stockist: bool = False
    delivery: bool = False
    delivery_india_wide: bool = False
    delivery_ahmedabad_or_gujarat: bool = False
    export: bool = False
    export_india: bool = False
    moq: str | None = None
    phones: list[str] = field(default_factory=list)
    emails: list[str] = field(default_factory=list)


def analyze_vendor_text(text: str) -> VendorSignals:
    v = VendorSignals()
    if RE_BIS.search(text):
        v.certs.add("BIS/ISI")
    if RE_ISO.search(text):
        v.certs.add("ISO")
    if RE_TESTCERT.search(text):
        v.certs.add("TEST_CERT")
    m = RE_CAPACITY.search(text)
    v.capacity = m.group(0).strip() if m else None
    v.stock = bool(RE_STOCK.search(text))
    v.manufacturer = bool(RE_MANUF.search(text))
    v.platform = bool(RE_PLATFORM.search(text))
    v.trader = bool(RE_TRADER.search(text))
    v.stockist = bool(RE_STOCKIST.search(text))
    v.delivery = bool(RE_DELIVERY.search(text))
    v.delivery_india_wide = bool(re.search(r"pan[- ]?india|all over india|across india|throughout india|nationwide", text, re.I))
    for line in text.split("\n"):
        if re.search(r"ahmedabad|gujarat", line, re.I) and RE_DELIVERY.search(line):
            v.delivery_ahmedabad_or_gujarat = True
    v.export = bool(RE_EXPORT.search(text))
    for line in text.split("\n"):
        if re.search(r"\bindia\b", line, re.I) and re.search(r"export|ship|supply|deliver", line, re.I):
            v.export_india = True
    m = RE_MOQ.search(text)
    v.moq = m.group(0).strip() if m else None
    v.phones = list(dict.fromkeys(p.strip() for p in RE_PHONE.findall(text)))[:4]
    v.emails = [e for e in dict.fromkeys(RE_EMAIL.findall(text)) if not e.lower().endswith((".png", ".jpg", ".gif", ".webp"))][:3]
    return v


# --------------------------------------------------------------------------- quote selection (rules)
def _windows(text: str, regex: re.Pattern, k: int = 2, span: int = 3, maxlen: int = 320) -> list[str]:
    lines = [ln.strip() for ln in text.split("\n") if ln.strip()]
    out, used = [], set()
    for i, ln in enumerate(lines):
        if regex.search(ln) and i not in used:
            lo = max(0, i - 1)
            w = " | ".join(lines[lo:lo + span])
            out.append(w[:maxlen])
            used.update(range(lo, lo + span))
            if len(out) >= k:
                break
    return out


def _any(pats: list[re.Pattern]) -> re.Pattern:
    return re.compile("|".join(p.pattern for p in pats), re.I) if pats else re.compile(r"(?!x)x")


def extract_evidence_rules(text: str, url: str, vendor_id: str, source_kind: str,
                           materials: list[NormalisedMaterial]) -> list[Evidence]:
    """Pick quotable windows from a page. Quotes are verbatim substrings of `text` (evidence gate re-checks)."""
    ev: list[Evidence] = []
    n = 0

    def add(ctype: str, claim: str, quote: str, mids: list[str] | None = None):
        nonlocal n
        n += 1
        ev.append(Evidence(id=f"{vendor_id}:E{n}", vendor_id=vendor_id, claim_type=ctype, claim=claim,
                           quote=quote, url=url, source_kind=source_kind, material_ids=mids or []))

    for q in _windows(text, RE_STD, k=2):
        add("standard", "Mentions a product standard", q)
    for q in _windows(text, RE_ERW, k=1):
        add("product_match", "Mentions ERW / welded pipe supply", q)
    for nm in materials:
        pat = build_patterns(nm)
        size_re = _any(pat.size_strong + pat.size_weak + pat.od_pat)
        for q in _windows(text, size_re, k=2):
            add("product_match", f"Mentions a size matching {nm.original.id}", q, [nm.original.id])
        for w, label in pat.walls.items():
            for q in _windows(text, pat.wall_pats[w], k=1):
                add("wall", f"Mentions {w:g} mm wall ({label}) for {nm.original.id}", q, [nm.original.id])
    for q in _windows(text, re.compile(RE_CLASS_ABC.pattern + "|" + RE_CLASS_WORD.pattern, re.I), k=1):
        add("class", "Mentions a pipe class / series", q)
    for q in _windows(text, re.compile(RE_BIS.pattern + "|" + RE_ISO.pattern + "|" + RE_TESTCERT.pattern, re.I), k=2):
        add("certification", "Mentions certification / test certificate", q)
    for q in _windows(text, RE_CAPACITY, k=1):
        add("capacity", "States production capacity", q)
    for q in _windows(text, RE_STOCK, k=1):
        add("stock", "Mentions stock / warehouse", q)
    for q in _windows(text, re.compile(RE_MANUF.pattern + "|" + RE_TRADER.pattern + "|" + RE_PLATFORM.pattern, re.I), k=2):
        add("profile", "Describes the business type", q)
    for q in _windows(text, RE_DELIVERY, k=2):
        add("delivery", "Mentions delivery / supply area", q)
    for q in _windows(text, RE_EXPORT, k=1):
        add("export", "Mentions export / overseas supply", q)
    for q in _windows(text, RE_MOQ, k=1):
        add("moq", "States a minimum order", q)
    from .geo import find_places
    loc_lines = [ln for ln in text.split("\n") if ln.strip()]
    got = 0
    for ln in loc_lines:
        pl = find_places(ln)
        if any(p.in_address_context and (p.city or p.state or p.country) for p in pl) and len(ln) < 400:
            add("location", "Address / location statement", ln.strip()[:320])
            got += 1
            if got >= 2:
                break
    for q in _windows(text, re.compile(RE_PHONE.pattern + "|" + RE_EMAIL.pattern), k=1, span=1):
        add("contact", "Contact details", q)
    return ev


def quote_in_text(quote: str, text: str) -> bool:
    """Evidence gate: the quote must be present in the fetched source (whitespace-insensitive)."""
    def norm(s: str) -> str:
        return re.sub(r"[\s|]+", " ", s).strip().lower()
    q = norm(quote)
    return bool(q) and q in norm(text)
