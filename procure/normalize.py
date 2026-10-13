"""Stage 1 - Intake & normalisation (deterministic).

Parses the free-text requirement into a structured spec, resolves it against the bundled
IS 1239 (Part 1):2004 reference table (primary source, see config/standards_is1239.yaml), and raises
*flags* for every ambiguity or technical inconsistency. It never overwrites the user's input: the
original line is preserved and the resolved values live in a separate object with a provenance label
per field.
"""
from __future__ import annotations

import re

from .config import RunConfig, load_standards
from .models import (DerivedFigures, Flag, Location, MaterialInput, NormalisedMaterial,
                     PipeSpec, Provenance, ResolvedSpec, Severity)

KG_PER_M_K = 0.02466          # mass of steel pipe: (OD - t) * t * 0.02466 kg/m  (OD, t in mm)
SERIES = ("light", "medium", "heavy")

_DIM = re.compile(r"(\d+(?:\.\d+)?)\s*[x×*]\s*(\d+(?:\.\d+)?)\s*(?:mm)?", re.I)
_DN = re.compile(r"\b(?:DN|NB)\s*[-:]?\s*(\d+)\b", re.I)
_BARE_MM = re.compile(r"(?<![\d.])(\d+(?:\.\d+)?)\s*mm\b", re.I)
_STD = re.compile(r"\b(IS|BS|EN|ASTM|API)\s*[-:]?\s*([A-Z]?\d[\w./-]*)", re.I)
_CLASS = re.compile(r"\bclass\s*[-:]?\s*([ABC])\b", re.I)
_UNIT_TONNES = {"t", "mt", "ton", "tons", "tonne", "tonnes", "metric ton", "metric tons"}
_UNIT_METRES = {"m", "mtr", "mtrs", "metre", "metres", "meter", "meters", "rm", "running metre"}
_UNIT_KG = {"kg", "kgs"}
_UNIT_LENGTHS = {"length", "lengths", "pcs", "pieces", "nos"}


def parse_location(raw: str) -> Location:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    return Location(raw=raw,
                    city=parts[0] if parts else None,
                    state=parts[1] if len(parts) > 2 else None,
                    country=parts[-1] if len(parts) > 1 else None)


def kg_per_m(od: float, wall: float) -> float:
    return (od - wall) * wall * KG_PER_M_K


def parse_spec(desc: str, standard_hint: str | None = None) -> PipeSpec:
    text = desc.strip()
    spec = PipeSpec()
    low = text.lower()

    if "erw" in low:
        spec.process = "ERW"
    if re.search(r"\bpipe\b", low):
        spec.product = "ERW pipe" if spec.process else "pipe"
    elif re.search(r"\btube\b", low):
        spec.product = "tube"
    if re.search(r"\b(ms|mild steel)\b", low):
        spec.material = "MS"
    elif re.search(r"\b(gi|galvani[sz]ed)\b", low):
        spec.material = "GI"

    m = _DN.search(text)
    if m:
        spec.dn = int(m.group(1))

    m = _DIM.search(text)
    consumed = None
    if m:
        spec.od_mm, spec.wall_mm = float(m.group(1)), float(m.group(2))
        consumed = m.span()

    # a bare "<n> mm" that is not part of an "OD x wall" pair and not preceded by DN
    if spec.dn is None:
        for bm in _BARE_MM.finditer(text):
            if consumed and consumed[0] <= bm.start() < consumed[1]:
                continue
            spec.bare_mm = float(bm.group(1))
            break

    stds = []
    for sm in _STD.finditer(text + " " + (standard_hint or "")):
        s = f"{sm.group(1).upper()} {sm.group(2).upper()}"
        if s not in stds:
            stds.append(s)
    spec.standards = stds

    cm = _CLASS.search(text)
    if cm:
        spec.pipe_class = cm.group(1).upper()
    return spec


