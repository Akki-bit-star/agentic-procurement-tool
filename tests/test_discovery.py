from procure.agents.discovery import (name_from_own_site, name_from_title, seller_from_marketplace_url,
                                      tier_queries, drafts_from_results)
from procure.config import load_config
from procure.context import RunContext
from procure.models import MaterialInput, SearchResult, Tier
from procure.normalize import normalise
from procure.state import State
from procure.geo import find_places, tier_from_place, registrable_domain


def test_descriptive_titles_are_not_used_as_vendor_names():
    assert name_from_own_site("ERW Pipe Size Chart in mm & Inches", "tubesandvalves.com") == "Tubesandvalves"
    assert name_from_own_site("MS ERW Round Pipe Price in India Today", "everestmetal.in") == "Everestmetal"
    assert name_from_title("Shree Ganesh Steel Tubes - ERW Pipe Manufacturer", "ganeshtubes.com")


def test_corporate_suffix_title_segment_is_a_company_name():
    assert name_from_own_site("Tianjin Metal Pipe Co., Ltd - ERW steel pipe exporter", "tjmetal.com") == "Tianjin Metal Pipe Co., Ltd"


def test_marketplace_seller_from_url():
    assert seller_from_marketplace_url("https://sianosteel.en.made-in-china.com/product/x", "made-in-china.com") == "Sianosteel"
    assert seller_from_marketplace_url("https://www.indiamart.com/shahpipes/", "indiamart.com") == "Shahpipes"
    assert seller_from_marketplace_url("https://www.indiamart.com/proddetail/ms-pipe-123.html", "indiamart.com") is None
    assert seller_from_marketplace_url("https://www.alibaba.com/countrysearch/CN/china-48.3-pipe.html", "alibaba.com") is None


def test_unnamed_marketplace_and_non_vendor_results_are_excluded_with_reason():
    cfg = load_config()
    nm = normalise(MaterialInput(id="M", description_raw="ERW pipe, DN 50, 60.3 x 3.6 mm, IS 1239", quantity=1, unit="t"), cfg)
    st = State([nm])
    rs = [SearchResult(title="China 48.3 Pipe China Trade", url="https://www.alibaba.com/countrysearch/CN/china-48.3-pipe.html",
                       snippet="ERW pipe suppliers"),
          SearchResult(title="IS 1239-1 (2004): Steel Tubes", url="https://law.resource.org/pub/in/bis/S10/is.1239.1.b.2004.pdf",
                       snippet="steel tubes standard"),
          SearchResult(title="Top 10 ERW pipe manufacturers in India", url="https://blog.example/top10", snippet="ERW pipe list"),
          SearchResult(title="Acme Tubes Pvt Ltd", url="https://www.acmetubes.example/erw", snippet="ERW pipe manufacturer")]
    drafts = drafts_from_results(rs, cfg, False, RunContext(cfg), st, Tier.INDIA_OTHER, "M")
    assert [d.name for d in drafts] == ["Acme Tubes Pvt Ltd"]
    assert len(st.excluded) == 3 and all(x["reason"] for x in st.excluded)


def test_global_queries_do_not_use_the_indian_standard():
    cfg = load_config()
    nm = normalise(MaterialInput(id="M", description_raw="ERW pipe, DN 50, 60.3 x 5.5 mm, IS 1239", quantity=1, unit="t"), cfg)
    for q in tier_queries(nm, Tier.GLOBAL):
        assert "IS 1239" not in q


def test_places_text_must_be_a_location_not_a_shipping_destination():
    # "export to India" is a destination; a Chinese vendor must not become Indian because of it
    assert not any(p.locative or p.in_address_context for p in find_places("We export to India, UAE and Vietnam. MOQ 25 tons.")
                   if p.country == "India")
    assert any(p.locative and p.city == "Ahmedabad" for p in find_places("Manufacturer of pipes in Ahmedabad"))
    assert tier_from_place("Ahmedabad", "India") == Tier.AHMEDABAD
    assert tier_from_place("Mumbai", "India") == Tier.INDIA_OTHER
    assert tier_from_place(None, "China") == Tier.GLOBAL
    assert tier_from_place(None, None) == Tier.UNRESOLVED


def test_registrable_domain():
    assert registrable_domain("https://www.shahpipes.co.in/x") == "shahpipes.co.in"
    assert registrable_domain("https://sianosteel.en.made-in-china.com/p") == "made-in-china.com"
