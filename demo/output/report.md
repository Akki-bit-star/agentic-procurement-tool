# Procurement shortlist — Ahmedabad, Gujarat
_Generated 2026-10-13T10:21:24+00:00 · search: serper · LLM: rules-only · cache: replay · config 2872791bcc4a · calls used: {'search': '0/60', 'llm': '0/120'}_

> **How to read this.** Every vendor fact is labelled `[SOURCED]` (backed by a verbatim quote + URL), `[DERIVED]` (calculated), `[REFERENCE]` (BIS table), `[ASSUMED]` (an assumption you can override) or `[NEEDS_RFQ]` (must be confirmed with the vendor). Prices, lead times, stock and certifications are never stated unless quoted from a source (a quote may contain an indicative price the vendor published; that is **not** a verified quotation). **Match** says how well the evidence fits the requirement (EXACT / NEAR / CATEGORY / UNVERIFIED); **confidence** says how well-supported that assessment is (own-site evidence, verified location, reachable contact, no conflicts) — a NEAR match with HIGH confidence is a *well-evidenced near match*, not a perfect one.

## 1. At a glance — top picks per material and geography

| Material | Ahmedabad vendors | India-based vendors outside Ahmedabad | International / global vendors |
|---|---|---|---|
| **M-01** ERW pipe, DN 50, 60.3 × 5.5 mm, IS 1239 | 1. **Rajsagar** — NEAR/HIGH<br>2. **Bhushantube** — NEAR/MEDIUM<br>3. **MN METAL** — NEAR/HIGH | 1. **Dealonsteel** — NEAR/MEDIUM<br>2. **Emirerristeel** — NEAR/MEDIUM<br>3. **Amco Exports** — NEAR/MEDIUM | 1. **Tianyingtai Steel Pipe** — NEAR/HIGH<br>2. **Forever Steel** — NEAR/HIGH<br>3. **Glory Steel** — NEAR/MEDIUM |
| **M-02** 40 mm MS ERW, Class B pipe | 1. **Rajsagar** — NEAR/HIGH<br>2. **Bhushantube** — NEAR/MEDIUM<br>3. **Ofbusiness** — NEAR/MEDIUM | 1. **Dealonsteel** — NEAR/MEDIUM<br>2. **Emirerristeel** — NEAR/MEDIUM<br>3. **RP Sales** — EXACT/MEDIUM | 1. **Tianyingtai Steel Pipe** — NEAR/HIGH<br>2. **Forever Steel** — NEAR/HIGH<br>3. **Glory Steel** — NEAR/MEDIUM |
| **M-03** ERW pipe, DN 80, 89.5 × 4.8 mm, IS 1239 | 1. **Rajsagar** — NEAR/HIGH<br>2. **Padmawati Traders** — NEAR/MEDIUM<br>3. **MN METAL** — NEAR/MEDIUM | 1. **Dealonsteel** — NEAR/MEDIUM<br>2. **Maxxon** — CATEGORY/MEDIUM<br>3. **Emirerristeel** — NEAR/MEDIUM | 1. **Forever Steel** — NEAR/HIGH<br>2. **Glory Steel** — NEAR/MEDIUM<br>3. **Octalsteel** — NEAR/MEDIUM |

## 2. Requirement ambiguities and assumptions (read before sending any RFQ)

**Applies to all items — STANDARD_SCOPE_NOTE:** IS 1239 (Part 1):2004 permits ERW/HFIW manufacture (cl. 6.3) and covers 6-150 mm nominal bore for water, non-hazardous gas, air and steam. Vendors quoting IS 3589 (large-diameter), IS 1161 (structural) or ASTM/API are a different scope. _Assumption [REFERENCE]: Vendors quoting another standard are classed NEAR, not EXACT._ _Ask for:_ Ask vendors for the BIS licence (ISI mark), the L/M/H marking and colour band, and a test certificate for the exact series.

### M-01 — `ERW pipe, DN 50, 60.3 × 5.5 mm, IS 1239` · qty 1000 (no unit) · Ahmedabad, Gujarat, India
- **Resolved for search** (original never overwritten): DN50, OD 60.3 mm [SOURCED], wall 5.5 mm [SOURCED], standard IS 1239 (Part 1), series n/a
- **Derived** [DERIVED]: 7.433 kg/m (formula (60.3 - 5.5) x 5.5 x 0.02466 [OD SOURCED, wall SOURCED]); 1,000 t ≈ 134,535 m ≈ 22,422 × 6 m lengths
- **WARNING · WALL_NOT_IN_STANDARD** — 5.5 mm is not an IS 1239 wall thickness for DN50 (BIS Tables 3-5: light 2.9, medium 3.6, heavy 4.5 mm). It is close to Sch 80 (ASME B36.10 family) - outside IS 1239 (5.54 mm). The requirement combines an IS 1239 reference with a wall outside that standard.
  - Interpretations considered: Sch 80 (ASME B36.10 family) - outside IS 1239: 5.54 mm; light series (2.9 mm); medium series (3.6 mm); heavy series (4.5 mm); 5.5 mm as written (custom / other standard)
  - Assumption used [ASSUMED]: Kept 5.5 mm as written. Vendors are searched for it AND for the nearest IS 1239 series; those without a 5.5 mm product are NEAR matches at best.
  - **Please confirm:** Confirm the required wall thickness (and whether IS 1239 or another standard governs).
- **CRITICAL · QTY_UNIT_MISSING** — Quantity 1000 has no unit. The unit changes the supplier type: a few tonnes is a dealer/stockist order, hundreds of tonnes is a mill-direct order.
  - Interpretations considered: 1000 tonnes; 1000 metres (~7.4 t); 1000 x 6 m lengths (~44.6 t)
  - Assumption used [ASSUMED]: Assumed 1000 tonnes (~134,535 m, ~22,422 x 6 m lengths).
  - **Please confirm:** Confirm the quantity unit.

### M-02 — `40 mm MS ERW, Class B pipe` · qty 500 (no unit) · Ahmedabad, Gujarat, India
- **Resolved for search** (original never overwritten): DN40, OD 48.3 mm [REFERENCE], wall 3.2 mm [REFERENCE], standard IS 1239 (Part 1), series medium
- **Derived** [REFERENCE]: 3.56 kg/m (IS 1239 table: DN40 medium = 3.56 kg/m (plain end); formula cross-check 3.56 kg/m); 500 t ≈ 140,449 m ≈ 23,408 × 6 m lengths
- **CRITICAL · SIZE_BARE_MM** — "40 mm" is ambiguous: Indian trade usage normally means nominal bore (DN40, OD about 48.3 mm), but it could be read as outside diameter.
  - Interpretations considered: DN40 nominal bore (OD about 48.3 mm); 40 mm outside diameter (not a standard IS 1239 OD)
  - Assumption used [ASSUMED]: Treated as DN40 nominal bore. The OD-40 mm reading is kept as an alternate search.
  - **Please confirm:** Confirm nominal bore vs outside diameter before issuing the RFQ.
- **WARNING · STANDARD_NOT_STATED** — No product standard is stated in the requirement.
  - Interpretations considered: IS 1239 (Part 1) - light/medium/heavy; IS 1161 (structural); IS 3589 (large-diameter)
  - Assumption used [ASSUMED]: Assumed IS 1239 (Part 1) because 'Class B' is the Indian trade shorthand for its medium series.
  - **Please confirm:** State the governing standard in the RFQ.
- **WARNING · CLASS_MEANING** — "Class B" does not appear in IS 1239 (Part 1):2004, which classifies tubes as light, medium and heavy (marked L/M/H, colour bands yellow/blue/red). In Indian trade, Class A/B/C = light/medium/heavy; other standards use classes for pressure rating.
  - Interpretations considered: IS 1239 medium series; pressure / other class from a different standard
  - Assumption used [ASSUMED]: Read as IS 1239 medium series; wall thickness taken from the BIS table.
  - **Please confirm:** Confirm class B = medium (blue colour band) and the required wall thickness.
- **CRITICAL · QTY_UNIT_MISSING** — Quantity 500 has no unit. The unit changes the supplier type: a few tonnes is a dealer/stockist order, hundreds of tonnes is a mill-direct order.
  - Interpretations considered: 500 tonnes; 500 metres (~1.8 t); 500 x 6 m lengths (~10.7 t)
  - Assumption used [ASSUMED]: Assumed 500 tonnes (~140,449 m, ~23,408 x 6 m lengths).
  - **Please confirm:** Confirm the quantity unit.

### M-03 — `ERW pipe, DN 80, 89.5 × 4.8 mm, IS 1239` · qty 1200 (no unit) · Ahmedabad, Gujarat, India
- **Resolved for search** (original never overwritten): DN80, OD 89.5 mm [SOURCED], wall 4.8 mm [SOURCED], standard IS 1239 (Part 1), series heavy
- **Derived** [REFERENCE]: 9.9 kg/m (IS 1239 table: DN80 heavy = 9.9 kg/m (plain end); formula cross-check 10.03 kg/m); 1,200 t ≈ 121,212 m ≈ 20,202 × 6 m lengths
- **INFO · OD_AT_LIMIT** — 89.5 mm is valid but is the maximum permitted OD for DN80 in IS 1239 (range 88-89.5 mm); the usual nominal OD is 88.9 mm.
  - Interpretations considered: nominal OD 88.9 mm; maximum OD limit 89.5 mm
  - Assumption used [ASSUMED]: Kept 89.5 mm as written; searches also use the nominal 88.9 mm.
  - **Please confirm:** Confirm whether 89.5 mm is a deliberate OD requirement or a table limit copied from the standard.
- **CRITICAL · QTY_UNIT_MISSING** — Quantity 1200 has no unit. The unit changes the supplier type: a few tonnes is a dealer/stockist order, hundreds of tonnes is a mill-direct order.
  - Interpretations considered: 1200 tonnes; 1200 metres (~11.9 t); 1200 x 6 m lengths (~71.3 t)
  - Assumption used [ASSUMED]: Assumed 1200 tonnes (~121,212 m, ~20,202 x 6 m lengths).
  - **Please confirm:** Confirm the quantity unit.

## 3. Coverage

| Material | Geography | Found | Shortlisted | By match class | Status |
|---|---|---|---|---|---|
| M-01 | Ahmedabad vendors | 7 | 5 | CATEGORY 3, NEAR 3, UNVERIFIED 1 | OK |
| M-01 | India-based vendors outside Ahmedabad | 13 | 5 | NEAR 10, CATEGORY 3 | OK |
| M-01 | International / global vendors | 7 | 5 | NEAR 7 | OK |
| M-01 | Location not established | 27 | 0 | UNVERIFIED 23, NEAR 2, CATEGORY 2 | ONLY_UNVERIFIED_LEADS |
| M-02 | Ahmedabad vendors | 8 | 5 | CATEGORY 2, NEAR 5, UNVERIFIED 1 | OK |
| M-02 | India-based vendors outside Ahmedabad | 10 | 5 | NEAR 7, EXACT 1, CATEGORY 2 | OK |
| M-02 | International / global vendors | 6 | 5 | NEAR 5, CATEGORY 1 | OK |
| M-02 | Location not established | 34 | 0 | UNVERIFIED 29, CATEGORY 5 | ONLY_UNVERIFIED_LEADS |
| M-03 | Ahmedabad vendors | 6 | 5 | CATEGORY 2, NEAR 3, UNVERIFIED 1 | OK |
| M-03 | India-based vendors outside Ahmedabad | 12 | 5 | NEAR 10, CATEGORY 2 | OK |
| M-03 | International / global vendors | 5 | 5 | NEAR 5 | OK |
| M-03 | Location not established | 28 | 0 | UNVERIFIED 24, NEAR 1, CATEGORY 3 | ONLY_UNVERIFIED_LEADS |

## 4. M-01 — ERW pipe, DN 50, 60.3 × 5.5 mm, IS 1239

### Ahmedabad vendors

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Rajsagar | MANUFACTURER | Ahmedabad, India (VERIFIED) | NEAR | HIGH | 0.75 | yes |
| 2 | Bhushantube | STOCKIST | Ahmedabad, India (VERIFIED) | NEAR | MEDIUM | 0.65 | yes |
| 3 | MN METAL | STOCKIST | Ahmedabad, India (VERIFIED) | NEAR | HIGH | 0.58 | yes |
| 4 | Padmawati Traders | STOCKIST | Ahmedabad, India (VERIFIED) | CATEGORY | MEDIUM | 0.50 | yes |
| 5 | Jai Vikas Steel Corporation Private Limited | MS | STOCKIST | Ahmedabad, India (VERIFIED) | CATEGORY | MEDIUM | 0.49 | yes |
| 6 | Navkar Tubes & Tools | STOCKIST | Ahmedabad, India (VERIFIED) | CATEGORY | MEDIUM | 0.49 | no |
| 7 | Hariom Steel Traders | TRADER | Ahmedabad, India (VERIFIED) | UNVERIFIED | LOW | 0.42 | no |

