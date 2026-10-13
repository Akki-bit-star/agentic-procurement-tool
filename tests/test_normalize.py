import json
from pathlib import Path

import pytest

from procure.config import load_config
from procure.models import MaterialInput, ProcurementRequest, Provenance
from procure.normalize import kg_per_m, normalise, parse_spec

ROOT = Path(__file__).resolve().parent.parent
CFG = load_config()


def mats():
    req = ProcurementRequest(**json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8")))
    return {m.id: normalise(m, CFG) for m in req.materials}


def codes(nm):
    return {f.code for f in nm.flags}


def test_original_input_is_preserved():
    for nm in mats().values():
        assert nm.original.description_raw
    assert mats()["M-01"].original.description_raw == "ERW pipe, DN 50, 60.3 × 5.5 mm, IS 1239"


def test_parse_dn_dims_standard():
    s = parse_spec("ERW pipe, DN 50, 60.3 × 5.5 mm, IS 1239")
    assert (s.dn, s.od_mm, s.wall_mm) == (50, 60.3, 5.5)
    assert s.standards == ["IS 1239"] and s.process == "ERW"
    assert s.bare_mm is None


def test_parse_bare_mm_and_class():
    s = parse_spec("40 mm MS ERW, Class B pipe")
    assert s.bare_mm == 40 and s.dn is None and s.material == "MS" and s.pipe_class == "B"


def test_quantity_unit_flagged_and_assumed_tonnes_for_all():
    for nm in mats().values():
        assert "QTY_UNIT_MISSING" in codes(nm)
        assert nm.unit_assumed and nm.quantity_tonnes == nm.original.quantity


def test_m01_wall_not_in_is1239_is_flagged_not_changed():
    nm = mats()["M-01"]
    assert "WALL_NOT_IN_STANDARD" in codes(nm)
    assert nm.resolved.wall_mm == 5.5                       # NOT silently changed to 4.5
    flag = next(f for f in nm.flags if f.code == "WALL_NOT_IN_STANDARD")
    assert any("Sch 80" in c for c in flag.candidates)


def test_m02_bare_mm_class_b_ambiguities():
    nm = mats()["M-02"]
    assert {"SIZE_BARE_MM", "CLASS_MEANING", "STANDARD_NOT_STATED"} <= codes(nm)
    assert nm.resolved.dn == 40 and nm.resolved.basis["dn"] == Provenance.ASSUMED
    assert nm.resolved.wall_mm == 3.2 and nm.resolved.basis["wall_mm"] == Provenance.REFERENCE
    assert nm.spec.bare_mm == 40                             # original reading retained
    assert any("MS ERW pipe 40 mm OD" == q for q in nm.search_interpretations)  # alternate reading searched


def test_m03_od_is_the_standards_max_not_an_error():
    nm = mats()["M-03"]
    flag = next(f for f in nm.flags if f.code == "OD_AT_LIMIT")
    assert flag.severity.value == "INFO"                    # valid per BIS: DN80 medium/heavy OD range 88.0-89.5
    assert nm.resolved.od_mm == 89.5 and "WALL_NOT_IN_STANDARD" not in codes(nm)
    assert nm.resolved.class_meaning == "heavy"             # 4.8 mm = IS 1239 heavy for DN80


def test_m01_od_within_standard_range_not_flagged():
    assert not {"OD_AT_LIMIT", "OD_MISMATCH"} & codes(mats()["M-01"])   # 60.3 is inside 59.7-60.8


def test_derived_mass_prefers_standard_table_over_formula():
    assert kg_per_m(60.3, 5.5) == pytest.approx(7.433, abs=0.01)
    m1, m2, m3 = (mats()[k] for k in ("M-01", "M-02", "M-03"))
    assert m1.derived.provenance == Provenance.DERIVED      # 5.5 mm is not in the standard -> formula
    assert m1.derived.quantity_metres == pytest.approx(1000 * 1000 / 7.433, rel=0.01)
    assert m2.derived.kg_per_m == 3.56 and m2.derived.provenance == Provenance.REFERENCE   # BIS Table 4, DN40 medium
    assert m3.derived.kg_per_m == 9.90 and m3.derived.provenance == Provenance.REFERENCE   # BIS Table 5, DN80 heavy


def test_reference_table_matches_bis_for_demo_sizes():
    from procure.config import load_standards
    s = load_standards()["sizes"]
    assert (s[40]["medium"], s[50]["heavy"], s[80]["heavy"]) == (3.2, 4.5, 4.8)
    assert s[80]["od_range_mh"] == [88.0, 89.5]


def test_metres_and_lengths_units_convert():
    m = MaterialInput(id="X", description_raw="ERW pipe, DN 50, 60.3 x 3.6 mm, IS 1239", quantity=1000, unit="m")
    nm = normalise(m, CFG)
    assert not nm.unit_assumed and "QTY_UNIT_MISSING" not in codes(nm)
    assert nm.quantity_tonnes == pytest.approx(1000 * kg_per_m(60.3, 3.6) / 1000, rel=0.01)


def test_search_interpretations_capped_and_unique():
    for nm in mats().values():
        assert 1 <= len(nm.search_interpretations) <= 3
        assert len(set(nm.search_interpretations)) == len(nm.search_interpretations)
