"""End-to-end pipeline test with a stub search provider and canned pages: no network, no keys."""
import json
from pathlib import Path

import pytest

from procure.config import load_config
from procure.fetch import Fetcher
from procure.models import MatchClass, Page, ProcurementRequest, Provenance, SearchResult, Tier, Confidence
from procure.pipeline import NeedsClarification, run_pipeline
from procure.providers import search as search_mod
from procure.report import to_csv, to_markdown
from procure.signals import quote_in_text

ROOT = Path(__file__).resolve().parent.parent

GANESH_URL = "https://www.ganeshtubes.example/erw-pipes"
SAI_URL = "https://www.saisteel.example/about"
TJ_URL = "https://www.tjmetal.example/erw"
PAGES = {
    GANESH_URL: ("Shree Ganesh Steel Tubes\nWe are manufacturer of ERW pipes conforming to IS 1239 (Part 1).\n"
                 "Size 50 NB | 60.3 mm OD | Thickness 5.5 mm | Heavy class\n"
                 "BIS licensed (ISI mark). Production capacity 5000 MT per month.\n"
                 "Address: Plot 12, GIDC Naroda, Ahmedabad, Gujarat 382330\n"
                 "Phone +91 98250 12345 | sales@ganeshtubes.example\nWe deliver all over India."),
    "https://www.ganeshtubes.example/": ("Shree Ganesh Steel Tubes\nERW pipes manufacturer. Plant: Naroda GIDC, Ahmedabad, Gujarat 382330.\n"
                                         "Contact sales@ganeshtubes.example for bulk orders and test certificates."),
    SAI_URL: ("Sai Steel Industries\nTraders and dealers of MS ERW pipes and GI pipes.\nRegistered office address: 14 Steel Market Road, "
              "Mumbai, Maharashtra 400001\nReady stock of 40 NB and 50 NB pipes. IS 1239 medium and heavy."),
    "https://www.saisteel.example/": "Sai Steel Industries - dealers of pipes. Address: 14 Steel Market Road, Mumbai, Maharashtra 400001. Stockist.",
    TJ_URL: ("Tianjin Metal Pipe Co., Ltd - ERW steel pipe exporter\nERW steel pipe 60.3 mm x 5.5 mm ASTM A53 / EN 10255.\n"
             "Address: No. 5 Jinnan Road, Tianjin, China\nWe export to India, UAE and Vietnam. MOQ 25 tons. FOB Tianjin port.\n"
             "ISO 9001 certified. Mill test certificate EN 10204 3.1 provided."),
    "https://www.tjmetal.example/": "Tianjin Metal Pipe Co., Ltd. Address: No. 5 Jinnan Road, Tianjin, China. ERW pipe factory, exporter.",
}


class StubProvider:
    name = "serper"

    def search(self, query, *, country, num):
        if country is None:  # global tier
            return [SearchResult(title="Tianjin Metal Pipe Co., Ltd - ERW steel pipe exporter", url=TJ_URL, position=1,
                                 snippet="ERW steel pipe 60.3 mm x 5.5 mm ASTM A53. We export to India. Tianjin, China.")]
        return [
            SearchResult(title="Shree Ganesh Steel Tubes - ERW Pipe Manufacturer Ahmedabad", url=GANESH_URL, position=1,
                         snippet="ERW pipe 50 NB IS 1239 heavy class manufacturer in Ahmedabad."),
            SearchResult(title="MS ERW Pipe 50 NB at Rs 62/kg in Ahmedabad | ID: 998877",
                         url="https://www.indiamart.com/proddetail/ms-erw-pipe-998877.html", position=2,
                         snippet="MS ERW Pipe, IS 1239, size 50 NB. Sold by Sai Steel Industries in Ahmedabad."),
            SearchResult(title="Shree Ganesh Steel Tubes", url="https://www.indiamart.com/shree-ganesh/", position=3,
                         snippet="ERW pipe manufacturers. by Shree Ganesh Steel Tubes in Ahmedabad."),
            SearchResult(title="IS 1239 steel pipe chart", url="https://www.scribd.com/document/123/pipe-chart", position=4,
                         snippet="pipe weight chart IS 1239"),
            SearchResult(title="Sai Steel Industries - MS pipes", url=SAI_URL, position=5, snippet="Dealers of MS ERW pipes IS 1239."),
        ]

    def places(self, query, *, country, num):
        return [SearchResult(title="Shree Ganesh Steel Tubes", url="https://www.ganeshtubes.example", position=1, snippet="Pipe manufacturer",
                             address="Plot 12, GIDC Naroda, Ahmedabad, Gujarat 382330", phone="+91 98250 12345",
                             website="https://www.ganeshtubes.example")]