#### 1. Rajsagar — NEAR · HIGH confidence · score 0.75
- **MANUFACTURER** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Ahmedabad' (evidence rajsagar.com#1))
- **Contact:** https://www.rajsagar.com/; 098989 72828 · **Address:** 103 Sukh Sagar Complex Ashram Road Usmanpura, Next to Fortune Land Mark Hotel, Ashram Road, Usmanpura, Ahmedabad, Gujar…
- **Match:** DN50 / OD size stated; IS 1239 stated; required wall 5.5 mm not confirmed
- **Confidence:** vendor's own site/maps evidences size, standard (12 quote(s), 3 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 1.00, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A106, ASTM A53, IS 1239, IS 3589 · Certs [SOURCED] ISO management-system certificate, test / inspection certificate (men… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `rajsagar.com#6` (product_match/profile, vendor_site) “MS Pipe Supplier in Ahmedabad, Gujarat | 1 1/2 inch (40 mm) pipe - 168 Rs/kg; 2 inch (50 mm) pipe - 175 Rs/kg; 1/2 inch (15 mm) black ms pipe - 61 Rs/kg; 1/2 inch (15 mm…” — [source](https://www.rajsagar.com/ms-pipes-supplier-stockist.html)
  - `rajsagar.com#10` (product_match, vendor_site) “Seamless Steel Pipes & Tubes in India meeting National & International Standards. The | plant is located in Chattral, Gujarat. The capabilities of producing size range f…” — [source](https://www.rajsagar.com/)
  - `rajsagar.com#18` (location, vendor_site) “plant is located in Chattral, Gujarat. The capabilities of producing size range from 2" OD” — [source](https://www.rajsagar.com/)
  - `rajsagar.com#25` (product_match, vendor_site) “2.375 | 60.30 | 2.90” — [source](https://www.rajsagar.com/is-1239-part-1-pipes-supplier-stockist.html)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 2. Bhushantube — NEAR · MEDIUM confidence · score 0.65
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: vendor site states 'Ahmedabad' (evidence bhushantube.com#10); also located in Delhi, Ghaziabad, Mumbai, New Delhi)
- **Contact:** https://www.bhushantube.com
- **Match:** DN50 / OD size stated; IS 1239 stated; required wall 5.5 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.38, geography delivery 1.00, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist with stock (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] API 5L, ASTM A106, IS 1239, IS 3589 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [NEEDS_RFQ] not found in sources - confirm delivery to Ahmedabad and freight terms · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer mentioning stock; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `bhushantube.com#6` (product_match, vendor_site) “4 | 2"" | 50 MM” — [source](https://www.bhushantube.com/ms-erw-black-pipes-range.html)
  - `bhushantube.com#7` (product_match, vendor_site) “50 MM | 60.3 | LIGHT” — [source](https://www.bhushantube.com/ms-erw-black-pipes-range.html)
  - `bhushantube.com#3` (standard, vendor_site) “Codes & Specification | IS 1239 | IS 3589” — [source](https://www.bhushantube.com/ms-erw-black-pipes-range.html)
  - `bhushantube.com#15` (standard, vendor_site) “Codes & Specification | IS 1239 | IS 3589” — [source](https://bhushantube.com/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 3. MN METAL — NEAR · HIGH confidence · score 0.58
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Bapunagar' (evidence mnmetal.in#1))
- **Contact:** https://www.mnmetal.in/; 084889 94771 · **Address:** Office No.311, 3rd Floor "BAPUNAGAR ONE" Business Hub, opp. White house, nr. Shyam Sikhar Complex, Bapunagar, Ahmedabad…
- **Match:** DN50 / OD size stated; IS 1239 stated; only the nearest IS 1239 wall (4.5 mm) is listed, not the required one
- **Confidence:** vendor's own site/maps evidences size, standard, wall (6 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239 · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [NEEDS_RFQ] not found in sources - confirm delivery to Ahmedabad and freight terms · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `mnmetal.in#5` (product_match, vendor_site) “Nominal Bore (NB): | 50 mm (2 inch) | Get Quote” — [source](https://www.mnmetal.in/)
  - `mnmetal.in#17` (product_match, vendor_site) “Nominal Bore (NB): | 50 mm (2 inch) | Get Quote” — [source](https://mnmetal.in/)
  - `mnmetal.in#3` (standard/product_match, vendor_site) “Hot Dip Galvanized Seamless Pipes | GI Round Tube, 50 mm OD, 3.6 mm Thickness, 6m Length, IS 1239, Galvanized | View All Products” — [source](https://www.mnmetal.in/)
  - `mnmetal.in#15` (standard/product_match, vendor_site) “Hot Dip Galvanized Seamless Pipes | GI Round Tube, 50 mm OD, 3.6 mm Thickness, 6m Length, IS 1239, Galvanized | View All Products” — [source](https://mnmetal.in/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 4. Padmawati Traders — CATEGORY · MEDIUM confidence · score 0.50
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Vatva' (evidence padmawatitraders.com#1))
- **Contact:** http://www.padmawatitraders.com/; 098983 34675; +91 98983 34675 · **Address:** PLOT NO -44 45/A/12/B Aarkoi Cement Compound Vatva Railway Crossing Over Bridge Road, opp. Yamuna Estate, near Neoplast…
- **Match:** ERW pipe supply mentioned; no size evidence for DN50
- **Confidence:** category-level only: supplies ERW/steel pipe but no size evidence
- **Score:** technical match 0.30, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 1.00, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [NEEDS_RFQ] not found in sources - ask for the standard and BIS licence · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Duplicates merged:** Padmawatitraders (padmawatitraders.in)
- **Evidence:**
  - `padmawatitraders.com#3` (product_match/profile, vendor_site) “MS Seamless, Erw, Gi, Crc, Square Pipe Dealers, Suppliers in ... | Padmawati Traders is the leading suppliers of Pipe Fittings, Boiler Tubes, SS Pipes, CRC, GI, ERW, Squ…” — [source](https://www.padmawatitraders.com/)
  - `padmawatitraders.com#4` (product_match/profile, vendor_site) “Mild Steel ERW Pipes | Trader - Wholesaler / Distributor of ERW Pipes - Mild Steel ERW Pipes, ERW Steel Pipes, ERW Line Pipes and MS Black Pipe offered by Padmavati Trad…” — [source](https://www.padmawatitraders.in/erw-pipes.html)
  - `padmawatitraders.com#8` (product_match/profile, vendor_site) “MS Seamless, Erw, Gi, Crc, Square Pipe Dealers, Suppliers in Ahmedabad | Call: +91 98983 34675 | Email:” — [source](http://www.padmawatitraders.com/)
  - `padmawatitraders.com#11` (export, vendor_site) “At Padmawati we believe in the quality of our product and services ERW pipes in Ahmedabad, ERW pipe Dealer in Ahmedabad, ERW pipe Supplier in Ahmedabad, seamless pipe in…” — [source](http://www.padmawatitraders.com/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Request their product list / catalogue for DN50 and the BIS licence before any RFQ.

#### 5. Jai Vikas Steel Corporation Private Limited | MS | ERW | GI | GP Pipe Manufacturers and Distributors in Ahmedabad — CATEGORY · MEDIUM confidence · score 0.49
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Ahmedabad' (evidence jaivikas.com#1))
- **Contact:** https://www.jaivikas.com/; 098251 27921 · **Address:** SURVEY NO - 382, SHYAM INDUSTRIAL ESTATE, PLOT NO - 2/3, CANAL ROAD, Changodar, Ahmedabad, Gujarat 382213
- **Match:** ERW pipe supply mentioned; no size evidence for DN50
- **Confidence:** category-level only: supplies ERW/steel pipe but no size evidence
- **Score:** technical match 0.30, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [NEEDS_RFQ] not found in sources - ask for the standard and BIS licence · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `jaivikas.com#1` (product_match/profile/location, maps) “Jai Vikas Steel Corporation Private Limited | MS | ERW | GI | GP Pipe Manufacturers and Distributors in Ahmedabad SURVEY NO - 382, SHYAM INDUSTRIAL ESTATE, PLOT NO - 2/3…” — [source](https://www.jaivikas.com/)
  - `jaivikas.com#2` (product_match/profile/location, maps) “Jai Vikas Steel Corporation Private Limited | MS | ERW | GI | GP Pipe Manufacturers and Distributors in Ahmedabad SURVEY NO - 382, SHYAM INDUSTRIAL ESTATE, PLOT NO - 2/3…” — [source](https://www.jaivikas.com/)
  - `jaivikas.com#3` (product_match/profile, maps) “MS and Mild Steel Pipe | ERW Pipe Dealer | Hot Dip GI Solar ... | Jai Vikas Steel Corporation Pvt. Ltd. Leading MS & Mild Steel Pipe | ERW Pipe Dealer | Hot Dip GI Solar…” — [source](https://www.jaivikas.com/)
  - `jaivikas.com#4` (product_match/profile, vendor_site) “MS and Mild Steel Pipe | ERW Pipe Dealer | Hot Dip GI Solar Pipe | GP & Galvanised Pipe | Mild steel Pipe Wholesalers Suppliers Distributors Manufacturers in Ahmedabad, …” — [source](https://www.jaivikas.com/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Request their product list / catalogue for DN50 and the BIS licence before any RFQ.

**Not shortlisted:** Navkar Tubes & Tools — ranked below the top 5 for this tier (score 0.49); Hariom Steel Traders — unverified lead: no quote shows a matching product - listed for follow-up, not shortlisted

### India-based vendors outside Ahmedabad

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Dealonsteel | STOCKIST | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.70 | yes |
| 2 | Emirerristeel | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.67 | yes |
| 3 | Amco Exports | MANUFACTURER | Bangalore, India (VERIFIED) | NEAR | MEDIUM | 0.65 | yes |
| 4 | Steel Pipes/Tubes Manufacturers in India, Top Pi | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | HIGH | 0.63 | yes |
| 5 | Sachiya Steel | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.59 | yes |
| 6 | Tubes & Valves MFG Co | MANUFACTURER | Chennai, India (VERIFIED) | NEAR | MEDIUM | 0.57 | no |
| 7 | APOLLON STEEL INC. | STOCKIST | Mumbai, India (VERIFIED) | NEAR | HIGH | 0.56 | no |
| 8 | Steelian | STOCKIST | Chennai, India (VERIFIED) | CATEGORY | MEDIUM | 0.56 | no |
| 9 | RP Sales | STOCKIST | Kanpur, India (VERIFIED) | NEAR | MEDIUM | 0.54 | no |
| 10 | Heavy (Class C) | STOCKIST | Vadodara, India (CLAIMED) | NEAR | MEDIUM | 0.41 | no |
| 11 | Katariyasteel | STOCKIST | Mumbai, India (VERIFIED) | CATEGORY | MEDIUM | 0.39 | no |
| 12 | Risingsteels | TRADER | Mumbai, India (VERIFIED) | CATEGORY | MEDIUM | 0.34 | no |
| 13 | Techno Tube Industries | TRADER | Mumbai, India (CLAIMED) | NEAR | MEDIUM | 0.34 | no |

#### 1. Dealonsteel — NEAR · MEDIUM confidence · score 0.70
- **STOCKIST** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence dealonsteel.com#38); also located in Navi Mumbai)
- **Contact:** https://dealonsteel.com
- **Match:** DN50 / OD size stated; IS 1239 stated; only the nearest IS 1239 wall (4.5 mm) is listed, not the required one
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.38, geography delivery 0.90, certification 1.00, source quality 0.90, contactability 0.50 — geography/delivery: delivery to Ahmedabad/Gujarat stated; bulk relevance: stockist with stock (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239 · Certs [SOURCED] BIS / ISI mark, test / inspection certificate (mentioned; certificate… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer mentioning stock; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `dealonsteel.com#7` (product_match, vendor_site) “Suppose: | OD = 60.3 mm | Thickness = 3.2 mm” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
  - `dealonsteel.com#8` (product_match, vendor_site) “Then: | Weight = 0.02466 × (60.3 − 3.2) × 3.2 | = Approx. 4.5 kg/m” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
  - `dealonsteel.com#24` (product_match, vendor_site) “Industrial utility systems | 50 NB | Medium to Large” — [source](https://dealonsteel.com/ms-pipes/top-ms-pipe-dealers-in-ahmedabad/)
  - `dealonsteel.com#1` (standard, vendor_site) “Jindal Pipe Weight Chart 2026 – MS & GI ... | The following Jindal MS and GI pipe weight chart is based on standard IS 1239 dimensions widely used across construction, p…” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 2. Emirerristeel — NEAR · MEDIUM confidence · score 0.67
- **MANUFACTURER** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence emirerristeel.com#14))
- **Contact:** https://emirerristeel.com
- **Match:** DN50 / OD size stated; IS 1239 stated; required wall 5.5 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.40, certification 1.00, source quality 0.90, contactability 0.50 — geography/delivery: India-based; delivery to Ahmedabad plausible but unconfirmed; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] EN 10217, EN 10219, EN 10255, IS 1239 · Certs [SOURCED] BIS / ISI mark (mentioned; certificate numbers not verified) · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `emirerristeel.com#1` (standard/product_match/class, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C | Mechanical Properties ; Elongation (on 5x Dia gauge length), Min. 20% ; Bend Test (Up to 50 mm NB), No crack on bending 180° ; …” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#7` (product_match, vendor_site) “Min. 20% | Bend Test (Up to 50 mm NB) | No crack on bending 180°” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#8` (product_match, vendor_site) “4.05 / 4.53 | 2″ / 50 mm | 2.375 / 60.30” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#2` (standard/class, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C | IS 1239 ; Specification, Mild Steel Tubes for Water, Gas, Air, and Steam ; Size Range, 1/8" NB to 20" NB (Nominal Bore) ; Outer…” — [source](https://emirerristeel.com/is-1239/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 3. Amco Exports — NEAR · MEDIUM confidence · score 0.65
- **MANUFACTURER** [SOURCED] · **Bangalore, Karnataka, India** (VERIFIED: vendor site states 'Bangalore' (evidence amcoexports.com#17); also located in Kolkata)
- **Contact:** https://www.amcoexports.com
- **Match:** DN50 / OD size stated; standard stated is EN 10219, IS 1161, not IS 1239; required wall 5.5 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.70, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: pan-India delivery stated; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] EN 10219, IS 1161 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] pan-India delivery stated · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `amcoexports.com#7` (class, vendor_site) “Key Benefits of ERW Scaffolding Pipes | High load-bearing capacity for heavy-duty applications | Accurate OD (38.1mm / 48.3mm / 60.3mm) for coupler compatibility” — [source](https://www.amcoexports.com/product/erw-scaffolding-pipe-manufacturer/?srsltid=AU7gw4VATjXbplt-H5tn8ytrNz5VAbGB3_RxzYU2-dqrDxGacysqGfWT)
  - `amcoexports.com#2` (standard, vendor_site) “Material Grade | IS 1161, YST 210, YST 240, EN Grade | Surface Finish” — [source](https://www.amcoexports.com/product/erw-scaffolding-pipe-manufacturer/?srsltid=AU7gw4VATjXbplt-H5tn8ytrNz5VAbGB3_RxzYU2-dqrDxGacysqGfWT)
  - `amcoexports.com#3` (standard, vendor_site) “Standards | BS 1139, EN 39, EN 10219, IS Specifications | Applications” — [source](https://www.amcoexports.com/product/erw-scaffolding-pipe-manufacturer/?srsltid=AU7gw4VATjXbplt-H5tn8ytrNz5VAbGB3_RxzYU2-dqrDxGacysqGfWT)
  - `amcoexports.com#17` (stock/export, vendor_site) “Scaffolding Manufacturer in India Since 1989 | Manufacturing Since 1989 | Warehouse in Bangalore & Kolkata | Exporting to 15+ Countries | Contact Now” — [source](https://amcoexports.com/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 4. Steel Pipes/Tubes Manufacturers in India, Top Pipe Suppliers — NEAR · HIGH confidence · score 0.63
- **MANUFACTURER** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence steeltubes.co.in#17))
- **Contact:** https://steeltubes.co.in; +919833604219; sales@metline.in
- **Match:** DN50 / OD size stated; IS 1239 stated; 5.5 mm wall mentioned but not tied to this size in one quote
- **Confidence:** vendor's own site/maps evidences series, size, standard, wall (11 quote(s), 1 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.40, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: India-based; delivery to Ahmedabad plausible but unconfirmed; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A106, ASTM A53, IS 1239, IS 3589 · Certs [SOURCED] ISO management-system certificate, test / inspection certificate (men… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `steeltubes.co.in#8` (product_match, vendor_site) “2.375 | 60.30 | 2.90” — [source](https://steeltubes.co.in/is-1239-steel-pipes-tubes-supplier-manufacturer-mumbai-india/)
  - `steeltubes.co.in#1` (standard/product_match/profile, vendor_site) “IS:1239 Steel Pipes, ERW Steel Tubes Supplier Mumbai, India | We stock an extensive range of electric resistance welded (ERW) IS:1239 steel pipes / tubes in a size range…” — [source](https://steeltubes.co.in/is-1239-steel-pipes-tubes-supplier-manufacturer-mumbai-india/)
  - `steeltubes.co.in#2` (standard/product_match/profile, vendor_site) “IS:1239 Steel Pipes, ERW Steel Tubes Supplier Mumbai, India | ERW Black Steel Pipes, Certified manufacturer and supplier of IS:1239 Steel Pipes/Tubes. ERW Steel Pipes! s…” — [source](https://steeltubes.co.in/is-1239-steel-pipes-tubes-supplier-manufacturer-mumbai-india/)
  - `steeltubes.co.in#3` (standard/product_match/class, vendor_site) “IS:1239 Steel Pipes, ERW Steel Tubes Supplier Mumbai, India | ERW STEEL PIPES. ERW PIPES, +919833604219, We stock an extensive range of electric resistance welded (ERW) …” — [source](https://steeltubes.co.in/is-1239-steel-pipes-tubes-supplier-manufacturer-mumbai-india/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 5. Sachiya Steel — NEAR · MEDIUM confidence · score 0.59
- **MANUFACTURER** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence sachiyasteel.com#20); also located in Thane, Vasai)
- **Contact:** https://sachiyasteel.com
- **Match:** DN50 / OD size stated; IS 1239 stated; required wall 5.5 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.40, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: India-based; delivery to Ahmedabad plausible but unconfirmed; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] IS 1239 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `sachiyasteel.com#2` (standard/product_match, vendor_site) “ERW Pipe Size Chart in mm & Inches – Dimensions Guide | ERW Pipe Dimensions Chart — IS 1239 (Indian Standard) ; 40mm (1-1/2"), 48.3, 2.9 ; 50mm (2"), 60.3, 2.9 ; 65mm (2…” — [source](https://sachiyasteel.com/blog/erw-pipe-size-chart/?srsltid=AU7gw4VtxOIoohSP72FUFWzyaj5oAD0L8RBp1iEolU_ZECX4Kvn_O-II)
  - `sachiyasteel.com#3` (standard/product_match, vendor_site) “ERW Pipe Size Chart in mm & Inches – Dimensions Guide | ERW Pipe Dimensions Chart — IS 1239 (Indian Standard) ; 40mm (1-1/2"), 48.3, 2.9 ; 50mm (2"), 60.3, 2.9 ; 65mm (2…” — [source](https://sachiyasteel.com/blog/erw-pipe-size-chart/?srsltid=AU7gw4UayNvvY5cVNV-xWLef41qN_ca6LPyqiFBxUVBvDCCVggEC7URY)
  - `sachiyasteel.com#10` (product_match, vendor_site) “5.41 | 2" | 60.33” — [source](https://sachiyasteel.com/blog/erw-pipe-size-chart/?srsltid=AU7gw4UU66pp3uc_v1nQefnNGQ4Y8MFNsbXBfmZuVBm5sh4vR7PMqiv8)
  - `sachiyasteel.com#11` (product_match, vendor_site) “1.500 | 2" | 2.375” — [source](https://sachiyasteel.com/blog/erw-pipe-size-chart/?srsltid=AU7gw4UU66pp3uc_v1nQefnNGQ4Y8MFNsbXBfmZuVBm5sh4vR7PMqiv8)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

**Not shortlisted:** Tubes & Valves MFG Co — ranked below the top 5 for this tier (score 0.57); APOLLON STEEL INC. — ranked below the top 5 for this tier (score 0.56); Steelian — ranked below the top 5 for this tier (score 0.56); RP Sales — ranked below the top 5 for this tier (score 0.54); Heavy (Class C) — ranked below the top 5 for this tier (score 0.41); Katariyasteel — ranked below the top 5 for this tier (score 0.39); Risingsteels — ranked below the top 5 for this tier (score 0.34); Techno Tube Industries — ranked below the top 5 for this tier (score 0.34)

### International / global vendors

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Tianyingtai Steel Pipe | MANUFACTURER | China (VERIFIED) | NEAR | HIGH | 0.67 | yes |
| 2 | Forever Steel | MANUFACTURER | China (VERIFIED) | NEAR | HIGH | 0.64 | yes |
| 3 | Glory Steel | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.61 | yes |
| 4 | Octalsteel | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.61 | yes |
| 5 | Youfa Steel Pipe | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.60 | yes |
| 6 | Eastern Steels | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.54 | no |
| 7 | Derbo | STOCKIST | China (VERIFIED) | NEAR | HIGH | 0.50 | no |

#### 1. Tianyingtai Steel Pipe — NEAR · HIGH confidence · score 0.67
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence tytsteelpipes.com#8))
- **Contact:** https://www.tytsteelpipes.com; +8618522522113; info@tytgg.com.cn
- **Match:** DN50 / OD size stated; standard stated is API 5L, ASTM A53, not IS 1239; required wall 5.5 mm not confirmed
- **Confidence:** vendor's own site/maps evidences size, standard (3 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 1.00, geography delivery 0.45, certification 0.40, source quality 0.90, contactability 1.00 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer with capacity
- **Facts:** Standards [SOURCED] API 5L, ASTM A53 · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [SOURCED] Capacity: 5000 TON · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · MOQ [SOURCED] Minimum order quantity: 20 tons 2) Price: FOB or CIF or CFR at aXin’g… · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [SOURCED]: manufacturer with a stated capacity; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `tytsteelpipes.com#13` (standard, vendor_site) “Read More | 2 Inch Black & Galvanized Steel Pipe - ASTM A53 SCH40 48m... | 2 Inch ERW Steel Pipe Price - Low MOQ & Fast Global Shipping.Hot Dipped Galvanized Tube” — [source](https://tytsteelpipes.com/)
  - `tytsteelpipes.com#14` (product_match/moq, vendor_site) “2 Inch Black & Galvanized Steel Pipe - ASTM A53 SCH40 48m... | 2 Inch ERW Steel Pipe Price - Low MOQ & Fast Global Shipping.Hot Dipped Galvanized Tube | Read More” — [source](https://tytsteelpipes.com/)
  - `tytsteelpipes.com#2` (standard, vendor_site) “Add to Inquiry | API 5L Seamless Steel Line Pipe | Supply Range of Diameters: 1/2” to 26”Range of Thickness: SCH 10 to SCH 160Ends Type: Beveled ends, Plain endsRange of…” — [source](https://www.tytsteelpipes.com/showroom/galvanized-48-3mm-scaffolding-tube/)
  - `tytsteelpipes.com#8` (profile, vendor_site) “China Galvanized 48 3mm Scaffolding Tube Manufacturers Factory Suppliers | info@tytgg.com.cn | +8618522522113” — [source](https://www.tytsteelpipes.com/showroom/galvanized-48-3mm-scaffolding-tube/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; price, lead time and MOQ require an RFQ (+4 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 2. Forever Steel — NEAR · HIGH confidence · score 0.64
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence forever-steels.com#18))
- **Contact:** https://www.forever-steels.com; +8615674993216; sales@forever-steels.com
- **Match:** DN50 / OD size stated; standard stated is API 5L, ASTM A53, EN 10217, not IS 1239; 5.5 mm wall mentioned but not tied to this size in one quote
- **Confidence:** vendor's own site/maps evidences size, standard, wall (10 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A53, EN 10217 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `forever-steels.com#5` (product_match, vendor_site) “SCH 40, SCH 80 | 2" (60.3 | mm)” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#6` (product_match, vendor_site) “Random: ±1.64 ft (0.5 m) | Fixed: −0/+2 in (50 mm) | ASTM A53(General Use)” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#2` (standard/product_match/profile, vendor_site) “ERW Steel Pipe Supplier,ASTM A53 Electric Resistance ... | Forever Steel supplies ERW steel pipe and electric resistance welded pipe for water,gas,structural and industr…” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#3` (standard/product_match/profile, vendor_site) “ERW Steel Pipe Supplier,ASTM A53 Electric Resistance Welded Pipe | +8615674993216 | sales@forever-steels.com” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+5 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 3. Glory Steel — NEAR · MEDIUM confidence · score 0.61
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence glrsteel.com#19))
- **Contact:** https://glrsteel.com
- **Match:** DN50 / OD size stated; standard stated is API 5L, ASTM A53, not IS 1239; required wall 5.5 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A53 · Certs [SOURCED] ISO management-system certificate, test / inspection certificate (men… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `glrsteel.com#7` (product_match, vendor_site) “1-1/2” Galvanized Pipe | 2” Galvanized Pipe | 2-1/2” Galvanized Pipe” — [source](https://glrsteel.com/product/erw-steel-pipe/)
  - `glrsteel.com#8` (product_match, vendor_site) “European Standard (EN / BS) | Nominal Diameter (DN): in millimeters, e.g. DN15, DN50 | Wall Thickness: S series (S1/S2/S3) or direct mm value” — [source](https://glrsteel.com/product/erw-steel-pipe/)
  - `glrsteel.com#25` (product_match, vendor_site) “1-1/2” Galvanized Pipe | 2” Galvanized Pipe | 2-1/2” Galvanized Pipe” — [source](https://glrsteel.com/)
  - `glrsteel.com#4` (standard, vendor_site) “Galvanized Culvert Pipe | ASTM A53 Gr.B Galvanized Pipe | Galvanized Electrical Conduit” — [source](https://glrsteel.com/product/erw-steel-pipe/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+5 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 4. Octalsteel — NEAR · MEDIUM confidence · score 0.61
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence octalsteel.com#17))
- **Contact:** https://www.octalsteel.com
- **Match:** DN50 / OD size stated; standard stated is API 5L, ASTM A135, ASTM A53, EN 10219, not IS 1239; required wall 5.5 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A135, ASTM A53, EN 10219 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `octalsteel.com#8` (product_match, vendor_site) “2 | 60.3 | 3.91” — [source](https://www.octalsteel.com/resources/erw-pipe/)
  - `octalsteel.com#1` (standard/product_match/certification, vendor_site) “ERW Steel Pipe | High-frequency ERW steel pipe and API 5L ERW line pipe for onshore oil, gas, water and structural service, with tight tolerances, NDT and 3.1/3.2 MTC.” — [source](https://www.octalsteel.com/resources/erw-pipe/)
  - `octalsteel.com#2` (standard/product_match, vendor_site) “ERW Steel Pipe | Octal Steel supplies ERW steel pipe and API 5L ERW line pipe from qualified and audited mills, covering international standards for fluid service, line …” — [source](https://www.octalsteel.com/resources/erw-pipe/)
  - `octalsteel.com#3` (standard/product_match, vendor_site) “ERW Steel Pipe | Contact Now ! · Type: High-frequency ERW pipe & API 5L ERW pipe · Size Range: 1/2″–24″ OD, 1.8–16 mm WT · Standards: API 5L, ASTM A53, ASTM A135, EN 102…” — [source](https://www.octalsteel.com/resources/erw-pipe/)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+5 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 5. Youfa Steel Pipe — NEAR · MEDIUM confidence · score 0.60
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence youfasteelpipe.com#1))
- **Contact:** https://www.youfasteelpipe.com
- **Match:** DN50 / OD size stated; standard stated is API 5L, ASTM A500, ASTM A53, BS 1387, EN 10219, EN 10255, not IS 1239; only the nearest IS 1239 wall (4.5 mm) is listed, not the required one
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A500, ASTM A53, BS 1387, EN 10219, EN 10255 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · MOQ [SOURCED] MOQ | 5 tons · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,000 t (~134,535 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `youfasteelpipe.com#1` (product_match/profile, vendor_site) “China Erw Steel Pipe Manufacturer, Supplier, Factory | Length: 6m with stock, customized 5.5 to 12m (not suitable for small OD), and cut into 1m to 5.5m according to cus…” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
  - `youfasteelpipe.com#4` (standard/product_match, vendor_site) “welded erw bs 1387 galvanized steel pipe 60.3mm | Pipes can be Customized according to customer's requirement on zinc coating thickness, length , wall thickness and stee…” — [source](https://www.youfasteelpipe.com/pid18177355/welded-erw-bs-1387-galvanized-steel-pipe-60-3mm.htm)
  - `youfasteelpipe.com#10` (product_match, vendor_site) “4mm | DN50 | 2"” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
  - `youfasteelpipe.com#11` (product_match, vendor_site) “2" | 60.3mm | 2.77mm” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
- **Unresolved:** requirement ambiguity WALL_NOT_IN_STANDARD: Confirm the required wall thickness (and whether IS 1239 or another standard governs).; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+5 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

**Not shortlisted:** Eastern Steels — ranked below the top 5 for this tier (score 0.54); Derbo — ranked below the top 5 for this tier (score 0.50)

## 5. M-02 — 40 mm MS ERW, Class B pipe

### Ahmedabad vendors

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Rajsagar | MANUFACTURER | Ahmedabad, India (VERIFIED) | NEAR | HIGH | 0.75 | yes |
| 2 | Bhushantube | STOCKIST | Ahmedabad, India (VERIFIED) | NEAR | MEDIUM | 0.65 | yes |
| 3 | Ofbusiness | MARKETPLACE_LISTING | Ahmedabad, India (VERIFIED) | NEAR | MEDIUM | 0.62 | yes |
| 4 | Padmawati Traders | STOCKIST | Ahmedabad, India (VERIFIED) | NEAR | MEDIUM | 0.59 | yes |
| 5 | MN METAL | STOCKIST | Ahmedabad, India (VERIFIED) | NEAR | HIGH | 0.58 | yes |
| 6 | Jai Vikas Steel Corporation Private Limited | MS | STOCKIST | Ahmedabad, India (VERIFIED) | CATEGORY | MEDIUM | 0.49 | no |
| 7 | Navkar Tubes & Tools | STOCKIST | Ahmedabad, India (VERIFIED) | CATEGORY | MEDIUM | 0.49 | no |
| 8 | Hariom Steel Traders | TRADER | Ahmedabad, India (VERIFIED) | UNVERIFIED | LOW | 0.42 | no |

#### 1. Rajsagar — NEAR · HIGH confidence · score 0.75
- **MANUFACTURER** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Ahmedabad' (evidence rajsagar.com#1))
- **Contact:** https://www.rajsagar.com/; 098989 72828 · **Address:** 103 Sukh Sagar Complex Ashram Road Usmanpura, Next to Fortune Land Mark Hotel, Ashram Road, Usmanpura, Ahmedabad, Gujar…
- **Match:** DN40 / OD size stated; IS 1239 stated; required wall 3.2 mm not confirmed
- **Confidence:** vendor's own site/maps evidences size, standard (9 quote(s), 3 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 1.00, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A106, ASTM A53, IS 1239, IS 3589 · Certs [SOURCED] ISO management-system certificate, test / inspection certificate (men… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `rajsagar.com#6` (product_match/profile, vendor_site) “MS Pipe Supplier in Ahmedabad, Gujarat | 1 1/2 inch (40 mm) pipe - 168 Rs/kg; 2 inch (50 mm) pipe - 175 Rs/kg; 1/2 inch (15 mm) black ms pipe - 61 Rs/kg; 1/2 inch (15 mm…” — [source](https://www.rajsagar.com/ms-pipes-supplier-stockist.html)
  - `rajsagar.com#2` (standard/product_match/profile, vendor_site) “IS 1239 PART 1 Pipes Supplier, stockist | Rajsagar Steel one of the largest Stockist and Suppliers of IS 1239. ERW Pipes are widely used and available ・ a manufacturer, …” — [source](https://www.rajsagar.com/is-1239-part-1-pipes-supplier-stockist.html)
  - `rajsagar.com#8` (standard, vendor_site) “Carbon Steel ERW Pipes | IS 1239 PART 1 Pipes | IS 3589 FE 330 Pipes” — [source](https://www.rajsagar.com/)
  - `rajsagar.com#9` (product_match, vendor_site) “ASTM A210 Grade A1 Pipe Tubes | Carbon Steel ERW Pipes | IS 1239 PART 1 Pipes” — [source](https://www.rajsagar.com/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details (+2 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 2. Bhushantube — NEAR · MEDIUM confidence · score 0.65
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: vendor site states 'Ahmedabad' (evidence bhushantube.com#10); also located in Delhi, Ghaziabad, Mumbai, New Delhi)
- **Contact:** https://www.bhushantube.com
- **Match:** DN40 / OD size stated; IS 1239 stated; required wall 3.2 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.38, geography delivery 1.00, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist with stock (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] API 5L, ASTM A106, IS 1239, IS 3589 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [NEEDS_RFQ] not found in sources - confirm delivery to Ahmedabad and freight terms · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer mentioning stock; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `bhushantube.com#2` (product_match, vendor_site) “MS ERW Black Pipes & Application | Electric resistance welded (ERW) pipes are available is mild steel black form in various thickness (Light, Medium, Heavy) and various …” — [source](https://www.bhushantube.com/ms-erw-black-pipes-range.html)
  - `bhushantube.com#8` (product_match, vendor_site) “4 | 1½" | 40 MM” — [source](https://www.bhushantube.com/ms-erw-black-pipes-range.html)
  - `bhushantube.com#9` (product_match, vendor_site) “40 MM | 48.3 | LIGHT” — [source](https://www.bhushantube.com/ms-erw-black-pipes-range.html)
  - `bhushantube.com#3` (standard, vendor_site) “Codes & Specification | IS 1239 | IS 3589” — [source](https://www.bhushantube.com/ms-erw-black-pipes-range.html)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 3. Ofbusiness — NEAR · MEDIUM confidence · score 0.62
- **MARKETPLACE_LISTING** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: vendor site states 'Ahmedabad' (evidence ofbusiness.com#14); also located in Gurugram)
- **Contact:** https://www.ofbusiness.com
- **Match:** DN40 / OD size stated; IS 1239 stated; 3.2 mm wall mentioned but not tied to this size in one quote; series 'medium' mentioned; the matching size/wall row is attributed to a different standard (not IS 1239), so it cannot be treated as an exact match
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.19, geography delivery 1.00, certification 0.60, source quality 0.90, contactability 0.50 — geography/delivery: Ahmedabad presence verified; bulk relevance: marketplace listing (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1161, IS 1239, IS 3589 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] pan-India delivery stated · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: marketplace listing only; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `ofbusiness.com#1` (standard/product_match/wall, vendor_site) “MS ERW Round Pipe Price in India Today | Scaffolding pipes: 48.3 mm OD x 3.2 mm (medium class, IS 1161) - standard ... MS ERW round pipes are available from 15 NB (21.3 …” — [source](https://www.ofbusiness.com/prices/pipes/ms-erw-round-pipe)
  - `ofbusiness.com#3` (standard/product_match/wall, vendor_site) “MS ERW Round Pipe Price in India Today | Scaffolding pipes: 48.3 mm OD x 3.2 mm (medium class, IS 1161) - standard for construction scaffolding throughout India. Grades:…” — [source](https://www.ofbusiness.com/prices/pipes/ms-erw-round-pipe)
  - `ofbusiness.com#7` (product_match/wall, vendor_site) “Scaffolding pipes: | 48.3 mm OD x 3.2 mm (medium class, IS 1161) - standard for construction scaffolding throughout India. | Grades:” — [source](https://www.ofbusiness.com/prices/pipes/ms-erw-round-pipe)
  - `ofbusiness.com#8` (product_match, vendor_site) “What sizes are available in MS ERW round pipes? | MS ERW round pipes are available from 15 NB (21.3 mm OD) to 150 NB (168.3 mm OD) as per IS 1239. Larger sizes up to 610…” — [source](https://www.ofbusiness.com/prices/pipes/ms-erw-round-pipe)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 4. Padmawati Traders — NEAR · MEDIUM confidence · score 0.59
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Vatva' (evidence padmawatitraders.com#1))
- **Contact:** http://www.padmawatitraders.com/; 098983 34675; +91 98983 34675 · **Address:** PLOT NO -44 45/A/12/B Aarkoi Cement Compound Vatva Railway Crossing Over Bridge Road, opp. Yamuna Estate, near Neoplast…
- **Match:** '40 mm' mentioned (nominal bore vs OD not stated); no standard stated; required wall 3.2 mm not confirmed
- **Confidence:** own-source support is thin: no fact kinds on 1 page(s) (NEAR needs 3 kinds, or 2 kinds on 2 pages, for HIGH)
- **Score:** technical match 0.60, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 1.00, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [NEEDS_RFQ] not found in sources - ask for the standard and BIS licence · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Duplicates merged:** Padmawatitraders (padmawatitraders.in)
- **Evidence:**
  - `padmawatitraders.com#7` (product_match/profile, vendor_site) “M S Pipes Trader - Wholesaler / Distributor from Ahmedabad | Wholesaler / Distributor of MS Pipes - ERW Mild Steel Pipes offered by Padmavati Traders, Ahmedabad, ... Dia…” — [source](https://www.padmawatitraders.in/ms-pipes.html)
  - `padmawatitraders.com#1` (profile/location, maps) “Padmawati Traders PLOT NO -44 45/A/12/B Aarkoi Cement Compound Vatva Railway Crossing Over Bridge Road, opp. Yamuna Estate, near Neoplast Factory, Phase I, Vatva GIDC, A…” — [source](http://www.padmawatitraders.com/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 5. MN METAL — NEAR · HIGH confidence · score 0.58
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Bapunagar' (evidence mnmetal.in#1))
- **Contact:** https://www.mnmetal.in/; 084889 94771 · **Address:** Office No.311, 3rd Floor "BAPUNAGAR ONE" Business Hub, opp. White house, nr. Shyam Sikhar Complex, Bapunagar, Ahmedabad…
- **Match:** DN40 / OD size stated; IS 1239 stated; 3.2 mm wall mentioned but not tied to this size in one quote; series 'medium' mentioned; the matching row is a seamless listing or the page never states ERW, so the ERW process is not confirmed
- **Confidence:** vendor's own site/maps evidences series, size, standard, wall (4 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239 · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [NEEDS_RFQ] not found in sources - confirm delivery to Ahmedabad and freight terms · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `mnmetal.in#2` (standard/product_match/class, vendor_site) “Mild Steel Seamless Pipe | IS 1239 Galvanized Seamless Pipe, 1.5 inch, Medium Class (SCH 40 Equiv.) | Mild Steel Seamless Round Pipe” — [source](https://www.mnmetal.in/)
  - `mnmetal.in#14` (standard/product_match/class, vendor_site) “Mild Steel Seamless Pipe | IS 1239 Galvanized Seamless Pipe, 1.5 inch, Medium Class (SCH 40 Equiv.) | Mild Steel Seamless Round Pipe” — [source](https://mnmetal.in/)
  - `mnmetal.in#8` (wall, vendor_site) “Class: | 3.2 mm | Coating Thickness:” — [source](https://www.mnmetal.in/)
  - `mnmetal.in#20` (wall, vendor_site) “Class: | 3.2 mm | Coating Thickness:” — [source](https://mnmetal.in/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

**Not shortlisted:** Jai Vikas Steel Corporation Private Limi — ranked below the top 5 for this tier (score 0.49); Navkar Tubes & Tools — ranked below the top 5 for this tier (score 0.49); Hariom Steel Traders — unverified lead: no quote shows a matching product - listed for follow-up, not shortlisted

### India-based vendors outside Ahmedabad

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Dealonsteel | STOCKIST | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.70 | yes |
| 2 | Emirerristeel | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.67 | yes |
| 3 | RP Sales | STOCKIST | Kanpur, India (VERIFIED) | EXACT | MEDIUM | 0.66 | yes |
| 4 | Amco Exports | MANUFACTURER | Bangalore, India (VERIFIED) | NEAR | MEDIUM | 0.65 | yes |
| 5 | Steelian | STOCKIST | Chennai, India (VERIFIED) | NEAR | HIGH | 0.65 | yes |
| 6 | Steel Pipes/Tubes Manufacturers in India, Top Pi | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | HIGH | 0.63 | no |
| 7 | Sachiya Steel | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.59 | no |
| 8 | Tubes & Valves MFG Co | MANUFACTURER | Chennai, India (VERIFIED) | NEAR | MEDIUM | 0.57 | no |
| 9 | Katariyasteel | STOCKIST | Mumbai, India (VERIFIED) | CATEGORY | MEDIUM | 0.39 | no |
| 10 | Risingsteels | TRADER | Mumbai, India (VERIFIED) | CATEGORY | MEDIUM | 0.34 | no |

#### 1. Dealonsteel — NEAR · MEDIUM confidence · score 0.70
- **STOCKIST** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence dealonsteel.com#38); also located in Navi Mumbai)
- **Contact:** https://dealonsteel.com
- **Match:** DN40 / OD size stated; IS 1239 stated; 3.2 mm wall mentioned but not tied to this size in one quote; series 'medium' mentioned
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.38, geography delivery 0.90, certification 1.00, source quality 0.90, contactability 0.50 — geography/delivery: delivery to Ahmedabad/Gujarat stated; bulk relevance: stockist with stock (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239 · Certs [SOURCED] BIS / ISI mark, test / inspection certificate (mentioned; certificate… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer mentioning stock; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `dealonsteel.com#10` (product_match, vendor_site) “3.13 – 4.74 | 40 NB | 1 1/2″” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
  - `dealonsteel.com#11` (product_match, vendor_site) “1 1/2″ | 48.3 | 2.9” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
  - `dealonsteel.com#25` (product_match, vendor_site) “Water supply networks | 40 NB | Medium Range” — [source](https://dealonsteel.com/ms-pipes/top-ms-pipe-dealers-in-ahmedabad/)
  - `dealonsteel.com#1` (standard, vendor_site) “Jindal Pipe Weight Chart 2026 – MS & GI ... | The following Jindal MS and GI pipe weight chart is based on standard IS 1239 dimensions widely used across construction, p…” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 2. Emirerristeel — NEAR · MEDIUM confidence · score 0.67
- **MANUFACTURER** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence emirerristeel.com#14))
- **Contact:** https://emirerristeel.com
- **Match:** '40 mm' mentioned (nominal bore vs OD not stated); IS 1239 stated; required wall 3.2 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.40, certification 1.00, source quality 0.90, contactability 0.50 — geography/delivery: India-based; delivery to Ahmedabad plausible but unconfirmed; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] EN 10217, EN 10219, EN 10255, IS 1239 · Certs [SOURCED] BIS / ISI mark (mentioned; certificate numbers not verified) · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `emirerristeel.com#9` (product_match, vendor_site) “4.05 / 3.84 | 1.1/2″ / 40 mm | 1.906 / 48.40” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#2` (standard/class, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C | IS 1239 ; Specification, Mild Steel Tubes for Water, Gas, Air, and Steam ; Size Range, 1/8" NB to 20" NB (Nominal Bore) ; Outer…” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#3` (standard/class/certification, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C | IS 1239 GI Pipes Part 1 & 2 available in Class A, B, C – ideal for water, gas & structural use. Durable, corrosion-resistant, a…” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#4` (standard/class, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C - Emirerristeel | Welcome to Emirerri Steel Manufacturer Pvt Ltd | About us” — [source](https://emirerristeel.com/is-1239/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 3. RP Sales — EXACT · MEDIUM confidence · score 0.66
- **STOCKIST** [SOURCED] · **Kanpur, Uttar Pradesh, India** (VERIFIED: vendor site states 'Kanpur' (evidence rpsalespipes.com#14); also located in Delhi)
- **Contact:** https://rpsalespipes.com
- **Match:** Size and required wall/series appear together in one source quote (rpsalespipes.com#2); IS 1239 stated
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 1.00, bulk relevance 0.38, geography delivery 0.40, certification 0.60, source quality 0.90, contactability 0.50 — geography/delivery: India-based; delivery to Ahmedabad plausible but unconfirmed; bulk relevance: stockist with stock (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239, IS 3589, IS 3601, IS 4270 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · MOQ [SOURCED] minimum order quantity for MS ERW pipes? | Minimum order, price break… · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer mentioning stock; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `rpsalespipes.com#2` (standard/product_match/class, vendor_site) “ERW Pipe Price List ₹/kg IS 1239 (May 2026) - RP Sales | IS 1239 ERW Pipe Price Table: Light, Medium & Heavy Class ; 40 NB (1½"), 48.3, ₹51-58, ₹54-61, ₹58-66 ; 50 NB (2…” — [source](https://rpsalespipes.com/ms-pipe-price-list)
  - `rpsalespipes.com#5` (standard/product_match, vendor_site) “ERW Pipe Price List ₹/kg IS 1239 (May 2026) | RP Sales | Skip to main content | Home” — [source](https://rpsalespipes.com/ms-pipe-price-list)
  - `rpsalespipes.com#6` (standard, vendor_site) “Standards | IS 1239 | water & gas” — [source](https://rpsalespipes.com/ms-pipe-price-list)
  - `rpsalespipes.com#11` (class, vendor_site) “. | IS 1239 ERW Pipe Price Table: Light, Medium & Heavy Class | Size (NB)” — [source](https://rpsalespipes.com/ms-pipe-price-list)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Issue an RFQ for 500 t of 40 mm MS ERW, Class B pipe: request price, MOQ, lead time, delivery to Ahmedabad, BIS licence no. and mill test certificate. Ask for freight cost and transit time to Ahmedabad.

#### 4. Amco Exports — NEAR · MEDIUM confidence · score 0.65
- **MANUFACTURER** [SOURCED] · **Bangalore, Karnataka, India** (VERIFIED: vendor site states 'Bangalore' (evidence amcoexports.com#17); also located in Kolkata)
- **Contact:** https://www.amcoexports.com
- **Match:** DN40 / OD size stated; standard stated is EN 10219, IS 1161, not IS 1239; required wall 3.2 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.70, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: pan-India delivery stated; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] EN 10219, IS 1161 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] pan-India delivery stated · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `amcoexports.com#1` (product_match, vendor_site) “ERW Scaffolding Pipe Manufacturer | 6m MS GI Pipes Price | ERW scaffolding pipe manufacturer in India. 6m MS & GI pipes (48.3mm). Bulk supply at factory price. Call AMCO…” — [source](https://www.amcoexports.com/product/erw-scaffolding-pipe-manufacturer/?srsltid=AU7gw4VATjXbplt-H5tn8ytrNz5VAbGB3_RxzYU2-dqrDxGacysqGfWT)
  - `amcoexports.com#5` (product_match, vendor_site) “, and | 48.3 mm OD Scaffold Tube | , our ERW scaffolding pipes are widely used in” — [source](https://www.amcoexports.com/product/erw-scaffolding-pipe-manufacturer/?srsltid=AU7gw4VATjXbplt-H5tn8ytrNz5VAbGB3_RxzYU2-dqrDxGacysqGfWT)
  - `amcoexports.com#6` (product_match, vendor_site) “Outside Diameter | 38.1 mm, 48.3 mm, 60.3 mm | Standard Length” — [source](https://www.amcoexports.com/product/erw-scaffolding-pipe-manufacturer/?srsltid=AU7gw4VATjXbplt-H5tn8ytrNz5VAbGB3_RxzYU2-dqrDxGacysqGfWT)
  - `amcoexports.com#7` (class, vendor_site) “Key Benefits of ERW Scaffolding Pipes | High load-bearing capacity for heavy-duty applications | Accurate OD (38.1mm / 48.3mm / 60.3mm) for coupler compatibility” — [source](https://www.amcoexports.com/product/erw-scaffolding-pipe-manufacturer/?srsltid=AU7gw4VATjXbplt-H5tn8ytrNz5VAbGB3_RxzYU2-dqrDxGacysqGfWT)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details (+2 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 5. Steelian — NEAR · HIGH confidence · score 0.65
- **STOCKIST** [SOURCED] · **Chennai, Tamil Nadu, India** (VERIFIED: vendor site states 'Chennai' (evidence steelian.com#15))
- **Contact:** https://steelian.com; +91-9888-2444
- **Match:** DN40 / OD size stated; IS 1239 stated; required wall 3.2 mm not confirmed
- **Confidence:** vendor's own site/maps evidences series, size, standard (7 quote(s), 1 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.30, geography delivery 0.90, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: delivery to Ahmedabad/Gujarat stated; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239, IS 3589 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `steelian.com#10` (product_match, vendor_site) “: | IS 1239 : 1/2″ NB, 1″ NB, 1 1/2″ NB, 2″ NB, 3″ NB, 4″ NB, 5″ NB, 6″ NB, 25 MM NB , 32 MM NB , 40 MM NB, 65 MM NB, 80 MM NB, 100 MM NB, 125 MM NB , 150 MM NB | IS 358…” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
  - `steelian.com#1` (standard/product_match/profile, vendor_site) “Mild Steel Erw Pipe Dealers in Ahmedabad Suppliers ... | ERW Pipe IS 1239 dealers in Ahmedabad, 5′′ NB, 6′′ call us at +91-9888-2444-54” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
  - `steelian.com#3` (standard/product_match/profile, vendor_site) “Mild Steel Erw Pipe Dealers in Ahmedabad Suppliers ... | MS ERW Pipe IS 1239 dealers in Ahmedabad, 5′′ NB, 6′′ call us at +91-9888-2444-54” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
  - `steelian.com#4` (standard/product_match/profile, vendor_site) “Mild Steel Erw Pipe Dealers in Ahmedabad Suppliers ... | Ms erw pipe suppliers of IS 1239 IS 3589, Surya, Apollo we provide material in Ahmedabad, Sarkhej, Vapi, Gujarat…” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated (+1 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

**Not shortlisted:** Steel Pipes/Tubes Manufacturers in India — ranked below the top 5 for this tier (score 0.63); Sachiya Steel — ranked below the top 5 for this tier (score 0.59); Tubes & Valves MFG Co — ranked below the top 5 for this tier (score 0.57); Katariyasteel — ranked below the top 5 for this tier (score 0.39); Risingsteels — ranked below the top 5 for this tier (score 0.34)

### International / global vendors

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Tianyingtai Steel Pipe | MANUFACTURER | China (VERIFIED) | NEAR | HIGH | 0.67 | yes |
| 2 | Forever Steel | MANUFACTURER | China (VERIFIED) | NEAR | HIGH | 0.64 | yes |
| 3 | Glory Steel | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.61 | yes |
| 4 | Sianosteel | MANUFACTURER | China (CLAIMED) | NEAR | MEDIUM | 0.60 | yes |
| 5 | Youfa Steel Pipe | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.60 | yes |
| 6 | Octalsteel | MANUFACTURER | China (VERIFIED) | CATEGORY | MEDIUM | 0.53 | no |

#### 1. Tianyingtai Steel Pipe — NEAR · HIGH confidence · score 0.67
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence tytsteelpipes.com#8))
- **Contact:** https://www.tytsteelpipes.com; +8618522522113; info@tytgg.com.cn
- **Match:** DN40 / OD size stated; standard stated is API 5L, ASTM A53, not IS 1239; 3.2 mm wall mentioned but not tied to this size in one quote
- **Confidence:** vendor's own site/maps evidences size, standard, wall (9 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 1.00, geography delivery 0.45, certification 0.40, source quality 0.90, contactability 1.00 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer with capacity
- **Facts:** Standards [SOURCED] API 5L, ASTM A53 · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [SOURCED] Capacity: 5000 TON · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · MOQ [SOURCED] Minimum order quantity: 20 tons 2) Price: FOB or CIF or CFR at aXin’g… · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [SOURCED]: manufacturer with a stated capacity; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `tytsteelpipes.com#1` (product_match/profile, vendor_site) “China Galvanized 48 3mm Scaffolding Tube Manufacturers ... | Tianjin Tianyingtai Steel Pipe Co., Ltd. is one of the most professional galvanized 48.3mm scaffolding tube …” — [source](https://www.tytsteelpipes.com/showroom/galvanized-48-3mm-scaffolding-tube/)
  - `tytsteelpipes.com#4` (product_match/export, vendor_site) “2 1 2 Inch Black Iron Pipe | . We are a technology-based enterprise focusing on the research and development of Galvanized 48.3mm Scaffolding Tube and solutions. As the …” — [source](https://www.tytsteelpipes.com/showroom/galvanized-48-3mm-scaffolding-tube/)
  - `tytsteelpipes.com#5` (product_match, vendor_site) “Add to Inquiry | Galvanized 48.3mm Scaffolding Tube | Shop from professional Steel Pipe manufacturers and suppliers for quality galvanised 48.3mm scaffolding steel pipe …” — [source](https://www.tytsteelpipes.com/showroom/galvanized-48-3mm-scaffolding-tube/)
  - `tytsteelpipes.com#6` (wall, vendor_site) “Read More | 48.3*3.2mm Scaffolding pipe Hot dip galvanized | Read More” — [source](https://www.tytsteelpipes.com/showroom/galvanized-48-3mm-scaffolding-tube/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details (+5 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 2. Forever Steel — NEAR · HIGH confidence · score 0.64
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence forever-steels.com#18))
- **Contact:** https://www.forever-steels.com; +8615674993216; sales@forever-steels.com
- **Match:** DN40 / OD size stated; standard stated is API 5L, ASTM A53, EN 10217, not IS 1239; 3.2 mm wall mentioned but not tied to this size in one quote
- **Confidence:** vendor's own site/maps evidences size, standard, wall (10 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A53, EN 10217 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `forever-steels.com#1` (standard/product_match/profile, vendor_site) “ERW Steel Pipe Supplier,ASTM A53 Electric Resistance ... | Forever Steel supplies ERW steel pipe and electric resistance welded pipe. Packing: Bundled/In Bulk, Diameter …” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#9` (product_match, vendor_site) “1-1/2" | (48.3 mm) | 1.65 mm – 5.08 mm” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#2` (standard/product_match/profile, vendor_site) “ERW Steel Pipe Supplier,ASTM A53 Electric Resistance ... | Forever Steel supplies ERW steel pipe and electric resistance welded pipe for water,gas,structural and industr…” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#3` (standard/product_match/profile, vendor_site) “ERW Steel Pipe Supplier,ASTM A53 Electric Resistance Welded Pipe | +8615674993216 | sales@forever-steels.com” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details (+6 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 3. Glory Steel — NEAR · MEDIUM confidence · score 0.61
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence glrsteel.com#19))
- **Contact:** https://glrsteel.com
- **Match:** DN40 / OD size stated; standard stated is API 5L, ASTM A53, not IS 1239; required wall 3.2 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A53 · Certs [SOURCED] ISO management-system certificate, test / inspection certificate (men… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `glrsteel.com#9` (product_match, vendor_site) “40 | 48.3 | 3.68” — [source](https://glrsteel.com/product/erw-steel-pipe/)
  - `glrsteel.com#4` (standard, vendor_site) “Galvanized Culvert Pipe | ASTM A53 Gr.B Galvanized Pipe | Galvanized Electrical Conduit” — [source](https://glrsteel.com/product/erw-steel-pipe/)
  - `glrsteel.com#5` (standard, vendor_site) “6” Schedule 40 Steel Pipe | ASTM A53 Gr.B Black Steel Pipe | API 5L Gr.B Carbon Steel Pipe” — [source](https://glrsteel.com/product/erw-steel-pipe/)
  - `glrsteel.com#14` (certification, vendor_site) “✓ | Superior Quality: Our products fully comply with major international standards such as API SPEC 5L and ASTM A53, and hold authoritative certifications including API …” — [source](https://glrsteel.com/product/erw-steel-pipe/)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details (+6 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 4. Sianosteel — NEAR · MEDIUM confidence · score 0.60
- **MANUFACTURER** [SOURCED] · **China** (CLAIMED: only a marketplace listing states 'China' (evidence mk:sianosteel#14); not confirmed on a vendor site or map listing)
- **Contact:** none found in sources
- **Match:** DN40 / OD size stated; standard stated is ASTM A53, BS 1387, EN 10219, not IS 1239; 3.2 mm wall mentioned but not tied to this size in one quote; the matching size/wall row is attributed to a different standard (not IS 1239), so it cannot be treated as an exact match
- **Confidence:** match rests on marketplace / search-snippet text only; location is only claimed, not verified
- **Score:** technical match 0.60, bulk relevance 1.00, geography delivery 0.45, certification 0.60, source quality 0.40, contactability 0.00 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer with capacity
- **Facts:** Standards [SOURCED] ASTM A53, BS 1387, EN 10219 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [SOURCED] Capacity | 1, 500, 000 Tons · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · MOQ [SOURCED] MOQ) | Contact Supplier | Send Inquiry · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [SOURCED]: manufacturer with a stated capacity; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `mk:sianosteel#1` (product_match/wall, marketplace) “48.3mm X 3.2mm Scaffolding Galvanized ERW Steel Pipes | With more than 16 years experience of pipes production, We Tianjin Youfa Steel Pipe Group has won wide praises fr…” — [source](https://sianosteel.en.made-in-china.com/product/GsjQxqJTstVN/China-48-3mm-X-3-2mm-Scaffolding-Galvanized-ERW-Steel-Pipes-Youfa-Brand.html)
  - `mk:sianosteel#4` (product_match/wall, marketplace) “48.3mm X 3.2mm Scaffolding Galvanized ERW Steel Pipes -- Youfa Brand - 2026 Galvanized Steel Pipe, Scaffodling Galvanized Pipes price | Made-in-china.com | Skip to main …” — [source](https://sianosteel.en.made-in-china.com/product/GsjQxqJTstVN/China-48-3mm-X-3-2mm-Scaffolding-Galvanized-ERW-Steel-Pipes-Youfa-Brand.html)
  - `mk:sianosteel#5` (product_match, marketplace) “Steel Pipe & Tube | 48.3mm X 3.2mm Scaffolding Galvanized ERW Steel Pipes -- Youfa Brand | Tianjin Youfa International Trade Co., Ltd.” — [source](https://sianosteel.en.made-in-china.com/product/GsjQxqJTstVN/China-48-3mm-X-3-2mm-Scaffolding-Galvanized-ERW-Steel-Pipes-Youfa-Brand.html)
  - `mk:sianosteel#2` (standard, marketplace) “Producing Standard | BS1387/ ASTM A53/ En39/ En10219 and So on | Steel Material” — [source](https://sianosteel.en.made-in-china.com/product/GsjQxqJTstVN/China-48-3mm-X-3-2mm-Scaffolding-Galvanized-ERW-Steel-Pipes-Youfa-Brand.html)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details (+6 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 5. Youfa Steel Pipe — NEAR · MEDIUM confidence · score 0.60
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence youfasteelpipe.com#1))
- **Contact:** https://www.youfasteelpipe.com
- **Match:** DN40 / OD size stated; standard stated is API 5L, ASTM A500, ASTM A53, BS 1387, EN 10219, EN 10255, not IS 1239; 3.2 mm wall mentioned but not tied to this size in one quote
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A500, ASTM A53, BS 1387, EN 10219, EN 10255 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · MOQ [SOURCED] MOQ | 5 tons · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 500 t (~140,449 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `youfasteelpipe.com#13` (product_match, vendor_site) “4mm | DN40 | 1-1/2"” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
  - `youfasteelpipe.com#14` (product_match, vendor_site) “1-1/2" | 48.3mm | 2.77mm” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
  - `youfasteelpipe.com#26` (product_match, vendor_site) “1.5-15 | 1 1/2” | 48.3” — [source](https://www.youfasteelpipe.com/pid18177355/welded-erw-bs-1387-galvanized-steel-pipe-60-3mm.htm)
  - `youfasteelpipe.com#27` (product_match, vendor_site) “Related Products | en39 scaffolding tube 48.3 steel scaffolding pipe | hot dip Galvanized iron pipe scaffolding steel pipe” — [source](https://www.youfasteelpipe.com/pid18177355/welded-erw-bs-1387-galvanized-steel-pipe-60-3mm.htm)
- **Unresolved:** requirement ambiguity SIZE_BARE_MM: Confirm nominal bore vs outside diameter before issuing the RFQ.; requirement ambiguity CLASS_MEANING: Confirm class B = medium (blue colour band) and the required wall thickness.; exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details (+6 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

**Not shortlisted:** Octalsteel — ranked below the top 5 for this tier (score 0.53)

## 6. M-03 — ERW pipe, DN 80, 89.5 × 4.8 mm, IS 1239

### Ahmedabad vendors

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Rajsagar | MANUFACTURER | Ahmedabad, India (VERIFIED) | NEAR | HIGH | 0.75 | yes |
| 2 | Padmawati Traders | STOCKIST | Ahmedabad, India (VERIFIED) | NEAR | MEDIUM | 0.59 | yes |
| 3 | MN METAL | STOCKIST | Ahmedabad, India (VERIFIED) | NEAR | MEDIUM | 0.58 | yes |
| 4 | Jai Vikas Steel Corporation Private Limited | MS | STOCKIST | Ahmedabad, India (VERIFIED) | CATEGORY | MEDIUM | 0.49 | yes |
| 5 | Navkar Tubes & Tools | STOCKIST | Ahmedabad, India (VERIFIED) | CATEGORY | MEDIUM | 0.49 | yes |
| 6 | Hariom Steel Traders | TRADER | Ahmedabad, India (VERIFIED) | UNVERIFIED | LOW | 0.42 | no |

#### 1. Rajsagar — NEAR · HIGH confidence · score 0.75
- **MANUFACTURER** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Ahmedabad' (evidence rajsagar.com#1))
- **Contact:** https://www.rajsagar.com/; 098989 72828 · **Address:** 103 Sukh Sagar Complex Ashram Road Usmanpura, Next to Fortune Land Mark Hotel, Ashram Road, Usmanpura, Ahmedabad, Gujar…
- **Match:** DN80 / OD size stated; IS 1239 stated; required wall 4.8 mm not confirmed; series 'heavy' mentioned
- **Confidence:** vendor's own site/maps evidences size, standard (9 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 1.00, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A106, ASTM A53, IS 1239, IS 3589 · Certs [SOURCED] ISO management-system certificate, test / inspection certificate (men… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `rajsagar.com#28` (product_match, vendor_site) “3.500 | 88.90 | 3.25” — [source](https://www.rajsagar.com/is-1239-part-1-pipes-supplier-stockist.html)
  - `rajsagar.com#2` (standard/product_match/profile, vendor_site) “IS 1239 PART 1 Pipes Supplier, stockist | Rajsagar Steel one of the largest Stockist and Suppliers of IS 1239. ERW Pipes are widely used and available ・ a manufacturer, …” — [source](https://www.rajsagar.com/is-1239-part-1-pipes-supplier-stockist.html)
  - `rajsagar.com#8` (standard, vendor_site) “Carbon Steel ERW Pipes | IS 1239 PART 1 Pipes | IS 3589 FE 330 Pipes” — [source](https://www.rajsagar.com/)
  - `rajsagar.com#9` (product_match, vendor_site) “ASTM A210 Grade A1 Pipe Tubes | Carbon Steel ERW Pipes | IS 1239 PART 1 Pipes” — [source](https://www.rajsagar.com/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 2. Padmawati Traders — NEAR · MEDIUM confidence · score 0.59
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Vatva' (evidence padmawatitraders.com#1))
- **Contact:** http://www.padmawatitraders.com/; 098983 34675; +91 98983 34675 · **Address:** PLOT NO -44 45/A/12/B Aarkoi Cement Compound Vatva Railway Crossing Over Bridge Road, opp. Yamuna Estate, near Neoplast…
- **Match:** DN80 / OD size stated; no standard stated; required wall 4.8 mm not confirmed
- **Confidence:** own-source support is thin: size on 1 page(s) (NEAR needs 3 kinds, or 2 kinds on 2 pages, for HIGH)
- **Score:** technical match 0.60, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 1.00, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [NEEDS_RFQ] not found in sources - ask for the standard and BIS licence · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Duplicates merged:** Padmawatitraders (padmawatitraders.in)
- **Evidence:**
  - `padmawatitraders.com#5` (product_match, vendor_site) “Mild Steel ERW Pipes | Mild Steel Erw Pipes. Rs 54 / Kg. Whatsapp. Nominal Bore (NB): 3 inch (80 mm); Thickness: 2.0 mm; Length: 6 Meter. Mild Steel ERW (Electric Resist…” — [source](https://www.padmawatitraders.in/erw-pipes.html)
  - `padmawatitraders.com#6` (product_match/profile, vendor_site) “Mild Steel ERW Pipes | ... Pipes and MS Black Pipe offered by Padmavati Traders, Ahmedabad, Gujarat ... Erw Pipe. Rs 56 / Kg. Whatsapp. Shape: Square; Nominal Size (NB):…” — [source](https://www.padmawatitraders.in/erw-pipes.html)
  - `padmawatitraders.com#1` (profile/location, maps) “Padmawati Traders PLOT NO -44 45/A/12/B Aarkoi Cement Compound Vatva Railway Crossing Over Bridge Road, opp. Yamuna Estate, near Neoplast Factory, Phase I, Vatva GIDC, A…” — [source](http://www.padmawatitraders.com/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 3. MN METAL — NEAR · MEDIUM confidence · score 0.58
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Bapunagar' (evidence mnmetal.in#1))
- **Contact:** https://www.mnmetal.in/; 084889 94771 · **Address:** Office No.311, 3rd Floor "BAPUNAGAR ONE" Business Hub, opp. White house, nr. Shyam Sikhar Complex, Bapunagar, Ahmedabad…
- **Match:** DN80 / OD size stated; no standard stated; required wall 4.8 mm not confirmed
- **Confidence:** own-source support is thin: size on 2 page(s) (NEAR needs 3 kinds, or 2 kinds on 2 pages, for HIGH)
- **Score:** technical match 0.60, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239 · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [NEEDS_RFQ] not found in sources - confirm delivery to Ahmedabad and freight terms · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `mnmetal.in#9` (product_match, vendor_site) “Nominal Diameter: | 80 mm (3 inch) | Nominal Bore (NB):” — [source](https://www.mnmetal.in/)
  - `mnmetal.in#21` (product_match, vendor_site) “Nominal Diameter: | 80 mm (3 inch) | Nominal Bore (NB):” — [source](https://mnmetal.in/)
  - `mnmetal.in#1` (location, maps) “MN METAL Office No.311, 3rd Floor "BAPUNAGAR ONE" Business Hub, opp. White house, nr. Shyam Sikhar Complex, Bapunagar, Ahmedabad, Gujarat 380024 084889 94771 https://www…” — [source](https://www.mnmetal.in/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ.

#### 4. Jai Vikas Steel Corporation Private Limited | MS | ERW | GI | GP Pipe Manufacturers and Distributors in Ahmedabad — CATEGORY · MEDIUM confidence · score 0.49
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Ahmedabad' (evidence jaivikas.com#1))
- **Contact:** https://www.jaivikas.com/; 098251 27921 · **Address:** SURVEY NO - 382, SHYAM INDUSTRIAL ESTATE, PLOT NO - 2/3, CANAL ROAD, Changodar, Ahmedabad, Gujarat 382213
- **Match:** ERW pipe supply mentioned; no size evidence for DN80
- **Confidence:** category-level only: supplies ERW/steel pipe but no size evidence
- **Score:** technical match 0.30, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [NEEDS_RFQ] not found in sources - ask for the standard and BIS licence · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `jaivikas.com#1` (product_match/profile/location, maps) “Jai Vikas Steel Corporation Private Limited | MS | ERW | GI | GP Pipe Manufacturers and Distributors in Ahmedabad SURVEY NO - 382, SHYAM INDUSTRIAL ESTATE, PLOT NO - 2/3…” — [source](https://www.jaivikas.com/)
  - `jaivikas.com#2` (product_match/profile/location, maps) “Jai Vikas Steel Corporation Private Limited | MS | ERW | GI | GP Pipe Manufacturers and Distributors in Ahmedabad SURVEY NO - 382, SHYAM INDUSTRIAL ESTATE, PLOT NO - 2/3…” — [source](https://www.jaivikas.com/)
  - `jaivikas.com#3` (product_match/profile, maps) “MS and Mild Steel Pipe | ERW Pipe Dealer | Hot Dip GI Solar ... | Jai Vikas Steel Corporation Pvt. Ltd. Leading MS & Mild Steel Pipe | ERW Pipe Dealer | Hot Dip GI Solar…” — [source](https://www.jaivikas.com/)
  - `jaivikas.com#4` (product_match/profile, vendor_site) “MS and Mild Steel Pipe | ERW Pipe Dealer | Hot Dip GI Solar Pipe | GP & Galvanised Pipe | Mild steel Pipe Wholesalers Suppliers Distributors Manufacturers in Ahmedabad, …” — [source](https://www.jaivikas.com/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Request their product list / catalogue for DN80 and the BIS licence before any RFQ.

#### 5. Navkar Tubes & Tools — CATEGORY · MEDIUM confidence · score 0.49
- **STOCKIST** [SOURCED] · **Ahmedabad, Gujarat, India** (VERIFIED: maps states 'Ahmedabad' (evidence navkartube.com#1))
- **Contact:** https://www.navkartube.com/; 087804 22006 · **Address:** 1426/B, Trikampura Patiya, Phase:3, Vatva GIDC, Ahmedabad, Gujarat 382445
- **Match:** ERW pipe supply mentioned; no size evidence for DN80
- **Confidence:** category-level only: supplies ERW/steel pipe but no size evidence
- **Score:** technical match 0.30, bulk relevance 0.30, geography delivery 1.00, certification 0.00, source quality 0.90, contactability 1.00 — geography/delivery: Ahmedabad presence verified; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [NEEDS_RFQ] not found in sources - ask for the standard and BIS licence · Certs [NEEDS_RFQ] not found in sources - request BIS licence number and mill test certi… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [NEEDS_RFQ] not found in sources - confirm delivery to Ahmedabad and freight terms · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `navkartube.com#2` (product_match/profile, vendor_site) “Navkar Tubes & Tools: MS pipes dealer Ahmedabad | Jindal ... | Navkar Tubes & Tools is an MS pipes dealer and authorized Jindal and Asian pipes dealer in Gujarat. We sto…” — [source](https://navkartube.com/)
  - `navkartube.com#1` (location, maps) “Navkar Tubes & Tools 1426/B, Trikampura Patiya, Phase:3, Vatva GIDC, Ahmedabad, Gujarat 382445 087804 22006 https://www.navkartube.com/” — [source](https://www.navkartube.com/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Request their product list / catalogue for DN80 and the BIS licence before any RFQ.

**Not shortlisted:** Hariom Steel Traders — unverified lead: no quote shows a matching product - listed for follow-up, not shortlisted

### India-based vendors outside Ahmedabad

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Dealonsteel | STOCKIST | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.70 | yes |
| 2 | Maxxon | MANUFACTURER | Chandigarh, India (VERIFIED) | CATEGORY | MEDIUM | 0.68 | yes |
| 3 | Emirerristeel | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.67 | yes |
| 4 | Steelian | STOCKIST | Chennai, India (VERIFIED) | NEAR | HIGH | 0.65 | yes |
| 5 | Exotic Metals LLP | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | HIGH | 0.63 | yes |
| 6 | Steel Pipes/Tubes Manufacturers in India, Top Pi | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | HIGH | 0.63 | no |
| 7 | Sachiya Steel | MANUFACTURER | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.59 | no |
| 8 | Tubes & Valves MFG Co | MANUFACTURER | Chennai, India (VERIFIED) | NEAR | MEDIUM | 0.57 | no |
| 9 | APOLLON STEEL INC. | STOCKIST | Mumbai, India (VERIFIED) | NEAR | HIGH | 0.56 | no |
| 10 | RP Sales | STOCKIST | Kanpur, India (VERIFIED) | NEAR | MEDIUM | 0.54 | no |
| 11 | Risingsteels | TRADER | Mumbai, India (VERIFIED) | NEAR | MEDIUM | 0.43 | no |
| 12 | Katariyasteel | STOCKIST | Mumbai, India (VERIFIED) | CATEGORY | MEDIUM | 0.39 | no |

#### 1. Dealonsteel — NEAR · MEDIUM confidence · score 0.70
- **STOCKIST** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence dealonsteel.com#38); also located in Navi Mumbai)
- **Contact:** https://dealonsteel.com
- **Match:** DN80 / OD size stated; IS 1239 stated; required wall 4.8 mm not confirmed; series 'heavy' mentioned
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.38, geography delivery 0.90, certification 1.00, source quality 0.90, contactability 0.50 — geography/delivery: delivery to Ahmedabad/Gujarat stated; bulk relevance: stockist with stock (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239 · Certs [SOURCED] BIS / ISI mark, test / inspection certificate (mentioned; certificate… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer mentioning stock; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `dealonsteel.com#13` (product_match, vendor_site) “6.18 – 8.83 | 80 NB | 3″” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
  - `dealonsteel.com#14` (product_match, vendor_site) “3″ | 88.9 | 3.2” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
  - `dealonsteel.com#26` (product_match, vendor_site) “Structural and engineering projects | 80 NB | Large Range” — [source](https://dealonsteel.com/ms-pipes/top-ms-pipe-dealers-in-ahmedabad/)
  - `dealonsteel.com#1` (standard, vendor_site) “Jindal Pipe Weight Chart 2026 – MS & GI ... | The following Jindal MS and GI pipe weight chart is based on standard IS 1239 dimensions widely used across construction, p…” — [source](https://dealonsteel.com/jindal-pipes/jindal-pipe-weight-chart/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 2. Maxxon — CATEGORY · MEDIUM confidence · score 0.68
- **MANUFACTURER** [SOURCED] · **Chandigarh, Punjab, India** (VERIFIED: vendor site states 'Chandigarh' (evidence maxxon.in#7))
- **Contact:** https://maxxon.in
- **Match:** ERW pipe supply mentioned; no size evidence for DN80
- **Confidence:** category-level only: supplies ERW/steel pipe but no size evidence
- **Score:** technical match 0.30, bulk relevance 0.70, geography delivery 0.90, certification 1.00, source quality 0.90, contactability 0.50 — geography/delivery: delivery to Ahmedabad/Gujarat stated; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] IS 1161, IS 1239, IS 3589, IS 3601, IS 4923 · Certs [SOURCED] BIS / ISI mark (mentioned; certificate numbers not verified) · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `maxxon.in#1` (standard/product_match/profile, vendor_site) “ERW Steel Pipes Supplier in Gujarat | Maxxon | Maxxon Steel supplies ERW steel pipes in Gujarat in multiple dimensions to meet diverse industry requirements. · IS 1239 E…” — [source](https://maxxon.in/erw-steel-pipe-supplier-in-gujarat/)
  - `maxxon.in#2` (standard, vendor_site) “Certifications Associated | Our ERW pipes are manufactured in compliance with the Indian Standard IS:4923,IS:3601 & IS:1161, ensuring they meet stringent quality and saf…” — [source](https://maxxon.in/erw-steel-pipe-supplier-in-gujarat/)
  - `maxxon.in#3` (product_match/profile, vendor_site) “ERW Steel Pipes Supplier in Gujarat | Maxxon | Home | About” — [source](https://maxxon.in/erw-steel-pipe-supplier-in-gujarat/)
  - `maxxon.in#4` (stock/delivery, vendor_site) “Our Punjab-based manufacturing facility follows advanced production technology and strict quality control processes to ensure high strength, uniform wall thickness, and …” — [source](https://maxxon.in/erw-steel-pipe-supplier-in-gujarat/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Request their product list / catalogue for DN80 and the BIS licence before any RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 3. Emirerristeel — NEAR · MEDIUM confidence · score 0.67
- **MANUFACTURER** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence emirerristeel.com#14))
- **Contact:** https://emirerristeel.com
- **Match:** DN80 / OD size stated; IS 1239 stated; required wall 4.8 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.40, certification 1.00, source quality 0.90, contactability 0.50 — geography/delivery: India-based; delivery to Ahmedabad plausible but unconfirmed; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] EN 10217, EN 10219, EN 10255, IS 1239 · Certs [SOURCED] BIS / ISI mark (mentioned; certificate numbers not verified) · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `emirerristeel.com#10` (product_match, vendor_site) “4.47 / 7.90 | 3″ / 80 mm | 3.500 / 88.90” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#2` (standard/class, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C | IS 1239 ; Specification, Mild Steel Tubes for Water, Gas, Air, and Steam ; Size Range, 1/8" NB to 20" NB (Nominal Bore) ; Outer…” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#3` (standard/class/certification, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C | IS 1239 GI Pipes Part 1 & 2 available in Class A, B, C – ideal for water, gas & structural use. Durable, corrosion-resistant, a…” — [source](https://emirerristeel.com/is-1239/)
  - `emirerristeel.com#4` (standard/class, vendor_site) “IS 1239 GI Pipe Part 1, 2 Class A, B ,C - Emirerristeel | Welcome to Emirerri Steel Manufacturer Pvt Ltd | About us” — [source](https://emirerristeel.com/is-1239/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 4. Steelian — NEAR · HIGH confidence · score 0.65
- **STOCKIST** [SOURCED] · **Chennai, Tamil Nadu, India** (VERIFIED: vendor site states 'Chennai' (evidence steelian.com#15))
- **Contact:** https://steelian.com; +91-9888-2444
- **Match:** DN80 / OD size stated; IS 1239 stated; required wall 4.8 mm not confirmed
- **Confidence:** vendor's own site/maps evidences series, size, standard (8 quote(s), 1 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.30, geography delivery 0.90, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: delivery to Ahmedabad/Gujarat stated; bulk relevance: stockist (x0.75: large order, mill-direct realistic)
- **Facts:** Standards [SOURCED] IS 1239, IS 3589 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] Ahmedabad/Gujarat delivery stated · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: stockist/dealer, stock not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. At this tonnage a mill-direct or large-stock source is more realistic. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `steelian.com#5` (standard/product_match/profile, vendor_site) “Mild Steel Erw Pipe Dealers in Ahmedabad Suppliers ... | MS ERW Pipe IS 1239 dealers in Ahmedabad, MS ERW Tubes IS 1239 Suppliers ... 80 MM NB, 100 MM NB, 125 MM NB , 15…” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
  - `steelian.com#10` (product_match, vendor_site) “: | IS 1239 : 1/2″ NB, 1″ NB, 1 1/2″ NB, 2″ NB, 3″ NB, 4″ NB, 5″ NB, 6″ NB, 25 MM NB , 32 MM NB , 40 MM NB, 65 MM NB, 80 MM NB, 100 MM NB, 125 MM NB , 150 MM NB | IS 358…” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
  - `steelian.com#1` (standard/product_match/profile, vendor_site) “Mild Steel Erw Pipe Dealers in Ahmedabad Suppliers ... | ERW Pipe IS 1239 dealers in Ahmedabad, 5′′ NB, 6′′ call us at +91-9888-2444-54” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
  - `steelian.com#3` (standard/product_match/profile, vendor_site) “Mild Steel Erw Pipe Dealers in Ahmedabad Suppliers ... | MS ERW Pipe IS 1239 dealers in Ahmedabad, 5′′ NB, 6′′ call us at +91-9888-2444-54” — [source](https://steelian.com/ms-erw-pipe-dealers-in-ahmedabad/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

#### 5. Exotic Metals LLP — NEAR · HIGH confidence · score 0.63
- **MANUFACTURER** [SOURCED] · **Mumbai, Maharashtra, India** (VERIFIED: vendor site states 'Mumbai' (evidence exoticmetalsllp.com#11); also located in Navi Mumbai)
- **Contact:** https://exoticmetalsllp.com; +91 75065 95134; +91 22 66159052
- **Match:** DN80 / OD size stated; IS 1239 stated; required wall 4.8 mm not confirmed
- **Confidence:** vendor's own site/maps evidences series, size, standard (2 quote(s), 1 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.40, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: India-based; delivery to Ahmedabad plausible but unconfirmed; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A53, BS 1387, IS 1239, IS 3589 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned (India mentioned) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `exoticmetalsllp.com#5` (product_match, vendor_site) “Medium (Class B) | 80 NB | 88.9” — [source](https://exoticmetalsllp.com/erw-pipe-manufacturer-stockist-exporter-india.php)
  - `exoticmetalsllp.com#2` (standard, vendor_site) “Standard Specifications | ASTM A53 Grade A & B, API 5L (Gr B to X80), IS 1239, IS 3589, BS 1387 | Length” — [source](https://exoticmetalsllp.com/erw-pipe-manufacturer-stockist-exporter-india.php)
  - `exoticmetalsllp.com#11` (location, vendor_site) “Lane Khetwadi Main Road, Charni Road East, Khetwadi, Sicka Nagar, Mumbai, Maharashtra 400004” — [source](https://exoticmetalsllp.com/erw-pipe-manufacturer-stockist-exporter-india.php)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for freight cost and transit time to Ahmedabad.

**Not shortlisted:** Steel Pipes/Tubes Manufacturers in India — ranked below the top 5 for this tier (score 0.63); Sachiya Steel — ranked below the top 5 for this tier (score 0.59); Tubes & Valves MFG Co — ranked below the top 5 for this tier (score 0.57); APOLLON STEEL INC. — ranked below the top 5 for this tier (score 0.56); RP Sales — ranked below the top 5 for this tier (score 0.54); Risingsteels — ranked below the top 5 for this tier (score 0.43); Katariyasteel — ranked below the top 5 for this tier (score 0.39)

### International / global vendors

| # | Vendor | Type | Location | Match | Confidence | Score | Shortlisted |
|---|---|---|---|---|---|---|---|
| 1 | Forever Steel | MANUFACTURER | China (VERIFIED) | NEAR | HIGH | 0.64 | yes |
| 2 | Glory Steel | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.61 | yes |
| 3 | Octalsteel | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.61 | yes |
| 4 | Youfa Steel Pipe | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.60 | yes |
| 5 | Eastern Steels | MANUFACTURER | China (VERIFIED) | NEAR | MEDIUM | 0.54 | yes |

#### 1. Forever Steel — NEAR · HIGH confidence · score 0.64
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence forever-steels.com#18))
- **Contact:** https://www.forever-steels.com; +8615674993216; sales@forever-steels.com
- **Match:** DN80 / OD size stated; standard stated is API 5L, ASTM A53, EN 10217, not IS 1239; required wall 4.8 mm not confirmed; series 'heavy' mentioned
- **Confidence:** vendor's own site/maps evidences size, standard (8 quote(s), 2 page(s)); location verified; no conflicts; phone/email found
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 1.00 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A53, EN 10217 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `forever-steels.com#11` (product_match, vendor_site) “Systems | 3" (88.9 | mm)” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#2` (standard/product_match/profile, vendor_site) “ERW Steel Pipe Supplier,ASTM A53 Electric Resistance ... | Forever Steel supplies ERW steel pipe and electric resistance welded pipe for water,gas,structural and industr…” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#3` (standard/product_match/profile, vendor_site) “ERW Steel Pipe Supplier,ASTM A53 Electric Resistance Welded Pipe | +8615674993216 | sales@forever-steels.com” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
  - `forever-steels.com#4` (standard, vendor_site) “SSAW Steel Pipe | ASTM A53 Steel Pipe | Hollow Sections” — [source](https://www.forever-steels.com/products-detail/erw-steel-pipe)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ (+4 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 2. Glory Steel — NEAR · MEDIUM confidence · score 0.61
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence glrsteel.com#19))
- **Contact:** https://glrsteel.com
- **Match:** DN80 / OD size stated; standard stated is API 5L, ASTM A53, not IS 1239; required wall 4.8 mm not confirmed; series 'heavy' mentioned
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A53 · Certs [SOURCED] ISO management-system certificate, test / inspection certificate (men… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `glrsteel.com#10` (product_match, vendor_site) “2-1/2” Galvanized Pipe | 3” Galvanized Pipe | Sch 40 Galvanized Steel Pipe” — [source](https://glrsteel.com/product/erw-steel-pipe/)
  - `glrsteel.com#11` (product_match, vendor_site) “80 | 88.9 | 5.49” — [source](https://glrsteel.com/product/erw-steel-pipe/)
  - `glrsteel.com#26` (product_match, vendor_site) “2-1/2” Galvanized Pipe | 3” Galvanized Pipe | Sch 40 Galvanized Steel Pipe” — [source](https://glrsteel.com/)
  - `glrsteel.com#27` (product_match, vendor_site) “PVC Coated Rigid Conduit | 3” Galvanized Pipe | Latest Cases” — [source](https://glrsteel.com/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ (+4 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 3. Octalsteel — NEAR · MEDIUM confidence · score 0.61
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence octalsteel.com#17))
- **Contact:** https://www.octalsteel.com
- **Match:** DN80 / OD size stated; standard stated is API 5L, ASTM A135, ASTM A53, EN 10219, not IS 1239; required wall 4.8 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.60, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A135, ASTM A53, EN 10219 · Certs [SOURCED] test / inspection certificate (mentioned; certificate numbers not ver… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `octalsteel.com#9` (product_match, vendor_site) “3 | 88.9 | 5.49” — [source](https://www.octalsteel.com/resources/erw-pipe/)
  - `octalsteel.com#1` (standard/product_match/certification, vendor_site) “ERW Steel Pipe | High-frequency ERW steel pipe and API 5L ERW line pipe for onshore oil, gas, water and structural service, with tight tolerances, NDT and 3.1/3.2 MTC.” — [source](https://www.octalsteel.com/resources/erw-pipe/)
  - `octalsteel.com#2` (standard/product_match, vendor_site) “ERW Steel Pipe | Octal Steel supplies ERW steel pipe and API 5L ERW line pipe from qualified and audited mills, covering international standards for fluid service, line …” — [source](https://www.octalsteel.com/resources/erw-pipe/)
  - `octalsteel.com#3` (standard/product_match, vendor_site) “ERW Steel Pipe | Contact Now ! · Type: High-frequency ERW pipe & API 5L ERW pipe · Size Range: 1/2″–24″ OD, 1.8–16 mm WT · Standards: API 5L, ASTM A53, ASTM A135, EN 102…” — [source](https://www.octalsteel.com/resources/erw-pipe/)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ (+4 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 4. Youfa Steel Pipe — NEAR · MEDIUM confidence · score 0.60
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence youfasteelpipe.com#1))
- **Contact:** https://www.youfasteelpipe.com
- **Match:** DN80 / OD size stated; standard stated is API 5L, ASTM A500, ASTM A53, BS 1387, EN 10219, EN 10255, not IS 1239; required wall 4.8 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.45, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: export mentioned (India not named); bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A500, ASTM A53, BS 1387, EN 10219, EN 10255 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Export [SOURCED] export / overseas supply mentioned · MOQ [SOURCED] MOQ | 5 tons · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `youfasteelpipe.com#16` (product_match, vendor_site) “4.5mm | DN80 | 3"” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
  - `youfasteelpipe.com#17` (product_match, vendor_site) “3" | 88.9mm | 3.05mm” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
  - `youfasteelpipe.com#29` (product_match, vendor_site) “0.8-4.0 | 3” | 88.9” — [source](https://www.youfasteelpipe.com/pid18177355/welded-erw-bs-1387-galvanized-steel-pipe-60-3mm.htm)
  - `youfasteelpipe.com#7` (standard, vendor_site) “ERW Steel Pipe Standards | ASTM A53, ASTM A500, ASTM A795, API 5L, BS1387, BS1139, EN39, EN10219, EN10255, JIS G3444, ISO65 | GB/T3091, GB/T13793” — [source](https://www.youfasteelpipe.com/products2088894/Erw-Steel-Pipe.htm)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ (+4 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

#### 5. Eastern Steels — NEAR · MEDIUM confidence · score 0.54
- **MANUFACTURER** [SOURCED] · **China** (VERIFIED: vendor site states 'China' (evidence eastern-steels.com#12))
- **Contact:** https://www.eastern-steels.com
- **Match:** DN80 / OD size stated; standard stated is API 5L, ASTM A500, ASTM A53, EN 10217, not IS 1239; required wall 4.8 mm not confirmed
- **Confidence:** no phone or email found in any source, so the vendor cannot yet be contacted from this output
- **Score:** technical match 0.60, bulk relevance 0.70, geography delivery 0.15, certification 0.50, source quality 0.90, contactability 0.50 — geography/delivery: no export evidence; bulk relevance: manufacturer
- **Facts:** Standards [SOURCED] API 5L, ASTM A500, ASTM A53, EN 10217 · Certs [SOURCED] ISO management-system certificate (mentioned; certificate numbers not… · Capacity [NEEDS_RFQ] not found in sources - ask for monthly capacity / stock at RFQ · Delivery [SOURCED] delivery mentioned (area not specific) · Price/lead time [NEEDS_RFQ]
- **Bulk feasibility** [NEEDS_RFQ]: manufacturer (self-declared), capacity not stated; required 1,200 t (~121,212 m) - unit ASSUMED to be tonnes. Monthly capacity, ready stock and lead time must be confirmed by RFQ.
- **Evidence:**
  - `eastern-steels.com#8` (product_match, vendor_site) “3 | 88.9 | 3.05” — [source](https://www.eastern-steels.com/newsdetail/erw-pipe-specifications-and-models.html)
  - `eastern-steels.com#2` (standard/product_match, vendor_site) “ERW Pipe Specifications and Size Chart (2026 Guide) | ASTM A53 covers ERW steel pipe used for general fluid transportation, water systems, steam lines, and industrial pi…” — [source](https://www.eastern-steels.com/newsdetail/erw-pipe-specifications-and-models.html)
  - `eastern-steels.com#3` (standard, vendor_site) “These specifications are used by engineers, contractors, and procurement teams to ensure the pipe meets pressure, structural, and transportation requirements. Common ERW…” — [source](https://www.eastern-steels.com/newsdetail/erw-pipe-specifications-and-models.html)
  - `eastern-steels.com#4` (standard, vendor_site) “, ASTM A500, | API 5L | , EN 10217, and ISO 3183, each covering different industrial applications and dimensional ranges.” — [source](https://www.eastern-steels.com/newsdetail/erw-pipe-specifications-and-models.html)
- **Unresolved:** exact product (size + wall + standard in one specification) not confirmed by a source; BIS licence / ISI mark not evidenced; manufacturer status is self-declared - verify via BIS licence / plant details; capacity / ready stock not stated; price, lead time and MOQ require an RFQ (+4 more in JSON/CSV)
- **Next step:** Send a technical clarification first: confirm they can supply the exact size, wall thickness and standard (see match reasons), then RFQ. Ask for the equivalent international standard (EN 10255 / BS 1387 / ASTM), MOQ, container loading, lead time and FOB/CIF terms; check Indian import compliance first.

## 7. Leads whose location could not be established (50)

These were surfaced by a search but no source quote gave an address (page blocked, JS-rendered, or not fetched within the verification budget). They are **not placed in any geography** — the 'surfaced by' column is only the search that found them, not their location. Verify the address before treating any as Ahmedabad / India / global.

| Vendor | Surfaced by | Site | Best match class | Why not located |
|---|---|---|---|---|
| Everest Metal | ahmedabad, india_other, global | http://everestmetal.in | NEAR | no location evidence found |
| Lgpipeindia | india_other | https://www.lgpipeindia.com | NEAR | no location evidence found |
| Baolaipipes | global | https://baolaipipes.com | CATEGORY | no location evidence found |
| Dinesh Metal Industries | global | https://www.dmitubes.com | CATEGORY | no location evidence found |
| Navstarsteel | global | https://www.navstarsteel.com | CATEGORY | no location evidence found |
| Steeltubesindia | ahmedabad, india_other, global | https://www.steeltubesindia.net | CATEGORY | no location evidence found |
| Aesteiron | global | https://www.aesteiron.com | UNVERIFIED | no location evidence found |
| Anamica Pipes & Tubes-Stockist-MS & CS Seaml | ahmedabad | https://www.google.com | UNVERIFIED | no location evidence found |
| Ans Pipes Ltd - Apl Apollo Tubes Pipes Ltd | ahmedabad | http://www.anspipes.com/ | UNVERIFIED | no location evidence found |
| ARIHANT ENTERPRISE | ahmedabad | http://www.arihantenterprises.co/ | UNVERIFIED | no location evidence found |
| Beveled | global | mk:beveled | UNVERIFIED | no location evidence found |
| Bhaveshmetals | ahmedabad | https://bhaveshmetals.com | UNVERIFIED | no location evidence found |
| Brooksindustrialmetals | global | https://brooksindustrialmetals.com | UNVERIFIED | no location evidence found |
| Compliant with ASTM A53 & | global | mk:compliant-with-astm-a53 | UNVERIFIED | no location evidence found |
| Coremarkmetals | global | https://www.coremarkmetals.com | UNVERIFIED | no location evidence found |
| Engineeringtoolbox | global | https://www.engineeringtoolbox.com | UNVERIFIED | no location evidence found |
| ERW Pipe — California Steel Industries | global | https://www.californiasteel.com | UNVERIFIED | no location evidence found |
| ERW Steel Pipe | global | https://www.johosteelpipe.com | UNVERIFIED | no location evidence found |
| ERW steel pipe manufacturer & supplier from  | global | https://winsteelpipes.com | UNVERIFIED | no location evidence found |
| Ganesh Steel Tubes | ahmedabad | https://shreeganeshsteelpipes.com/products/carbon-steel-pipes | UNVERIFIED | no location evidence found |
| Gautamtube | global | https://www.gautamtube.com | UNVERIFIED | no location evidence found |
| Goyal Pipes and Tubes | ahmedabad | http://goyalpipesandtubes.com/ | UNVERIFIED | no location evidence found |
| Hitechoverseas | global | https://www.hitechoverseas.com | UNVERIFIED | no location evidence found |
| Hu Steel | india_other, global | https://www.hu-steel.com | UNVERIFIED | no location evidence found |
| Kantilal Enterprise (pipes and fittings supp | ahmedabad | https://www.google.com | UNVERIFIED | no location evidence found |
| KHADKA-G STEEL CORPORATION | ahmedabad | http://www.khadkagsteel.com/ | UNVERIFIED | no location evidence found |
| Landee | global | https://www.landeepipe.com | UNVERIFIED | no location evidence found |
| Madrassteels | india_other, ahmedabad | https://www.madrassteels.in | UNVERIFIED | no location evidence found |
| Neelconsteel | india_other | https://www.neelconsteel.com | UNVERIFIED | no location evidence found |
| Oshwin | global | https://www.oshwin.com | UNVERIFIED | no location evidence found |
| Padmavati Tubes | ahmedabad | https://www.google.com | UNVERIFIED | no location evidence found |
| Pandapipe | global | https://pandapipe.com | UNVERIFIED | no location evidence found |
| Pipeandsections | global | https://pipeandsections.com | UNVERIFIED | no location evidence found |
| Prices Manufacturers & Suppliers | india_other | mk:prices-manufacturers-suppli | UNVERIFIED | no location evidence found |
| PS Steel | global | https://pssteel.co.in | UNVERIFIED | no location evidence found |
| Raj Rajeshwari Metal Impex-Stockist-Seamless | ahmedabad | https://www.google.com | UNVERIFIED | no location evidence found |
| Ratnabhumi Steeltech Private Limited | ahmedabad | https://ratnasteeltech.com/ | UNVERIFIED | no location evidence found |
| Rexaltubes | global | https://www.rexaltubes.com | UNVERIFIED | no location evidence found |
| Saisteeltube | ahmedabad | https://www.saisteeltube.com | UNVERIFIED | no location evidence found |
| Shreerajaramsteelindia | ahmedabad | https://www.shreerajaramsteelindia.com | UNVERIFIED | no location evidence found |
| Siddhagirimetals | global | https://www.siddhagirimetals.com | UNVERIFIED | no location evidence found |
| Srjsteel | india_other | https://srjsteel.in | UNVERIFIED | no location evidence found |
| Steel dealers | ahmedabad | https://www.indiamart.com/steeldealers/ | UNVERIFIED | no location evidence found |
| Tridentsteel | india_other | https://www.tridentsteel.co.in | UNVERIFIED | no location evidence found |
| Triloksteel | global | https://www.triloksteel.com | UNVERIFIED | no location evidence found |
| Tubetrading | ahmedabad, india_other | http://www.tubetrading.in | UNVERIFIED | no location evidence found |
| Tubewell | global | https://www.tubewell.co.in | UNVERIFIED | no location evidence found |
| Unitedpipe | global | https://unitedpipe.com | UNVERIFIED | no location evidence found |
| Vishwastubes | global | https://www.vishwastubes.com | UNVERIFIED | no location evidence found |
| Youfaconstruction | global | https://www.youfaconstruction.com | UNVERIFIED | no location evidence found |

## Run log, failures and exclusions

- **Page fetch failures:** 30
  - https://www.navkartube.com/ — page has no extractable text (JS-rendered or blocked)
  - https://navkartube.com/ — page has no extractable text (JS-rendered or blocked)
  - https://www.lgpipeindia.com/is-1239-yst-210-240-310-355-pipes-tubes.html — HTTP 403
  - https://lgpipeindia.com/ — HTTP 403
  - https://lgpipeindia.com/contact-us — HTTP 403
  - https://lgpipeindia.com/contact — HTTP 403
  - https://lgpipeindia.com/contact-us.html — HTTP 403
  - https://www.risingsteels.com/blog/bs1387-tube.html — HTTP 403
  - https://www.risingsteels.com/is-1239-mild-steel-pipe.html — HTTP 403
  - https://baolaipipes.com/standards-grades-testing/astm-a53-erw-pipe-specifications-guide/ — HTTP 403
  - https://everestmetal.in/contact-us — HTTP 404
  - https://baolaipipes.com/ — HTTP 403
  - … (full list in result.json)
- **Claims dropped by the evidence gate:** 0
- **Search results excluded before becoming vendors:** 70
  - non-vendor content (reference / social / government / trade data) — 40: (48.3mm) scaffolding tubes in-house — da; Approved Manufacturers of Steel Pipes | ; BS1387 ERW Steel Tube Specifications | P; ERW Welded Pipe Mill for carbon steel & 
  - marketplace page with no identifiable seller (category / search page) - follow it manually to find sellers — 29: China 48.3 Pipe(999+); ERW Pipes in Ahmedabad, Gujarat; ERW Pipes in Jaipur, Rajasthan; ERW Pipes in Vadodara, Gujarat
  - informational article / list, not a vendor page — 1: List Of Top ERW Pipe Manufacturers & Sup
- **Warnings / errors:** 4
  - [normalise] 4 critical ambiguities - proceeding with logged assumptions
  - [coverage] M-01/UNRESOLVED: ONLY_UNVERIFIED_LEADS (found 27)
  - [coverage] M-02/UNRESOLVED: ONLY_UNVERIFIED_LEADS (found 34)
  - [coverage] M-03/UNRESOLVED: ONLY_UNVERIFIED_LEADS (found 28)

## Assumptions in force

- [M-01] WALL_NOT_IN_STANDARD: Kept 5.5 mm as written. Vendors are searched for it AND for the nearest IS 1239 series; those without a 5.5 mm product are NEAR matches at best.
- [M-01] STANDARD_SCOPE_NOTE: Vendors quoting another standard are classed NEAR, not EXACT.
- [M-01] QTY_UNIT_MISSING: Assumed 1000 tonnes (~134,535 m, ~22,422 x 6 m lengths).
- [M-02] SIZE_BARE_MM: Treated as DN40 nominal bore. The OD-40 mm reading is kept as an alternate search.
- [M-02] STANDARD_NOT_STATED: Assumed IS 1239 (Part 1) because 'Class B' is the Indian trade shorthand for its medium series.
- [M-02] CLASS_MEANING: Read as IS 1239 medium series; wall thickness taken from the BIS table.
- [M-02] STANDARD_SCOPE_NOTE: Vendors quoting another standard are classed NEAR, not EXACT.
- [M-02] QTY_UNIT_MISSING: Assumed 500 tonnes (~140,449 m, ~23,408 x 6 m lengths).
- [M-03] OD_AT_LIMIT: Kept 89.5 mm as written; searches also use the nominal 88.9 mm.
- [M-03] STANDARD_SCOPE_NOTE: Vendors quoting another standard are classed NEAR, not EXACT.
- [M-03] QTY_UNIT_MISSING: Assumed 1200 tonnes (~121,212 m, ~20,202 x 6 m lengths).
- Evidence is limited to public web sources found by the search provider; absence of evidence is reported as 'not found', never as a negative fact.
- Manufacturer / trader status comes from the vendor's own wording and is self-declared.
- Prices, lead times, stock and MOQ are never estimated; they are marked NEEDS_RFQ.
- Ranking weights and confidence rules are those in config (technical_match 30%, bulk_relevance 20%, geography_delivery 20%, certification 15%, source_quality 10%, contactability 5%).
