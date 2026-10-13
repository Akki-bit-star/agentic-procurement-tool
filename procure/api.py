"""FastAPI wrapper. Thin by design: it calls the SAME `run_pipeline` the CLI uses.

    uvicorn procure.api:app --reload      (then open http://127.0.0.1:8000)

Endpoints
  GET  /api/defaults            demo input + default config summary
  POST /api/normalize           ambiguity report only (no network)
  POST /api/runs                start a run (background thread) -> {run_id}
  GET  /api/runs/{id}           status + result when finished
  GET  /api/runs/{id}/events    Server-Sent Events: stage / log / discovery / verified
  GET  /api/runs/{id}/export    ?format=json|csv|md  [&tier=AHMEDABAD|INDIA_OTHER|GLOBAL]
"""
from __future__ import annotations

import asyncio
import json
import threading
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from .config import ROOT, llm_preset_names, llm_preset_overrides, load_config
from .models import ProcurementRequest, Tier
from .pipeline import NeedsClarification, normalise_request, run_pipeline
from .providers.search import ProviderError
from .report import to_csv, to_json, to_markdown

app = FastAPI(title="Agentic Procurement Tool", version="0.1")


class RunRequest(BaseModel):
    request: ProcurementRequest
    cache_mode: str = Field("auto", pattern="^(auto|replay|refresh)$")
    llm: str | None = Field(None, description="LLM preset name from config/llm_presets.yaml, e.g. gemini | groq | none")
    agent: bool = False
    strict: bool = False
    overrides: dict[str, Any] = Field(default_factory=dict)


class RunState:
    def __init__(self) -> None:
        self.status = "running"
        self.events: list[dict[str, Any]] = []
        self.result = None
        self.error: dict[str, Any] | None = None
        self.lock = threading.Lock()


RUNS: dict[str, RunState] = {}
MAX_RUNS = 20          # in-memory only; older runs are dropped (CLI outputs on disk are the durable record)


def _worker(run_id: str, body: RunRequest) -> None:
    st = RUNS[run_id]

    def on_event(ev: dict[str, Any]) -> None:
        with st.lock:
            st.events.append(ev)

    try:
        ov = dict(body.overrides)
        if body.llm:
            ov.update(llm_preset_overrides(body.llm))
        if body.agent:
            ov["llm.agent.enabled"] = True
        cfg = load_config(overrides=ov)
        st.result = run_pipeline(body.request, cfg, cache_mode=body.cache_mode, on_event=on_event, strict=body.strict)
        st.status = "done"
    except NeedsClarification as e:
        st.status, st.error = "needs_clarification", {"message": str(e), "flags": e.flags}
    except ProviderError as e:
        st.status, st.error = "error", {"message": f"Search provider not available: {e}"}
    except Exception as e:  # noqa: BLE001 - the UI must always get a terminal state
        st.status, st.error = "error", {"message": f"{type(e).__name__}: {e}"}
    finally:
        with st.lock:
            st.events.append({"type": "end", "status": st.status})


@app.get("/api/defaults")
def defaults() -> dict[str, Any]:
    demo = json.loads((ROOT / "demo" / "input.json").read_text(encoding="utf-8"))
    cfg = load_config()
    return {"demo_input": demo, "weights": cfg.weights, "default_unit": cfg.default_unit, "llm_presets": llm_preset_names(),
            "budgets": {"max_search_calls_total": cfg.search.max_search_calls_total},
            "location": cfg.procurement_location.model_dump()}


@app.get("/api/demo-result")
def demo_result() -> JSONResponse:
    """The committed demo output, so the UI can be explored with no keys and no run."""
    p = ROOT / "demo" / "output" / "result.json"
    if not p.exists():
        raise HTTPException(404, "no committed demo result")
    return JSONResponse(json.loads(p.read_text(encoding="utf-8")))


_DEMO_FILES = {"result.json", "report.md", "vendors_all.csv", "vendors_ahmedabad.csv",
               "vendors_india_outside_ahmedabad.csv", "vendors_global.csv"}


@app.get("/api/demo-file/{name}")
def demo_file(name: str) -> FileResponse:
    if name not in _DEMO_FILES:                     # whitelist: no path traversal
        raise HTTPException(404, "unknown file")
    p = ROOT / "demo" / "output" / name
    if not p.exists():
        raise HTTPException(404, "no committed demo output")
    return FileResponse(p, filename=name)


@app.post("/api/normalize")
def normalize(req: ProcurementRequest) -> list[dict[str, Any]]:
    return [nm.model_dump(mode="json") for nm in normalise_request(req, load_config())]


@app.post("/api/runs")
def start_run(body: RunRequest) -> dict[str, str]:
    if len(RUNS) >= MAX_RUNS:
        for k in list(RUNS)[: len(RUNS) - MAX_RUNS + 1]:
            if RUNS[k].status != "running":
                RUNS.pop(k, None)
    run_id = uuid.uuid4().hex[:12]
    RUNS[run_id] = RunState()
    threading.Thread(target=_worker, args=(run_id, body), daemon=True).start()
    return {"run_id": run_id}


def _get(run_id: str) -> RunState:
    st = RUNS.get(run_id)
    if not st:
        raise HTTPException(404, "unknown run")
    return st


@app.get("/api/runs/{run_id}")
def get_run(run_id: str) -> JSONResponse:
    st = _get(run_id)
    body: dict[str, Any] = {"status": st.status, "error": st.error, "n_events": len(st.events)}
    if st.result is not None:
        body["result"] = json.loads(st.result.model_dump_json())
    return JSONResponse(body)


@app.get("/api/runs/{run_id}/events")
async def events(run_id: str) -> StreamingResponse:
    st = _get(run_id)

    async def gen():
        i = 0
        while True:
            with st.lock:
                batch, i = st.events[i:], len(st.events)
            for ev in batch:
                yield f"data: {json.dumps(ev, default=str)}\n\n"
                if ev.get("type") == "end":
                    return
            await asyncio.sleep(0.4)

    return StreamingResponse(gen(), media_type="text/event-stream", headers={"Cache-Control": "no-cache"})


@app.get("/api/runs/{run_id}/export")
def export(run_id: str, format: str = Query("json", pattern="^(json|csv|md)$"), tier: str | None = None) -> PlainTextResponse:
    st = _get(run_id)
    if st.result is None:
        raise HTTPException(409, "run has not finished")
    if format == "json":
        return PlainTextResponse(to_json(st.result), media_type="application/json",
                                 headers={"Content-Disposition": "attachment; filename=result.json"})
    if format == "md":
        return PlainTextResponse(to_markdown(st.result), media_type="text/markdown",
                                 headers={"Content-Disposition": "attachment; filename=report.md"})
    t = Tier(tier) if tier else None
    return PlainTextResponse(to_csv(st.result, t), media_type="text/csv",
                             headers={"Content-Disposition": f"attachment; filename=vendors_{(tier or 'all').lower()}.csv"})


# ---- serve the built React app when present (npm run build in ./frontend)
_DIST = Path(ROOT) / "frontend" / "dist"
if _DIST.exists():
    app.mount("/assets", StaticFiles(directory=_DIST / "assets"), name="assets")

    @app.get("/{path:path}")
    def spa(path: str) -> FileResponse:   # noqa: ARG001
        return FileResponse(_DIST / "index.html")
