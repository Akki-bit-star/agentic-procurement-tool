import React, { useEffect, useRef, useState } from "react";
import { getDefaults, getDemoResult, getRun, normalize, startRun, subscribe } from "./api.js";
import Results, { Flags } from "./Results.jsx";

const STAGES = ["normalise", "discovery", "resolve", "verification", "geography", "assessment", "report"];

function InputPanel({ rows, setRows, opts, setOpts, onPreview, onRun, onDemo, busy, defaults }) {
  const upd = (i, k, v) => setRows(rows.map((r, j) => (j === i ? { ...r, [k]: v } : r)));
  return (
    <div className="panel">
      <h2>1 · Requirements</h2>
      <p className="muted small" style={{ marginTop: 0 }}>
        Free text is kept exactly as typed. A blank unit is allowed — the tool will flag it and state its assumption
        (default: <b>{defaults?.default_unit || "tonnes"}</b>).
      </p>
      <div className="table-scroll">
        <table>
          <thead><tr><th>ID</th><th>Material (as written)</th><th>Quantity</th><th>Unit</th><th>Procurement location</th><th /></tr></thead>
          <tbody>
            {rows.map((r, i) => (
              <tr key={i}>
                <td><input style={{ width: 64 }} value={r.id} onChange={(e) => upd(i, "id", e.target.value)} /></td>
                <td><input style={{ width: "100%", minWidth: 260 }} value={r.description_raw} onChange={(e) => upd(i, "description_raw", e.target.value)} /></td>
                <td><input style={{ width: 84 }} type="number" value={r.quantity ?? ""} onChange={(e) => upd(i, "quantity", e.target.value === "" ? null : Number(e.target.value))} /></td>
                <td><input style={{ width: 80 }} placeholder="(none)" value={r.unit ?? ""} onChange={(e) => upd(i, "unit", e.target.value || null)} /></td>
                <td><input style={{ width: "100%", minWidth: 200 }} value={r.location_raw} onChange={(e) => upd(i, "location_raw", e.target.value)} /></td>
                <td><button onClick={() => setRows(rows.filter((_, j) => j !== i))} title="remove row">✕</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <div className="row" style={{ marginTop: 10 }}>
        <button onClick={() => setRows([...rows, { id: `M-${String(rows.length + 1).padStart(2, "0")}`, description_raw: "", quantity: null, unit: null, location_raw: "Ahmedabad, Gujarat, India" }])}>+ Add item</button>
        <span className="grow" />
        <label className="small">Cache&nbsp;
          <select value={opts.cache_mode} onChange={(e) => setOpts({ ...opts, cache_mode: e.target.value })}>
            <option value="auto">auto (cache, then network)</option>
            <option value="replay">replay (offline)</option>
            <option value="refresh">refresh (spends quota)</option>
          </select>
        </label>
        <label className="small">LLM&nbsp;
          <select value={opts.llm} onChange={(e) => setOpts({ ...opts, llm: e.target.value })}>
            {(defaults?.llm_presets || ["none", "anthropic"]).map((p) => <option key={p} value={p}>{p === "none" ? "none (rules only)" : p}</option>)}
          </select>
        </label>
        <label className="small" title="Model-directed research agents (needs a tool-calling provider and its API key in .env)">
          <input type="checkbox" checked={opts.agent} onChange={(e) => setOpts({ ...opts, agent: e.target.checked })} /> agent mode
        </label>
        <label className="small"><input type="checkbox" checked={opts.strict} onChange={(e) => setOpts({ ...opts, strict: e.target.checked })} /> strict (stop on critical ambiguity)</label>
      </div>
      <div className="row" style={{ marginTop: 10 }}>
        <button onClick={onPreview} disabled={busy}>Check ambiguities</button>
        <button className="primary" onClick={onRun} disabled={busy}>{busy ? "Running…" : "Run procurement search"}</button>
        <button onClick={onDemo} disabled={busy}>Open committed demo result</button>
      </div>
    </div>
  );
}

function Progress({ run }) {
  if (!run) return null;
  const idx = STAGES.indexOf(run.stage);
  return (
    <div className="panel">
      <h2>2 · Progress {run.status !== "running" && <span className={`badge ${run.status === "done" ? "HIGH" : "CRITICAL"}`}>{run.status}</span>}</h2>
      <div className="stages">
        {STAGES.map((s, i) => <span key={s} className={`stage ${i < idx || run.status === "done" ? "done" : i === idx ? "on" : ""}`}>{s}</span>)}
      </div>
      {run.discovery.length > 0 && <div className="small muted">discovery loops finished: {run.discovery.length} · vendors verified: {run.verified}</div>}
      <div className="log">
        {run.log.slice(-60).map((l, i) => <div key={i} className={l.level}>{l.level !== "info" ? `[${l.level}] ` : ""}{l.message}</div>)}
      </div>
    </div>
  );
}

export default function App() {
  const [defaults, setDefaults] = useState(null);
  const [rows, setRows] = useState([]);
  const [opts, setOpts] = useState({ cache_mode: "auto", llm: "none", agent: false, strict: false });
  const [preview, setPreview] = useState(null);
  const [run, setRun] = useState(null);
  const [result, setResult] = useState(null);
  const [runId, setRunId] = useState(null);
  const [error, setError] = useState(null);
  const [strictFlags, setStrictFlags] = useState(null);
  const unsub = useRef(null);

  useEffect(() => {
    getDefaults().then((d) => { setDefaults(d); setRows(d.demo_input.materials); }).catch((e) => setError(`Cannot reach the API: ${e.message}. Start it with: uvicorn procure.api:app --port 8000`));
    return () => unsub.current && unsub.current();
  }, []);

  const request = () => ({ materials: rows });
  const guard = async (fn) => { setError(null); setStrictFlags(null); try { await fn(); } catch (e) { setError(e.message); } };

  const onPreview = () => guard(async () => setPreview(await normalize(request())));
  const onDemo = () => guard(async () => { setResult(await getDemoResult()); setRunId(null); setRun(null); });

  const onRun = () => guard(async () => {
    setResult(null); setRunId(null);
    const { run_id } = await startRun({ request: request(), cache_mode: opts.cache_mode, llm: opts.llm, agent: opts.agent, strict: opts.strict });
    const st = { status: "running", stage: "normalise", log: [], discovery: [], verified: 0 };
    setRun({ ...st });
    unsub.current && unsub.current();
    unsub.current = subscribe(run_id, async (ev) => {
      if (ev.type === "stage") st.stage = ev.stage;
      else if (ev.type === "log") st.log.push({ level: ev.level, message: ev.message });
      else if (ev.type === "agent_step") st.log.push({ level: "info", message: `agent ${ev.material}/${ev.tier} step ${ev.step}: ${ev.tool}(${Object.values(ev.args).join(", ").slice(0, 90)})` });
      else if (ev.type === "discovery") st.discovery.push(ev);
      else if (ev.type === "verified") st.verified += 1;
      else if (ev.type === "end") {
        const fin = await getRun(run_id);
        st.status = fin.status;
        if (fin.status === "done") { setResult(fin.result); setRunId(run_id); }
        else if (fin.error) {
          setError(fin.error.message);
          // strict mode: show exactly what must be confirmed, grouped by material
          if (fin.error.flags) setStrictFlags(fin.error.flags);
        }
      }
      setRun({ ...st, log: [...st.log], discovery: [...st.discovery] });
    });
  });

  const busy = run?.status === "running";
  return (
    <div className="wrap">
      <h1>Agentic Procurement Tool</h1>
      <p className="sub">Evidence-based vendor shortlist — Ahmedabad, India-wide and global. Every fact is sourced, derived, assumed or marked “needs RFQ”.</p>
      {error && <div className="panel err">{error}</div>}
      {strictFlags && (
        <div className="panel">
          <h2>Strict mode stopped the run — please confirm these first</h2>
          {strictFlags.map((f, i) => <Flags key={i} flags={[{ ...f, code: `${f.material} · ${f.code}` }]} />)}
          <div className="small muted">Edit the requirement above (e.g. add a unit) or untick “strict” to proceed with the logged assumptions.</div>
        </div>
      )}
      <InputPanel {...{ rows, setRows, opts, setOpts, onPreview, onRun, onDemo, busy, defaults }} />
      {preview && !result && (
        <div className="panel">
          <h2>Ambiguities detected before searching</h2>
          {preview.map((nm) => (
            <div key={nm.original.id}><h3>{nm.original.id} — {nm.original.description_raw}</h3><Flags flags={nm.flags} /></div>
          ))}
        </div>
      )}
      <Progress run={run} />
      {result && <Results result={result} runId={runId} />}
    </div>
  );
}
