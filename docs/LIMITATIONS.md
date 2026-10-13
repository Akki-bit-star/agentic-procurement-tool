# Known limitations and possible improvements

Honest list, roughly in order of how much they affect a purchasing decision.

## Limitations

1. **The committed demo ran in rules-only mode (no LLM calls).** No funded LLM key was available when it was recorded, so the
   demo is a deterministic workflow with rule-driven adaptive control flow. The model-directed **agent mode** (`--agent`) and the
   two LLM stages (candidate labelling, quote selection) are implemented and tested with a scripted fake model and a mocked HTTP
   transport (tool-call parsing, rate-limit retry, circuit breaker, evidence-gate feedback, budgets, grounding), but have **not
   been run against a live provider**. Run `procure llm-check --llm <preset>` to verify a provider, then `--agent`.
   Expect more recall and better names with a capable model; the ranking logic does not change. Small free-tier models may
   follow the tool protocol less reliably — the rules backstop exists for that reason.
2. **Bot-blocked sites.** Roughly a third of vendor pages return 403 or are JS-rendered. The tool honours robots.txt, does not
   disguise its user agent and does not retry blocked hosts, so those vendors stay snippet-only (lower match class /
   confidence) or "location not established". A headless-browser fetcher or a contact-data API would recover many of them.
3. **Self-declared facts.** Manufacturer vs trader, capacity, certifications and "BIS licensed" are the vendor's own wording.
   BIS licence numbers are not looked up (no public machine-readable register was integrated) — this is the single most valuable
   missing verification for IS 1239 purchases.
4. **Evidence is mostly web-snippet and landing-page text.** No datasheets/PDF catalogues are parsed (PDF links are skipped), so
   wall-thickness tables inside PDFs are missed. A PDF text extractor in the fetcher is a small addition.
5. **Regex signals.** Size / wall / standard detection is pattern-based. It handles NB, DN, inch and OD forms, ranges and table
   rows, but unusual notations (e.g. `2"NB`, `60.3x5.54`, fractions in other layouts, non-English pages) can be missed or, rarely,
   mismatched. Misses lower a vendor's class; they do not create false matches because EXACT needs size + wall/series + standard
   in one quote.
6. **Geography needs an address.** Vendors whose address sits on a page that could not be fetched are reported as
   "location not established" rather than guessed. Ahmedabad coverage depends on Google-Maps results plus own-site addresses.
7. **Global tier is shallow.** Overseas vendors are assessed for export / India mentions, MOQ and equivalent standards only. Landed
   cost, duty, and the applicability of Indian quality-control orders for imported pipe are listed as checks, **not** evaluated.
8. **Search-quota-driven coverage.** Defaults use ≈20–30 search calls for three materials. More queries per tier or a second search
   provider would increase recall. Results from one engine are not exhaustive.
9. **Large-volume feasibility is an inference.** It combines vendor type, stated capacity/stock, and the tonnage; no vendor has
   confirmed capacity, lead time or price. Tonnage vs truck/container loads is not modelled.
10. **Name quality for some vendors** is limited to what titles, `og:site_name` and map listings say; some map listings are
    keyword-stuffed.
11. **No persistence for the web API.** Runs live in memory (CLI outputs are the durable record); there is no auth, so the API is for
    local use.
12. **The IS 1239 reference table** covers DN 15–150 for Part 1 (the sizes used here). Other standards (IS 3589, IS 1161, ASTM A53) are
    recognised as "different standard" but their dimension tables are not bundled.

## What I would do with more time

* Run the demo with the LLM enabled and compare against the rules-only baseline (recall, naming, false-positive rate).
* BIS licence lookup + ISI-mark verification; GSTIN/MCA company checks to confirm manufacturer status and registered address.
* PDF catalogue parsing; headless fetching for JS sites (still respecting robots.txt).
* An RFQ generator: draft the technical clarification / RFQ per vendor from the match gaps and unresolved list.
* A landed-cost module for global vendors (freight, duty, port) and a truck-load model for domestic delivery.
* An evaluation harness: a labelled set of vendors/pages to measure the evidence gate, the classifier and the geography rules.
* Persisted run history and diffing between runs in the UI.