def _unit_to_tonnes(qty: float | None, unit: str | None, kgpm: float | None, default_unit: str):
    """Returns (tonnes|None, unit_assumed, unit_used)."""
    assumed = unit is None or not str(unit).strip()
    u = (default_unit if assumed else str(unit)).strip().lower()
    if qty is None:
        return None, assumed, u
    if u in _UNIT_TONNES:
        return float(qty), assumed, "tonnes"
    if u in _UNIT_KG:
        return qty / 1000.0, assumed, "kg"
    if u in _UNIT_METRES and kgpm:
        return qty * kgpm / 1000.0, assumed, "metres"
    if u in _UNIT_LENGTHS and kgpm:
        return qty * 6 * kgpm / 1000.0, assumed, "6 m lengths"
    return None, assumed, u


def available_walls(ref: dict) -> dict[str, float]:
    return {k: ref[k] for k in SERIES if ref.get(k) is not None}


def od_range_for(ref: dict, series: str | None) -> tuple[float, float] | None:
    light, mh = ref.get("od_range_light"), ref.get("od_range_mh")
    if series == "light":
        return tuple(light) if light else None
    if series in ("medium", "heavy"):
        return tuple(mh) if mh else None
    rs = [r for r in (light, mh) if r]
    return (min(r[0] for r in rs), max(r[1] for r in rs)) if rs else None


