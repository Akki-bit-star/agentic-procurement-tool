# Agentic Procurement Tool

Finds and evaluates vendors for industrial materials (demo: ERW steel pipe, Ahmedabad), separates them into
**Ahmedabad / India-outside-Ahmedabad / global**, and produces an **evidence-based shortlist** where every fact is either
backed by a verbatim quote and URL, or explicitly labelled as derived, assumed, or "needs RFQ".

* **CLI first** (`python -m procure ...`) — the full system, no UI required.
* **Web UI** (React + FastAPI) on top of the same pipeline function.
* **Reproducible**: every search / page / LLM response is cached; `--replay` re-runs the whole pipeline offline and gives the same ranking.
* **Works without an LLM** (rules-only workflow, the committed demo). With any tool-calling LLM (Gemini/Groq free tiers,
  OpenRouter, Ollama, OpenAI) `--agent` turns discovery and verification into model-directed research agents — still behind
  the same evidence gate and deterministic scoring.

| Doc | What it covers |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | agentic harness, workflow stages, failure handling, security |
| [docs/PARAMETERS.md](docs/PARAMETERS.md) | input parameters, match classes, ranking weights, confidence model, assumptions |
| [docs/LIMITATIONS.md](docs/LIMITATIONS.md) | known limitations and what I'd improve |
| [demo/output/report.md](demo/output/report.md) | **the demo result** (3 materials, Ahmedabad) |

## Quick start

Requires **Python 3.10+**. Node is only needed if you want to *rebuild* the UI (a build is committed in `frontend/dist`).

```bash
python -m venv .venv
.venv\Scripts\activate            # Windows   (Linux/macOS: source .venv/bin/activate)
pip install -r requirements.txt
copy .env.example .env            # Windows   (Linux/macOS: cp .env.example .env)
```
Edit `.env`: `SERPER_API_KEY` for live searches, and optionally one LLM key (e.g. `GEMINI_API_KEY`) for agent mode.
**No keys are needed** to explore the committed demo or to replay it offline.

**Web app** (UI + API on one port):
```bash
uvicorn procure.api:app --port 8000      # then open http://127.0.0.1:8000
```
Click **Open committed demo result** to browse the demo without any key, or edit the requirements and **Run procurement search**
(choose an LLM provider and tick *agent mode* in the UI if you configured a key).

**Command line** (the full system, no UI required):
```bash
python -m procure normalize demo/input.json                                    # how requirements are interpreted (offline)
python -m procure run demo/input.json --out runs/replay --replay --llm none    # reproduce the committed demo offline, no keys
python -m procure run demo/input.json --out runs/live                          # live run (needs SERPER_API_KEY; cached, re-runs are free)
```

Outputs per run: `result.json` (source of truth), `report.md`, `vendors_all.csv`, and one CSV per geography
(`vendors_ahmedabad.csv`, `vendors_india_outside_ahmedabad.csv`, `vendors_global.csv`).

### Agent mode (model-directed research) — free providers work

