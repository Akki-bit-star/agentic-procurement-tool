import json
from pathlib import Path

from procure.assess import classify_match
from procure.config import load_config
from procure.models import Evidence, MatchClass, ProcurementRequest
from procure.normalize import normalise
from procure.signals import analyze_vendor_text, build_patterns

ROOT = Path(__file__).resolve().parent.parent
CFG = load_config()


def nm(i):
    req = ProcurementRequest(**json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8")))
    return normalise(req.materials[i], CFG)


def ev(i, quote, url="https://v.example/p", kind="vendor_site"):
    return Evidence(id=f"e{i}", vendor_id="v", claim_type="product_match", claim="c", quote=quote, url=url, source_kind=kind)


def test_row_attributed_to_another_standard_is_never_exact():
    """Regression: 'OfBusiness' got EXACT for M-02 from '48.3 mm OD x 3.2 mm (medium class, IS 1161)'."""
    m2 = nm(1)   # 40 mm / Class B -> DN40, 48.3 x 3.2, IS 1239 medium
    quote = ("Scaffolding pipes: 48.3 mm OD x 3.2 mm (medium class, IS 1161) - standard for scaffolding. "
             "Grades: Fe 330 (IS 1239), E250 (IS 1161)")
    cls, reasons, _, _ = classify_match([ev(1, quote)], m2, build_patterns(m2))
    assert cls == MatchClass.NEAR
    assert any("different standard" in r for r in reasons)


def test_clean_row_with_required_standard_is_exact():
    m1 = nm(0)   # DN50 60.3 x 5.5 IS 1239
    evs = [ev(1, "ERW pipe | Size 50 NB | 60.3 mm OD | Thickness 5.5 mm | Heavy class conforming to IS 1239")]
    cls, _, _, _ = classify_match(evs, m1, build_patterns(m1))
    assert cls == MatchClass.EXACT


def test_exact_needs_the_standard_on_the_same_page():
    m1 = nm(0)
    evs = [ev(1, "Size 50 NB | 60.3 mm OD | Thickness 5.5 mm", url="https://a.example/x"),
           ev(2, "Conforming to IS 1239", url="https://b.example/y")]       # standard on a different site
    cls, _, _, _ = classify_match(evs, m1, build_patterns(m1))
    assert cls == MatchClass.NEAR


def test_seamless_listing_is_not_an_exact_match_for_an_erw_requirement():
    """Regression: a stockist's 'IS 1239 Galvanized Seamless Pipe, 1.5 inch, Medium Class' was ranked EXACT for 'MS ERW, Class B'."""
    m2 = nm(1)
    quote = "IS 1239 Galvanized Seamless Pipe, 1.5 inch, Medium Class (SCH 40 Equiv.) | Mild Steel Seamless Round Pipe"
    cls, reasons, _, _ = classify_match([ev(1, quote)], m2, build_patterns(m2))
    assert cls == MatchClass.NEAR and any("seamless" in r or "ERW" in r for r in reasons)


def test_page_that_never_says_erw_cannot_prove_an_erw_match():
    m2 = nm(1)
    cls, _, _, _ = classify_match([ev(1, "IS 1239 pipe 40 NB medium class 3.2 mm")], m2, build_patterns(m2))
    assert cls == MatchClass.NEAR
    cls, _, _, _ = classify_match([ev(1, "IS 1239 ERW pipe 40 NB medium class 3.2 mm")], m2, build_patterns(m2))
    assert cls == MatchClass.EXACT


def test_nearest_series_wall_only_is_near_with_reason():
    m1 = nm(0)
    evs = [ev(1, "ERW pipe 50 NB IS 1239 heavy class thickness 4.5 mm")]
    cls, reasons, _, _ = classify_match(evs, m1, build_patterns(m1))
    assert cls == MatchClass.NEAR and any("nearest IS 1239 wall" in r for r in reasons)


def test_manufacturer_must_be_self_declared():
    assert not analyze_vendor_text("Buy IS 1239 pipes from APL Apollo, Tata, Jindal manufacturers at best prices").manufacturer
    assert analyze_vendor_text("We are a leading manufacturer of ERW pipes").manufacturer
    assert analyze_vendor_text("Manufacturer & Supplier of MS pipes").manufacturer
    assert analyze_vendor_text("Visit our plant in Naroda").manufacturer


def test_price_information_sites_are_flagged_as_platforms():
    s = analyze_vendor_text("MS ERW Round Pipe Price in India Today. Buy at best B2B rates on OfBusiness")
    assert s.platform and not s.manufacturer