def normalise(m: MaterialInput, cfg: RunConfig) -> NormalisedMaterial:
    std = load_standards()
    sizes: dict[int, dict] = std["sizes"]
    cls_map: dict[str, str] = std["class_map"]
    spec = parse_spec(m.description_raw, m.standard_hint)
    flags: list[Flag] = []
    res = ResolvedSpec()
    used_reference = False

    # ---------------------------------------------------------------- size: DN vs OD vs bare mm
    dn: int | None = spec.dn
    if dn is None and spec.bare_mm is not None:
        n = spec.bare_mm
        cands = []
        if int(n) == n and int(n) in sizes:
            cands.append(f"DN{int(n)} nominal bore (OD about {sizes[int(n)]['od']} mm)")
        cands.append(f"{n:g} mm outside diameter (not a standard IS 1239 OD)")
        if int(n) == n and int(n) in sizes:
            dn = int(n)
            res.basis["dn"] = Provenance.ASSUMED
            flags.append(Flag(
                code="SIZE_BARE_MM", severity=Severity.CRITICAL, field="size",
                message=(f'"{n:g} mm" is ambiguous: Indian trade usage normally means nominal bore '
                         f'(DN{int(n)}, OD about {sizes[int(n)]["od"]} mm), but it could be read as outside diameter.'),
                candidates=cands,
                assumption=f"Treated as DN{int(n)} nominal bore. The OD-{n:g} mm reading is kept as an alternate search.",
                action="Confirm nominal bore vs outside diameter before issuing the RFQ."))
        else:
            res.od_mm = n
            res.basis["od_mm"] = Provenance.ASSUMED
            flags.append(Flag(
                code="SIZE_BARE_MM", severity=Severity.CRITICAL, field="size",
                message=f'"{n:g} mm" cannot be mapped to a known nominal bore.',
                candidates=cands, assumption=f"Treated as OD {n:g} mm.",
                action="Confirm the intended size."))
    elif dn is not None:
        res.basis["dn"] = Provenance.SOURCED  # stated by the user (sourced from the input)
    res.dn = dn
    ref = sizes.get(dn) if dn is not None else None
    lo_nb, hi_nb = std["scope_nb_range"]
    if dn is not None and not lo_nb <= dn <= hi_nb:
        flags.append(Flag(
            code="OUT_OF_IS1239_SCOPE", severity=Severity.WARNING, field="size",
            message=f"DN{dn} is outside IS 1239 (Part 1) scope ({lo_nb}-{hi_nb} mm nominal bore).",
            candidates=["IS 3589 (large-diameter ERW/spiral pipe)", "IS 1161 (structural tube)"],
            assumption="Kept as written.", action="Confirm which standard governs this size."))

    # ---------------------------------------------------------------- standard
    if spec.standards:
        res.standard = "IS 1239 (Part 1)" if "IS 1239" in spec.standards else spec.standards[0]
        res.basis["standard"] = Provenance.SOURCED
    else:
        flags.append(Flag(
            code="STANDARD_NOT_STATED", severity=Severity.WARNING, field="standard",
            message="No product standard is stated in the requirement.",
            candidates=["IS 1239 (Part 1) - light/medium/heavy", "IS 1161 (structural)", "IS 3589 (large-diameter)"],
            assumption=("Assumed IS 1239 (Part 1) because 'Class B' is the Indian trade shorthand for its medium series."
                        if spec.pipe_class else "No standard assumed; vendors listing any Indian pipe standard are kept as near matches."),
            action="State the governing standard in the RFQ."))
        if spec.pipe_class:
            res.standard = "IS 1239 (Part 1)"
            res.basis["standard"] = Provenance.ASSUMED

    # ---------------------------------------------------------------- class (A/B/C trade shorthand)
    if spec.pipe_class:
        meaning = cls_map.get(spec.pipe_class)
        spec.class_meaning = meaning
        res.class_meaning = meaning
        res.basis["class_meaning"] = Provenance.ASSUMED
        band = std["colour_band"][meaning]
        flags.append(Flag(
            code="CLASS_MEANING", severity=Severity.WARNING, field="class",
            message=(f'"Class {spec.pipe_class}" does not appear in IS 1239 (Part 1):2004, which classifies tubes as light, medium '
                     f"and heavy (marked L/M/H, colour bands yellow/blue/red). In Indian trade, Class A/B/C = light/medium/heavy; "
                     "other standards use classes for pressure rating."),
            candidates=[f"IS 1239 {meaning} series", "pressure / other class from a different standard"],
            assumption=f"Read as IS 1239 {meaning} series; wall thickness taken from the BIS table.",
            provenance=Provenance.ASSUMED,
            action=f"Confirm class {spec.pipe_class} = {meaning} ({band} colour band) and the required wall thickness."))

    # ---------------------------------------------------------------- wall, class, OD
    if ref:
        nominal_od = ref["od"]
        walls = available_walls(ref)
        # wall first (it can settle the series), then the OD range for that series
        if spec.wall_mm is not None:
            res.wall_mm = spec.wall_mm
            res.basis["wall_mm"] = Provenance.SOURCED
            hit = next((k for k, v in walls.items() if abs(v - spec.wall_mm) <= 0.06), None)
            if hit:
                if not res.class_meaning:
                    res.class_meaning = hit
                    res.basis["class_meaning"] = Provenance.DERIVED
                used_reference = True
                res.notes.append(f"Wall {spec.wall_mm:g} mm matches the IS 1239 {hit} series for DN{dn}.")
            else:
                other = std.get("other_standard_walls", {}).get(dn)
                cands = [f"{k} series ({v:g} mm)" for k, v in walls.items()]
                cands.append(f"{spec.wall_mm:g} mm as written (custom / other standard)")
                extra = ""
                if other and abs(other["value"] - spec.wall_mm) <= 0.1:
                    cands.insert(0, f"{other['label']}: {other['value']} mm")
                    extra = f" It is close to {other['label']} ({other['value']} mm)."
                flags.append(Flag(
                    code="WALL_NOT_IN_STANDARD", severity=Severity.WARNING, field="wall",
                    message=(f"{spec.wall_mm:g} mm is not an IS 1239 wall thickness for DN{dn} "
                             f"(BIS Tables 3-5: " + ", ".join(f"{k} {v:g}" for k, v in walls.items()) + f" mm).{extra} "
                             "The requirement combines an IS 1239 reference with a wall outside that standard."),
                    candidates=cands,
                    assumption=(f"Kept {spec.wall_mm:g} mm as written. Vendors are searched for it AND for the nearest IS 1239 series; "
                                f"those without a {spec.wall_mm:g} mm product are NEAR matches at best."),
                    action="Confirm the required wall thickness (and whether IS 1239 or another standard governs)."))
        elif res.class_meaning in walls:
            res.wall_mm = walls[res.class_meaning]
            res.basis["wall_mm"] = Provenance.REFERENCE
            used_reference = True
            res.notes.append(f"Wall {res.wall_mm:g} mm = IS 1239 {res.class_meaning} series for DN{dn} (BIS table).")

        rng = od_range_for(ref, res.class_meaning)
        if spec.od_mm is not None:
            res.od_mm = spec.od_mm
            res.basis["od_mm"] = Provenance.SOURCED
            if rng and rng[0] - 0.001 <= spec.od_mm <= rng[1] + 0.001:
                at_limit = abs(spec.od_mm - rng[1]) < 0.001 or abs(spec.od_mm - rng[0]) < 0.001
                if at_limit and abs(spec.od_mm - nominal_od) > 0.05:
                    side = "maximum" if abs(spec.od_mm - rng[1]) < 0.001 else "minimum"
                    flags.append(Flag(
                        code="OD_AT_LIMIT", severity=Severity.INFO, field="od",
                        message=(f"{spec.od_mm:g} mm is valid but is the {side} permitted OD for DN{dn} in IS 1239 "
                                 f"(range {rng[0]:g}-{rng[1]:g} mm); the usual nominal OD is {nominal_od:g} mm."),
                        candidates=[f"nominal OD {nominal_od:g} mm", f"{side} OD limit {spec.od_mm:g} mm"],
                        assumption=f"Kept {spec.od_mm:g} mm as written; searches also use the nominal {nominal_od:g} mm.",
                        action=f"Confirm whether {spec.od_mm:g} mm is a deliberate OD requirement or a table limit copied from the standard."))
            elif rng:
                flags.append(Flag(
                    code="OD_MISMATCH", severity=Severity.WARNING, field="od",
                    message=(f"{spec.od_mm:g} mm is outside the IS 1239 OD range for DN{dn} ({rng[0]:g}-{rng[1]:g} mm)."),
                    candidates=[f"nominal OD {nominal_od:g} mm", f"{spec.od_mm:g} mm as written"],
                    assumption="Kept as written.", action="Confirm OD vs nominal bore."))
        else:
            res.od_mm = nominal_od
            res.basis["od_mm"] = Provenance.REFERENCE
            used_reference = True
    else:
        res.od_mm = res.od_mm or spec.od_mm
        res.wall_mm = spec.wall_mm
        if spec.od_mm is not None:
            res.basis["od_mm"] = Provenance.SOURCED
        if spec.wall_mm is not None:
            res.basis["wall_mm"] = Provenance.SOURCED
        if dn is not None:
            flags.append(Flag(code="DN_NOT_IN_REFERENCE", severity=Severity.INFO, field="size",
                              message=f"DN{dn} is not in the bundled reference table; dimensions cannot be cross-checked.",
                              assumption="No reference cross-check performed."))

    # ---------------------------------------------------------------- scope note (verified against the standard text)
    if spec.process == "ERW" and any(s.startswith("IS 1239") for s in spec.standards + ([res.standard] if res.standard else [])):
        flags.append(Flag(
            code="STANDARD_SCOPE_NOTE", severity=Severity.INFO, field="standard",
            message=("IS 1239 (Part 1):2004 permits ERW/HFIW manufacture (cl. 6.3) and covers 6-150 mm nominal bore for water, "
                     "non-hazardous gas, air and steam. Vendors quoting IS 3589 (large-diameter), IS 1161 (structural) or ASTM/API "
                     "are a different scope."),
            assumption="Vendors quoting another standard are classed NEAR, not EXACT.",
            provenance=Provenance.REFERENCE,
            action="Ask vendors for the BIS licence (ISI mark), the L/M/H marking and colour band, and a test certificate for the exact series."))

    # ---------------------------------------------------------------- derived figures
    d = DerivedFigures()
    table_kgpm = None
    if ref and res.class_meaning in available_walls(ref) and res.wall_mm and abs(res.wall_mm - ref[res.class_meaning]) <= 0.06:
        table_kgpm = ref["kgpm"][res.class_meaning]
    if table_kgpm is not None:
        d.kg_per_m = table_kgpm
        formula = round(kg_per_m(res.od_mm, res.wall_mm), 2) if res.od_mm else None
        d.kg_per_m_basis = (f"IS 1239 table: DN{dn} {res.class_meaning} = {table_kgpm} kg/m (plain end)"
                            + (f"; formula cross-check {formula} kg/m" if formula else ""))
        d.provenance = Provenance.REFERENCE
    elif res.od_mm and res.wall_mm:
        d.kg_per_m = round(kg_per_m(res.od_mm, res.wall_mm), 3)
        d.kg_per_m_basis = (f"formula ({res.od_mm:g} - {res.wall_mm:g}) x {res.wall_mm:g} x {KG_PER_M_K} "
                            f"[OD {res.basis.get('od_mm', Provenance.ASSUMED).value}, wall {res.basis.get('wall_mm', Provenance.ASSUMED).value}]")
    tonnes, unit_assumed, unit_used = _unit_to_tonnes(m.quantity, m.unit, d.kg_per_m, cfg.default_unit)
    d.quantity_tonnes = round(tonnes, 3) if tonnes is not None else None
    if tonnes is not None and d.kg_per_m:
        d.quantity_metres = round(tonnes * 1000 / d.kg_per_m)
        d.approx_6m_lengths = round(d.quantity_metres / 6)
    if used_reference:
        res.notes.append(f"Reference values: {std['source_note']}")

    # ---------------------------------------------------------------- quantity unit ambiguity
    if unit_assumed and m.quantity is not None:
        cands = [f"{m.quantity:g} tonnes"]
        if d.kg_per_m:
            alt_m = m.quantity * d.kg_per_m / 1000
            alt_l = m.quantity * 6 * d.kg_per_m / 1000
            cands += [f"{m.quantity:g} metres (~{alt_m:.1f} t)", f"{m.quantity:g} x 6 m lengths (~{alt_l:.1f} t)"]
        flags.append(Flag(
            code="QTY_UNIT_MISSING", severity=Severity.CRITICAL, field="quantity",
            message=(f"Quantity {m.quantity:g} has no unit. The unit changes the supplier type: a few tonnes is a dealer/stockist order, "
                     "hundreds of tonnes is a mill-direct order."),
            candidates=cands,
            assumption=(f"Assumed {m.quantity:g} {cfg.default_unit}"
                        + (f" (~{d.quantity_metres:,} m, ~{d.approx_6m_lengths:,} x 6 m lengths)" if d.quantity_metres else "")
                        + "."),
            action="Confirm the quantity unit."))

    nm = NormalisedMaterial(
        original=m, location=parse_location(m.location_raw), spec=spec, resolved=res,
        quantity_tonnes=d.quantity_tonnes, unit_assumed=unit_assumed, derived=d, flags=flags)
    nm.search_interpretations = build_interpretations(nm)
    return nm