By default the system is a rule-driven workflow (the committed demo). `--agent` replaces discovery + verification with
**one tool-using research agent per material × geography**: the model chooses searches, which pages to read and which
quotes to record, while the evidence gate, geography rules and scoring stay deterministic (see
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#two-execution-modes-same-pipeline-same-evidence-gate-same-scoring)).

```bash
# 1. get a free key, e.g. Gemini: https://aistudio.google.com/apikey   (or Groq: https://console.groq.com/keys)
# 2. put it in .env:  GEMINI_API_KEY=...        (see .env.example for all providers)
python -m procure llm-check --llm gemini                           # 2 tiny calls: JSON mode + tool call; says "ready for --agent"
python -m procure run demo/input_one.json --out runs/agent1 --llm gemini --agent    # one material first (cheap)
python -m procure run demo/input.json     --out runs/agent  --llm gemini --agent    # all three
python -m procure compare demo/output/result.json runs/agent/result.json            # agent vs rules baseline
```

> **Status / honesty note.** The committed demo is the rule-driven workflow (zero LLM calls). Agent mode is covered by tests with a
> scripted model and a mocked HTTP provider, and was exercised live against Gemini's free tier, where individual agent turns worked
> (searches, parallel page reads, verbatim-quote recording) but free models were frequently out of daily quota or overloaded, so a
> complete all-LLM run was not achieved; the client rotates models and the rules backstop covers gaps. Expect results to depend on
> which models your key can use that day.

Providers are presets in `config/llm_presets.yaml` (`gemini`, `groq`, `openrouter`, `ollama`, `openai`; any OpenAI-compatible
endpoint is one more entry). Free tiers rate-limit hard, so calls are paced (`requests_per_minute`), 429s are retried, and a
full agent run takes minutes, not seconds. Model ids and limits change — check the provider's current docs.
Cost control: every model turn and search is cached (re-runs and `--replay` are free); the agent starts from the already-cached
planner queries; per-agent caps are `llm.agent.max_steps / max_searches / max_reads` in `config/default.yaml`.

### CLI reference

| Command | Purpose |
|---|---|
| `procure normalize <input.json>` | parse requirements, print ambiguities and assumptions (offline) |
| `procure run <input.json> --out DIR` | full pipeline. Flags: `--replay` (offline, recorded responses only), `--refresh` (ignore cache, spends quota), `--strict` (stop on critical ambiguity instead of assuming), `--llm <preset>`, `--agent`, `--search-provider`, `--config`, `--cache-dir` |
| `procure report <result.json>` | re-render md/csv from a saved result |
| `procure llm-check --llm <preset>` | verify a provider preset + key (JSON mode and tool calling) before a full run |
| `procure compare A.json B.json` | side-by-side of two runs (e.g. rules-only vs agent) |
| `procure run ... --llm <preset> --agent` | provider preset (`gemini`, `groq`, …) and model-directed research agents |

Exit codes: `0` ok · `2` stopped by `--strict` (lists what to confirm) · `3` setup error (e.g. missing search key).

### Web UI

```bash
uvicorn procure.api:app --port 8000           # API + serves the built UI if frontend/dist exists
cd frontend && npm install && npm run build   # build the UI once (or `npm run dev` with the API on :8000)
```
Open http://127.0.0.1:8000 — edit requirements, start a run, watch stage progress, filter vendors by geography / match / confidence,
inspect each vendor's evidence quotes, and export JSON / CSV / Markdown. The API has no authentication: **local use only**.

## Input

`demo/input.json` — one object per material. The original text is never modified.

```json
{"id": "M-02", "description_raw": "40 mm MS ERW, Class B pipe", "quantity": 500, "unit": null,
 "location_raw": "Ahmedabad, Gujarat, India"}
```

`unit: null` is legal: the tool flags it, assumes **tonnes**, shows the metre and 6 m-length equivalents, and lists the
assumption in the report (or stops in `--strict` mode).

## What the demo found (rules-only run, ~30 recorded search calls)

See the full [report](demo/output/report.md). Highlights:

* **All three inputs are ambiguous, and the tool says so** (and does not silently fix them):
  * quantity unit missing → assumed tonnes (1,000 t of DN 50 ≈ 134 km of pipe; 1,000 m would be only ≈ 7 t — a different supplier type);
  * M-01: **5.5 mm is not an IS 1239 wall for DN 50** (BIS: light 2.9 / medium 3.6 / heavy 4.5 mm) — kept as written, nearest series searched too;
  * M-02: "40 mm" (DN 40 vs OD) and "Class B" (trade shorthand for IS 1239 *medium*; the standard itself says light/medium/heavy);
  * M-03: 89.5 mm is valid but is the *maximum* permitted OD for DN 80 (nominal ≈ 88.9).
* Each geography has real, sourced vendors with verified addresses and contacts; almost all are **NEAR** matches with the reason
  stated (e.g. "required wall 4.8 mm not confirmed"), because very few public pages tie size + wall + standard + ERW together.
  Only one **EXACT** match was found. This is deliberate: EXACT requires size, wall/series, standard *and* ERW process in evidence.
* Vendors whose address could not be established (blocked / JS pages) are listed separately, not forced into a geography.

## Repository layout

```
procure/            pipeline, agents, CLI, API       config/   default.yaml (parameters), IS 1239 table, gazetteer
  normalize.py        stage 1: parse + ambiguity     data/cache/  committed response cache (replay)
  agents/discovery.py stage 3: search loops          demo/     input.json + output/ (committed result)
  agents/verify.py    stage 5: fetch + evidence      docs/     architecture, parameters, limitations
  signals.py          quote -> typed signals         tests/    83 tests (offline)
  state.py            evidence ledger + gate         frontend/ React UI
  resolve.py          dedupe + geography             .env.example
  assess.py           match, score, confidence
  report.py, report_md.py, cli.py, api.py
```

## Tests

```bash
python -m pytest -q       # 83 tests, offline, no keys; includes an end-to-end run with a stub search provider,
                          # the evidence gate, grounding of LLM output, and a replay-reproducibility check of the committed demo
```

## Configuration and secrets

* Non-secret parameters (budgets, weights, thresholds, domain lists) live in `config/default.yaml`.
* Secrets come from environment variables / `.env` only (`SERPER_API_KEY`, `ANTHROPIC_API_KEY`); `.env` is git-ignored and
  `.env.example` is committed. **No keys are in the repository or the cache.**
* Search quota protection: hard cap `search.max_search_calls_total` (60), per-tier query caps, and caching of every response.

## Swapping providers

* **Search** — implement `RawSearchProvider` (`search`, `places`) in `procure/providers/search.py` and register it in `PROVIDERS`; select with
  `search.provider` in config. Caching, budgets, retries and logging are applied by `SearchService`, not the adapter.
* **LLM** — `LLMClient.complete_json`; model ids are in config (`llm.fast_model`, `llm.strong_model`).
