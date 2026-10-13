# Parameters, ranking, confidence and assumptions

All numbers below live in `config/default.yaml` (non-secret) and can be overridden per run. Nothing is hard-coded in the
ranking code.

## 1. Input parameters

Per line item (`demo/input.json`):

| Field | Meaning |
|---|---|
| `id` | stable id, used everywhere in the output |
| `description_raw` | exactly what the buyer typed — **never modified** |
| `quantity`, `unit` | `unit` may be `null`; the tool then assumes `default_unit` (tonnes) and logs it |
| `location_raw` | procurement location; Ahmedabad is the tier-1 anchor |
| `standard_hint` | optional extra standard text |

Run-level: `default_unit`, `strict` (stop on CRITICAL ambiguity instead of assuming), search/LLM provider, cache mode
(`auto` / `replay` / `refresh`).

## 2. Search constraints (quota protection)

| Parameter | Default | Purpose |
|---|---|---|
| `search.max_search_calls_total` | 60 | hard cap on paid search calls per run |
| `search.max_queries_per_material_per_tier` | 3 | round-1 queries; round 2 adds one relaxed query if the tier is thin |
| `search.max_places_calls_per_material` | 1 | Google-Maps lookups (shared by all materials) |
| `search.max_vendors_verified_per_material_per_tier` | 8 | page-fetch budget; the rest stay snippet-only leads |
| `search.max_pages_fetched_per_vendor` / `max_followup_pages_per_vendor` | 2 / 3 | pages per vendor; follow-ups only when no address was found |
| `shortlist.per_tier_per_material` | 5 | shortlist size per material per tier |

Cache hits are free and never counted, so repeated runs do not consume quota.

## 3. Technical match classes

Derived only from **quote-backed signals** (size, wall, standard, series), never from a model's opinion.

| Class | Rule |
|---|---|
| **EXACT** | product evidence **and** size **and** required wall/series appear *together in one source quote* (e.g. a table row) **and** the required standard (IS 1239) is stated |
| **NEAR** | size (or a range covering it, or an ambiguous "50 mm") is evidenced but something differs: other standard (IS 3589 / ASTM / EN), only the nearest IS 1239 wall, wall not confirmed, or no standard. The reasons are listed. |
| **CATEGORY** | supplies ERW / steel pipe or names a pipe standard, but no evidence for this size |
| **UNVERIFIED** | no quote shows a matching product — listed for follow-up, **never shortlisted** |

Because M-01's 5.5 mm wall is not an IS 1239 thickness, EXACT requires a source that literally lists that wall for DN 50;
vendors showing only the 4.5 mm heavy series are NEAR, with the reason stated.

## 4. Ranking score (0–1)

`score = Σ weight × component`

| Component | Weight | How it is computed |
|---|---|---|
| technical_match | **0.30** | EXACT 1.0 · NEAR 0.6 · CATEGORY 0.3 · UNVERIFIED 0.1 |
| bulk_relevance | **0.20** | manufacturer + stated capacity 1.0 · manufacturer 0.7 · stockist with stock 0.5 · stockist 0.4 · trader 0.35 · marketplace listing 0.25 · unknown 0.2; **×0.75** for stockists/traders/listings when the order ≥ `large_order_tonnes` (100 t), because mill-direct is the realistic route |
| geography_delivery | **0.20** | Ahmedabad verified 1.0 (claimed only 0.6) · India: Ahmedabad/Gujarat delivery stated 0.9, Gujarat-based 0.8, pan-India stated 0.7, otherwise 0.4 (×0.8 if location not verified) · Global: export-to-India stated 0.7, export mentioned 0.45, none 0.15 |
| certification | **0.15** | BIS/ISI 1.0 · test certificate 0.6 · ISO 9001/14001/45001 0.5 · (global only) international standard named 0.4 |
| source_quality | **0.10** | best source reliability (vendor site 0.9 · maps 0.6 · marketplace 0.4 · unknown 0.2) +0.2 if ≥2 independent domains |
| contactability | **0.05** | website + phone/email 1.0 · one of them 0.5 · none 0 |

Ranking is **within a (material, tier)**; the three tiers are never mixed in one list.

## 5. Confidence model (separate from the score)

A vendor can score well and still be low-confidence if everything rests on one marketplace line.

| Level | Rule |
|---|---|
| **HIGH** | match is EXACT or NEAR **and** the vendor's own site / maps evidences ≥2 *kinds* of fact (standard / size / wall / series) **or** ≥2 pages **and** location VERIFIED **and** no conflicts |
| **MEDIUM** | EXACT/NEAR with a verified or claimed location but weaker support (marketplace/snippet only, one kind of fact, or a conflict); or CATEGORY with verified location and own-site evidence |
| **LOW** | everything else (category-level, unverified, unresolved location) |

The reasons are printed beside every confidence value.

## 6. Geography rules

* **Ahmedabad** needs an address / branch / warehouse / plant in Ahmedabad (or its listed industrial localities) in a
  quote from the vendor's own site or a map listing → `VERIFIED`. A marketplace-only claim → `CLAIMED` (shown, scored
  lower, never HIGH).
* A place counts only as a **location** ("in/from/at X", or in an address line), not as a **destination** ("we export to India").
* **India outside Ahmedabad**: Indian address elsewhere. **Global**: non-Indian address. If a marketplace and the vendor's
  own site disagree, the higher-reliability source wins and the conflict is recorded.
* No location evidence → `UNRESOLVED` (reported separately, never forced into a tier).

## 7. Key assumptions

1. **Quantity unit = tonnes** (the input has none). The metre / 6 m-length equivalents are *derived* and shown. If the unit
   were metres, 1,000 m of DN 50 is ≈ 7 t — a dealer order, not a mill order.
2. **IS 1239 reference values** come from the BIS standard text (IS 1239 Part 1:2004, Tables 3–5; verified against the public
   copy on 2026-10-13); the nominal OD used for search terms is trade convention.
3. "40 mm" is read as **DN 40**, "Class B" as IS 1239 **medium** (trade shorthand; the standard itself says light/medium/heavy).
   Alternate readings are searched too.
4. M-01's 5.5 mm wall is **kept as written** and flagged; the nearest IS 1239 series (heavy, 4.5 mm) is searched as an alternate.
5. Manufacturer / trader status is the vendor's own wording (self-declared). BIS licence numbers are never inferred.
6. Absence of evidence is reported as "not found", never as a negative fact.
7. Prices, lead times, stock and MOQ are not collected — they are `NEEDS_RFQ`.