def build_interpretations(nm: NormalisedMaterial) -> list[str]:
    """Search-ready descriptions. Primary reading first; alternates follow. Max 3."""
    r, s = nm.resolved, nm.spec
    std = (r.standard or "IS 1239").replace(" (Part 1)", "")
    proc = "ERW pipe"
    out: list[str] = []
    if r.dn:
        ref = load_standards()["sizes"].get(r.dn)
        nominal_od = ref["od"] if ref else None
        base = f"{proc} {r.dn} NB"
        if r.od_mm and r.wall_mm:
            out.append(f"{base} {r.od_mm:g} x {r.wall_mm:g} mm {std}")          # primary reading, as resolved
        if s.bare_mm and s.bare_mm == int(s.bare_mm):
            out.append(f"MS ERW pipe {s.bare_mm:g} mm OD")                       # the alternate "OD" reading
        if ref and r.wall_mm and any(f.code == "WALL_NOT_IN_STANDARD" for f in nm.flags):
            walls = available_walls(ref)
            series = min(walls, key=lambda k: abs(walls[k] - r.wall_mm))
            out.append(f"{base} {series} class {std} {walls[series]:g} mm")      # nearest real IS 1239 series
        if nominal_od and r.od_mm and abs(nominal_od - r.od_mm) > 0.05:
            out.append(f"{base} {nominal_od:g} mm OD {std} heavy" if r.wall_mm else f"{base} {nominal_od:g} mm {std}")
        if r.class_meaning:
            out.append(f"{base} {r.class_meaning} class {std}"
                       + (f" {r.wall_mm:g} mm" if r.wall_mm else ""))
        else:
            out.append(f"{base} {std}")
    seen, uniq = set(), []
    for q in out:
        if q not in seen:
            seen.add(q)
            uniq.append(q)
    return uniq[:3]
