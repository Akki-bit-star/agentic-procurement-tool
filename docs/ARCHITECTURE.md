# Architecture note — the agentic harness

## The problem, decomposed

Buying 500–1,200 (assumed) tonnes of ERW pipe is not one question. It is five:

1. **What exactly is being bought?** The input is ambiguous (no quantity unit, "40 mm", "Class B", a wall thickness that
   is not in the cited standard). → *deterministic normalisation*
2. **Who might supply it?** Three different markets with different vocabularies (Ahmedabad dealers, Indian mills,
   overseas exporters who never write "IS 1239"). → *search agents, one per tier*
3. **Are they real, where are they, and do they make this?** Marketplaces mislabel cities; titles are not names. →
   *entity resolution + verification agent + evidence gate*
4. **Can they do this volume and deliver to Ahmedabad?** → *deterministic feasibility reasoning, labelled as inference*
5. **What should the buyer do next?** → *ranked shortlist, explicit assumptions, RFQ next steps*

## Design principle: the model reasons, code decides

LLMs are used only where language understanding genuinely helps. Today that is exactly two places: labelling messy search
results (vendor name / type) and picking quotable passages from a fetched page. Everything that decides *what is believed*
is plain code:

| Decision | Done by | Why |
|---|---|---|
| Parse the requirement, detect ambiguity, cross-check against IS 1239 | rules + BIS table | must be exact and explainable |
| Which text is admitted as evidence | **evidence gate** (code) | the anti-hallucination control |
| Facts about a vendor (standard, size, wall, certs, capacity…) | regexes over *quotes* | reproducible; a model cannot assert what a quote does not show |
| Geography tier (Ahmedabad / India / global) | gazetteer + evidence | auditable; "export to India" ≠ "is in India" |
| Match class, score, confidence, shortlist | deterministic rules + config weights | same evidence ⇒ same ranking |
| Candidate vendor names, quote selection | LLM (optional) + rules fallback | language-heavy, low-stakes, re-verified |
| Which query to run next / which page to read next | **rules** in workflow mode · **the model** in agent mode (`--agent`) | workflow = predictable quota use; agent = adaptive, bounded by the same budgets and gate |

The system **runs fully without an LLM** (rules-only mode). The LLM raises recall and name quality; it cannot raise a
vendor's rank by inventing facts, because its output must be verbatim quotes that the gate re-checks against the fetched
source text.

## Workflow

```
Input (JSON/CLI/UI)
  │
  ▼ 1 NORMALISE           parse → resolve vs IS 1239 table → flags (CRITICAL/WARNING/INFO) + provenance per field
  │                       original input is never overwritten; QTY unit assumption is logged (or --strict stops)
  ▼ 2 PLAN                per material × tier: query variants (primary reading + alternates)
  │                       Ahmedabad: web + Google-Maps places · India: IS 1239 vocabulary · Global: OD/wall + EN/BS/ASTM
  ▼ 3 DISCOVER (agent loop, per material × tier)
  │     search → draft candidates → reflect on this tier's coverage → reformulate (round 2) if thin
  │     bounded by query caps + a global search-quota budget; failed searches are logged, never fatal
  ▼ 4 RESOLVE             drop non-vendors/unnamed listings (with reasons) · dedupe by domain / phone / name similarity
  ▼ 5 VERIFY (agent, parallel)
  │     fetch ≤2 pages (SSRF-guarded, robots.txt, size/time limits) → pick quotes (rules ± LLM)
  │     → EVIDENCE GATE → if no address: follow contact/about page (reflection step)
  ▼ 6 GEOGRAPHY           evidence → tier + status VERIFIED / CLAIMED / WEAK / UNKNOWN; conflicts recorded
  ▼ 7 ASSESS              match class → six-component score → confidence → bulk feasibility → next step
  ▼ 8 REPORT              result.json (source of truth) · report.md · per-tier CSVs
```

## Two execution modes (same pipeline, same evidence gate, same scoring)

**Workflow mode (default; the committed demo).** A code-orchestrated workflow. Stages 3 and 5 are stateful, tool-using loops
with *rule-driven* adaptive control flow: they inspect what has been found (tier coverage below target → run a relaxed
query; no address on a vendor-owned page → follow its contact page; 403 → stop hitting that host), act under hard budgets,
recover from failures, and write to a shared evidence ledger. No model decides the next action; the optional LLM only
labels and extracts inside the loops. The committed demo made zero LLM calls.

**Agent mode (`--agent`, any tool-calling provider via `--llm gemini|groq|openrouter|ollama|openai`).** Stages 3 and 5 are
replaced by one **model-directed research agent per (material × geography)**:

```
system prompt: requirement + resolved spec + ambiguity flags + geography brief + budgets + suggested (cached) queries
loop (≤ max_steps):  model ──tool call──▶ search_web | search_places | read_page | record_evidence | status | finish
                       ▲                                   │
                       └──── compact JSON result ◀─────────┘   (record_evidence → EVIDENCE GATE → accepted / rejected + reason)
```

* **The model decides**: what to search, scope (India/global), which candidate pages to read, when to follow a contact
  page, which passages to record as evidence, when it has enough.
* **The model does not decide**: whether a quote is admitted (the gate re-checks it against the fetched text; a rejection is
  returned to the model as feedback so it can retry with an exact copy), where a vendor is, how it scores or ranks.
* **Bounded**: `max_steps`, `max_searches`, `max_reads` per agent, the global search-quota guard, a global LLM-call budget, and
  a circuit breaker (auth/billing/daily-quota errors disable the LLM once and the run continues).
* **Backstop**: vendors the agent never gathered ≥2 evidence items for go through the deterministic page verification, so a
  weak or rate-limited model can lower recall but never silently drop a candidate. Agent- and rules-evidence share one ledger.
* **Cheap / small-token friendly**: tool outputs are compact digests (not pages), old tool results are elided from history
  (`status` restores the candidate ledger), calls are paced to `requests_per_minute`, 429s are retried with `retry-after`.
* **Replayable**: every model turn is cached by request hash, so an agent run can be replayed offline with `--replay`.

Workflow mode is the baseline; `procure compare A B` shows what agent mode changes (recall, evidence, shortlist).

## Where the evidence trail lives

* `Evidence` = verbatim quote + URL + fetch time + source kind (`vendor_site` / `maps` / `marketplace`).
* `State.gate()` admits an item only if the quote is found in the recorded text of that URL; rejected claims are kept in
  `dropped_claims` and printed in the report.
* Quotes are merged per distinct passage (one passage cannot count as several "independent" confirmations).
* Every vendor fact carries a provenance label: `SOURCED` (cites evidence ids) · `DERIVED` · `REFERENCE` (BIS table) ·
  `ASSUMED` · `NEEDS_RFQ`. Price and lead time are *always* `NEEDS_RFQ`.

## Failure handling

| Failure | Behaviour |
|---|---|
| Search error / timeout / 5xx | retried with backoff; then logged and skipped (`[]`), run continues |
| Search quota guard | `BudgetExceeded` stops that stage cleanly; partial results are reported with `coverage` status |
| 403 / robots / timeout on a vendor page | recorded in `fetch_failures`; vendor stays snippet-only → lower match class/confidence |
| JS-rendered / empty page | treated as a failed fetch, never guessed at |
| LLM error / refusal / truncation | logged; stage falls back to rules; run continues |
| Conflicting sources (marketplace vs vendor site) | both recorded; higher-reliability source wins; vendor cannot be HIGH confidence |
| Duplicates | merged by domain / phone / name similarity ≥ 95 %; every merge logged |
| Unsupported claim | dropped by the gate |
| No vendors in a tier | `coverage` row says `NO_VENDORS_FOUND` — never silently empty |

## Reproducibility

Every search, page fetch and LLM response is cached on disk (`data/cache`, keys = hash of the request). `--replay` re-runs
the entire pipeline offline from the recorded responses and produces the same vendors, scores and ranking. No sampling
parameters are used (current Claude models reject non-default values), so the cache — not temperature — is the source of
determinism.

## Security

* API keys come from environment / `.env` only (git-ignored); the repo contains `.env.example`.
* Fetching search-result URLs is an SSRF surface: http/https only, every hop must resolve to a public IP, ≤3 redirects,
  robots.txt honoured, per-host politeness delay, 600 KB cap, non-HTML skipped.
* Page text is treated as data. The LLM prompts say so, outputs are schema-constrained (`output_config.format`) and every
  quote is re-verified by the gate; names are accepted only if they literally appear in the result text.

## Swappable parts

`SearchProvider` (2 methods) — Serper implemented; Brave/Tavily need one adapter. LLM: `OpenAICompatLLM` covers any
OpenAI-compatible endpoint (Gemini, Groq, OpenRouter, Ollama, OpenAI) with JSON mode **and** tool calling — a provider is one
entry in `config/llm_presets.yaml` (base URL, model ids, env-var *name* of the key). `AnthropicLLM` supports the JSON stages
only (no agent adapter yet); `NullLLM` is rules-only. Caching, budgets, retries and logging live in `SearchService` /
the LLM clients, not in the stages.