@pytest.fixture()
def result(tmp_path, monkeypatch):
    monkeypatch.setitem(search_mod.PROVIDERS, "serper", lambda: StubProvider())

    def fake_fetch(self, url):
        txt = PAGES.get(url)
        return Page(url=url, ok=True, status=200, text=txt) if txt else Page(url=url, ok=False, error="HTTP 404")

    monkeypatch.setattr(Fetcher, "_fetch_network", fake_fetch)
    monkeypatch.setattr(Fetcher, "_polite_wait", lambda self, host: None)
    cfg = load_config(overrides={"llm.provider": "none"})
    req = ProcurementRequest(**json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8")))
    return run_pipeline(req, cfg, cache_dir=tmp_path / "cache", cache_mode="auto")


def vendor(res, needle):
    return next(v for v in res.vendors if needle.lower() in v.name.lower())


def test_three_tiers_populated_and_correct(result):
    assert vendor(result, "Ganesh").tier == Tier.AHMEDABAD and vendor(result, "Ganesh").geo_status == "VERIFIED"
    assert vendor(result, "Tianjin").tier == Tier.GLOBAL
    assert vendor(result, "Sai Steel").tier == Tier.INDIA_OTHER


def test_marketplace_claim_vs_site_conflict_is_recorded_and_resolved_by_reliability(result):
    sai = vendor(result, "Sai Steel")
    assert sai.conflicts, "marketplace said Ahmedabad, own site says Mumbai"
    assert sai.city == "Mumbai"


def test_duplicates_are_merged(result):
    assert sum("ganesh" in v.name.lower() for v in result.vendors) == 1
    assert vendor(result, "Ganesh").merged_from


def test_every_tier_runs_its_own_queries(result):
    """Regression: coverage was once counted across tiers, so later tiers stopped after one query."""
    for d in result.discovery:
        assert len(d["queries"]) >= 3, d
    # tiers with few candidates reformulate (round 2) instead of giving up
    assert any(d["rounds"] == 2 for d in result.discovery)


def test_non_vendor_result_excluded(result):
    assert any("scribd" in x["url"] for x in result.excluded_candidates)
    assert not any("scribd" in (v.domain or "") for v in result.vendors)


def test_exact_match_requires_size_wall_standard_in_evidence(result):
    a = vendor(result, "Ganesh").assessments["M-01"]
    assert a.match_class == MatchClass.EXACT and a.confidence == Confidence.HIGH
    assert a.shortlisted and a.rank == 1
    # M-02 (DN40) is not on Ganesh's page -> must not be EXACT
    m2 = vendor(result, "Ganesh").assessments.get("M-02")
    assert m2 is None or m2.match_class != MatchClass.EXACT


def test_other_standard_gives_near_not_exact_and_says_why(result):
    # The exporter lists 60.3 x 5.5 mm but to ASTM A53 / EN 10255, not IS 1239 -> NEAR, with the reason stated.
    a = vendor(result, "Tianjin").assessments["M-01"]
    assert a.match_class == MatchClass.NEAR
    assert any("not IS 1239" in r for r in a.match_reasons)


def test_one_passage_cannot_vouch_for_itself(result):
    """Evidence is merged per distinct quote, so repeated windows of one passage are not 'independent' support."""
    quotes = [(e.url, " ".join(e.quote.split()).lower()) for e in result.evidence]
    assert len(quotes) == len(set(quotes))
    assert any(len(e.claim_types) > 1 for e in result.evidence)


def test_conflicts_listed_once_and_website_is_site_root(result):
    sai = vendor(result, "Sai Steel")
    assert len(sai.conflicts) == len(set(sai.conflicts)) == 1
    assert sai.contact.website == "https://www.saisteel.example"
    assert sai.assessments["M-01"].confidence != Confidence.HIGH     # unresolved conflict caps confidence


def test_export_to_india_does_not_make_a_vendor_indian(result):
    tj = vendor(result, "Tianjin")
    assert tj.country == "China" and tj.tier == Tier.GLOBAL
    assert any(u.startswith("import check") for u in tj.assessments["M-01"].unresolved)


def test_every_evidence_quote_exists_in_a_recorded_source(result):
    texts = {}
    for u, t in PAGES.items():
        texts.setdefault(u, []).append(t)
    assert result.evidence
    for e in result.evidence:
        sources = texts.get(e.url, [])
        # snippets / places text are also valid sources: rebuild them from the stub
        sources += [f"{r.title}\n{r.snippet}" for r in StubProvider().search("x", country="in", num=10) + StubProvider().search("x", country=None, num=10)]
        sources += [" ".join(filter(None, [p.title, p.address, p.phone, p.website])) for p in StubProvider().places("x", country="in", num=5)]
        assert any(quote_in_text(e.quote, s) for s in sources), (e.id, e.quote)


def test_nothing_unsourced_is_presented_as_fact(result):
    for v in result.vendors:
        assert v.facts["price"].provenance == Provenance.NEEDS_RFQ
        assert v.facts["lead_time"].provenance == Provenance.NEEDS_RFQ
        for key, f in v.facts.items():
            if f.provenance == Provenance.SOURCED and key not in ("vendor_type",):
                assert f.evidence_ids, f"{v.name}.{key} is SOURCED but cites no evidence"
                assert all(i in {e.id for e in result.evidence} for i in f.evidence_ids)


def test_unit_assumption_visible_in_report(result):
    md = to_markdown(result)
    assert "QTY_UNIT_MISSING" in md and "WALL_NOT_IN_STANDARD" in md and "SIZE_BARE_MM" in md
    assert "[NEEDS_RFQ]" in md
    assert "material_id" in to_csv(result)


def test_evidence_gate_rejects_fabricated_quote():
    from procure.models import Evidence
    from procure.state import State
    st = State([])
    st.add_source_text("https://a.example", "We make ERW pipe in Surat.")
    good = Evidence(id="1", vendor_id="v", claim_type="location", claim="c", quote="ERW pipe in Surat", url="https://a.example")
    fake = Evidence(id="2", vendor_id="v", claim_type="certification", claim="c", quote="BIS licence CM/L-123456", url="https://a.example")
    assert st.gate(good) and not st.gate(fake)
    assert st.dropped_claims and st.dropped_claims[0]["claim"] == "c"


def test_strict_mode_stops_on_critical_ambiguity(tmp_path):
    cfg = load_config(overrides={"llm.provider": "none"})
    req = ProcurementRequest(**json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8")))
    with pytest.raises(NeedsClarification) as ei:
        run_pipeline(req, cfg, cache_dir=tmp_path, strict=True)
    assert any(f["code"] == "QTY_UNIT_MISSING" for f in ei.value.flags)
