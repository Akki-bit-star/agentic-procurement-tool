"""Command line interface - the primary way to run the system.

    python -m procure normalize demo/input.json            # ambiguity report only, no network
    python -m procure run demo/input.json --out runs/demo  # full search (uses cache, then network)
    python -m procure run demo/input.json --replay         # offline re-run from recorded responses
    python -m procure report runs/demo/result.json         # re-render md/csv from a saved result
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .config import ROOT, llm_preset_names, llm_preset_overrides, load_config
from .models import ProcurementRequest
from .pipeline import NeedsClarification, RunResult, normalise_request, run_pipeline
from .providers.search import ProviderError
from .report import write_outputs


def _load_request(path: str) -> ProcurementRequest:
    return ProcurementRequest(**json.loads(Path(path).read_text(encoding="utf-8")))


def cmd_normalize(args) -> int:
    cfg = load_config(args.config)
    nms = normalise_request(_load_request(args.input), cfg)
    for nm in nms:
        r = nm.resolved
        print(f"\n=== {nm.original.id}: {nm.original.description_raw!r} qty={nm.original.quantity} unit={nm.original.unit}")
        print(f"    resolved: DN{r.dn} OD={r.od_mm} wall={r.wall_mm} std={r.standard} series={r.class_meaning}  "
              f"basis={ {k: v.value for k, v in r.basis.items()} }")
        d = nm.derived
        print(f"    derived : {d.kg_per_m} kg/m ({d.kg_per_m_basis}); {d.quantity_tonnes} t = {d.quantity_metres} m")
        print(f"    queries : {nm.search_interpretations}")
        for f in nm.flags:
            print(f"    [{f.severity.value:8}] {f.code}: {f.message}")
            if f.assumption:
                print(f"               assumption: {f.assumption}")
    return 0


def cmd_run(args) -> int:
    overrides = {}
    if args.llm:
        overrides.update(llm_preset_overrides(args.llm))
    if args.agent:
        overrides["llm.agent.enabled"] = True
    if args.search_provider:
        overrides["search.provider"] = args.search_provider
    cfg = load_config(args.config, overrides)
    mode = "replay" if args.replay else "refresh" if args.refresh else "auto"
    cache_dir = args.cache_dir or ROOT / "data" / "cache"

    def progress(ev):
        if ev.get("type") == "stage":
            print(f"-- stage: {ev['stage']}", flush=True)
        elif ev.get("type") == "log" and ev["level"] in ("warn", "error"):
            print(f"   [{ev['level']}] {ev['message']}", flush=True)

    try:
        res = run_pipeline(_load_request(args.input), cfg, cache_dir=cache_dir, cache_mode=mode,
                           on_event=progress, strict=args.strict)
    except NeedsClarification as e:
        print("\nStopped (--strict): please confirm these before running:\n")
        for f in e.flags:
            print(f"  [{f['material']}] {f['code']}: {f['message']}\n      -> {f.get('action')}")
        return 2
    except ProviderError as e:
        print(f"\nSetup error: {e}", file=sys.stderr)
        return 3
    paths = write_outputs(res, args.out)
    print(f"\nDone. {len(res.vendors)} vendors, {len(res.evidence)} admitted evidence items, "
          f"{len(res.dropped_claims)} claims dropped by the evidence gate.")
    print(f"Calls used: {res.meta['budget_used']} · cache hits {res.meta['cache_hits']}")
    for c in res.coverage:
        print(f"   {c['material_id']} {c['tier']:12} found={c['found']:3} shortlisted={c['shortlisted']:2} {c['status']}")
    print("Outputs:", ", ".join(str(p) for p in paths.values()))
    return 0


def cmd_report(args) -> int:
    res = RunResult(**json.loads(Path(args.result).read_text(encoding="utf-8")))
    paths = write_outputs(res, args.out or Path(args.result).parent)
    print("Wrote:", ", ".join(str(p) for p in paths.values()))
    return 0


def cmd_llm_check(args) -> int:
    """Two tiny calls (JSON mode + a tool call) to prove a provider preset, model ids and key work BEFORE a full run."""
    import tempfile

    from .cache import Cache
    from .context import RunContext
    from .llm import build_llm

    cfg = load_config(args.config, llm_preset_overrides(args.llm))
    ctx = RunContext(cfg)
    llm = build_llm(ctx, Cache(tempfile.mkdtemp(), "auto"))
    print(f"provider={cfg.llm.provider} base_url={cfg.llm.base_url} fast={cfg.llm.fast_model} strong={cfg.llm.strong_model} "
          f"key_env={cfg.llm.api_key_env} available={llm.available}")
    if not llm.available:
        for lg in ctx.logs:
            print("  ", lg.message)
        return 3
    ok = True
    try:
        out = llm.complete_json(tier="fast", system="Reply with JSON only.", user='Return {"ok": true}.',
                                schema={"type": "object", "properties": {"ok": {"type": "boolean"}}}, max_tokens=300, label="check")
        print("JSON mode :", "OK" if out.get("ok") is True else f"unexpected {out}")
    except Exception as e:  # noqa: BLE001
        ok = False
        print("JSON mode : FAILED -", str(e)[:300])
    if hasattr(llm, "chat"):
        try:
            tools = [{"type": "function", "function": {"name": "finish", "description": "End.",
                                                       "parameters": {"type": "object", "properties": {"summary": {"type": "string"}},
                                                                      "required": ["summary"]}}}]
            res = llm.chat(tier="strong", messages=[{"role": "system", "content": "Call the finish tool."},
                                                    {"role": "user", "content": "Finish now with summary 'ok'."}],
                           tools=tools, max_tokens=300, label="check")
            names = [t.name for t in res.tool_calls]
            print("tool call :", "OK -> " + ", ".join(names) if "finish" in names else f"model did not call the tool ({res.content!r})")
            ok = ok and "finish" in names
        except Exception as e:  # noqa: BLE001
            ok = False
            print("tool call : FAILED -", str(e)[:300])
    else:
        print("tool call : n/a (this provider has no agent adapter; JSON-mode stages only)")
    print("RESULT:", "ready for --agent" if ok else "NOT ready (see above)")
    return 0 if ok else 3


def cmd_compare(args) -> int:
    """Side-by-side of two result.json files (e.g. rules-only baseline vs an LLM run)."""
    from collections import Counter
    runs = [json.loads(Path(p).read_text(encoding="utf-8")) for p in (args.a, args.b)]

    def shortlisted(r):
        return {(mid, v["tier"], v["name"]) for v in r["vendors"] for mid, a in v["assessments"].items() if a["shortlisted"]}

    for label, p, r in (("A", args.a, runs[0]), ("B", args.b, runs[1])):
        sh = [a for v in r["vendors"] for a in v["assessments"].values() if a["shortlisted"]]
        print(f"{label}: {p}\n   llm={r['meta']['llm_mode']} vendors={len(r['vendors'])} evidence={len(r['evidence'])} "
              f"dropped_by_gate={len(r['dropped_claims'])} calls={r['meta']['budget_used']}\n"
              f"   shortlisted match classes={dict(Counter(a['match_class'] for a in sh))} confidence={dict(Counter(a['confidence'] for a in sh))}")
        print("   vendors per tier:", dict(Counter(v['tier'] for v in r['vendors'])))
    sa, sb = shortlisted(runs[0]), shortlisted(runs[1])
    print(f"\nshortlist overlap: {len(sa & sb)} common, {len(sa - sb)} only in A, {len(sb - sa)} only in B")
    for tag, s in (("only in A", sa - sb), ("only in B", sb - sa)):
        for mid, tier, name in sorted(s)[:15]:
            print(f"   {tag}: {mid} {tier:11} {name[:60]}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="procure", description="Agentic procurement tool")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("normalize", help="parse requirements and print ambiguities (no network)")
    p.add_argument("input")
    p.add_argument("--config")
    p.set_defaults(fn=cmd_normalize)

    p = sub.add_parser("run", help="run the full pipeline")
    p.add_argument("input")
    p.add_argument("--out", default=str(ROOT / "runs" / "latest"))
    p.add_argument("--config")
    p.add_argument("--replay", action="store_true", help="offline: use only recorded responses")
    p.add_argument("--refresh", action="store_true", help="ignore the cache and re-query (spends quota)")
    p.add_argument("--strict", action="store_true", help="stop on critical ambiguities instead of assuming")
    p.add_argument("--llm", choices=llm_preset_names(),
                   help="LLM provider preset from config/llm_presets.yaml (gemini, groq, openrouter, ollama, openai, anthropic, none)")
    p.add_argument("--agent", action="store_true",
                   help="model-directed research agents (needs a tool-calling provider, e.g. --llm gemini --agent)")
    p.add_argument("--search-provider", choices=["serper", "fixture"])
    p.add_argument("--cache-dir")
    p.set_defaults(fn=cmd_run)

    p = sub.add_parser("report", help="re-render reports from result.json")
    p.add_argument("result")
    p.add_argument("--out")
    p.set_defaults(fn=cmd_report)

    p = sub.add_parser("llm-check", help="verify an LLM provider preset + key with two tiny calls")
    p.add_argument("--llm", required=True, choices=llm_preset_names())
    p.add_argument("--config")
    p.set_defaults(fn=cmd_llm_check)

    p = sub.add_parser("compare", help="compare two result.json files (e.g. rules-only vs LLM)")
    p.add_argument("a")
    p.add_argument("b")
    p.set_defaults(fn=cmd_compare)

    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
