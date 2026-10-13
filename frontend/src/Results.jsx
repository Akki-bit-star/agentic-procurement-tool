import React, { useMemo, useState } from "react";
import { exportUrl } from "./api.js";

const TIERS = [
  ["AHMEDABAD", "Ahmedabad"],
  ["INDIA_OTHER", "India (outside Ahmedabad)"],
  ["GLOBAL", "Global"],
  ["UNRESOLVED", "Location not established"],
];
const WEIGHT_KEYS = ["technical_match", "bulk_relevance", "geography_delivery", "certification", "source_quality", "contactability"];

const Badge = ({ v, title }) => <span className={`badge ${v}`} title={title}>{v}</span>;

export function Flags({ flags }) {
  return flags.map((f, i) => (
    <div key={i} className={`flag ${f.severity}`}>
      <Badge v={f.severity} /> <b>{f.code}</b> — {f.message}
      {f.candidates?.length > 0 && <div className="small muted">Interpretations considered: {f.candidates.join(" · ")}</div>}
      {f.assumption && <div className="small"><Badge v={f.provenance} /> Assumption used: {f.assumption}</div>}
      {f.action && <div className="small"><b>Please confirm:</b> {f.action}</div>}
    </div>
  ));
}

function Drawer({ vendor, assessment, evidence, weights, onClose }) {
  const ev = evidence;
  const used = assessment.evidence_ids.map((i) => ev[i]).filter(Boolean);
  const locIds = vendor.facts.location?.evidence_ids || [];
  const shown = [...new Map([...used, ...locIds.map((i) => ev[i]).filter(Boolean)].map((e) => [e.id, e])).values()];
  return (
    <>
      <div className="scrim" onClick={onClose} />
      <aside className="drawer">
        <div className="row"><h2 className="grow">{vendor.name}</h2><button onClick={onClose}>Close ✕</button></div>
        <div className="pill-row">
          <Badge v={assessment.match_class} title="how well the evidence fits the requirement" />
          <Badge v={assessment.confidence} title="how well supported the assessment is" />
          <span className="badge">{vendor.vendor_type}</span>
          <Badge v={vendor.geo_status} title={vendor.tier_reason} />
          <span className="badge">score {assessment.score.toFixed(2)}</span>
        </div>
        <h3>Where and how to reach them</h3>
        <div className="kv">
          <div>Location</div><div>{[vendor.city, vendor.state, vendor.country].filter(Boolean).join(", ") || "unknown"}<div className="small muted">{vendor.tier_reason}</div></div>
          <div>Website</div><div>{vendor.contact.website ? <a href={vendor.contact.website} target="_blank" rel="noreferrer">{vendor.contact.website}</a> : "—"}</div>
          <div>Phone / email</div><div>{[...vendor.contact.phones, ...vendor.contact.emails].join(" · ") || "none found in sources"}</div>
          {vendor.contact.address && <><div>Address</div><div>{vendor.contact.address}</div></>}
        </div>
        <h3>Why this match class</h3>
        <ul>{assessment.match_reasons.map((r, i) => <li key={i}>{r}</li>)}</ul>
        <h3>Why this confidence</h3>
        <ul>{assessment.confidence_reasons.map((r, i) => <li key={i}>{r}</li>)}</ul>
        <h3>Score breakdown</h3>
        {WEIGHT_KEYS.map((k) => (
          <div key={k} style={{ margin: "4px 0" }}>
            <div className="row small"><span className="grow">{k.replace("_", " ")} <span className="muted">(weight {Math.round((weights?.[k] || 0) * 100)}%)</span></span><b>{(assessment.score_breakdown[k] ?? 0).toFixed(2)}</b></div>
            <div className="bar"><i style={{ width: `${(assessment.score_breakdown[k] ?? 0) * 100}%` }} /></div>
          </div>
        ))}
        <div className="small muted">{assessment.score_notes.join(" · ")}</div>
        <h3>Facts and their provenance</h3>
        <div className="kv">
          {["standards", "certifications", "capacity", "delivery", "export", "moq", "price", "lead_time"].filter((k) => vendor.facts[k]).map((k) => (
            <React.Fragment key={k}><div>{k.replace("_", " ")}</div><div><Badge v={vendor.facts[k].provenance} /> {vendor.facts[k].value}{vendor.facts[k].evidence_ids.length > 0 && <span className="small muted"> ({vendor.facts[k].evidence_ids.slice(0, 3).join(", ")})</span>}</div></React.Fragment>
          ))}
        </div>
        {assessment.bulk_feasibility && <><h3>Bulk-quantity feasibility <Badge v={assessment.bulk_feasibility.provenance} /></h3><div>{assessment.bulk_feasibility.value}</div></>}
        {vendor.conflicts.length > 0 && <><h3>Conflicting information</h3><ul>{vendor.conflicts.map((c, i) => <li key={i}>{c}</li>)}</ul></>}
        {vendor.merged_from.length > 0 && <><h3>Duplicates merged</h3><ul>{vendor.merged_from.map((c, i) => <li key={i}>{c}</li>)}</ul></>}
        <h3>Evidence (verbatim quotes)</h3>
        {shown.length === 0 && <div className="muted">No evidence admitted by the evidence gate.</div>}
        {shown.map((e) => (
          <div className="quote" key={e.id}>
            <div className="small muted">{e.id} · {e.claim_types.join(" / ")} · {e.source_kind}</div>
            “{e.quote}”<div className="small"><a href={e.url} target="_blank" rel="noreferrer">{e.url}</a></div>
          </div>
        ))}
        <h3>Unresolved</h3>
        <ul>{assessment.unresolved.map((u, i) => <li key={i}>{u}</li>)}</ul>
        <h3>Recommended next step</h3>
        <div>{assessment.next_step}</div>
        {assessment.exclusion_reason && <div className="small muted" style={{ marginTop: 8 }}>Not shortlisted: {assessment.exclusion_reason}</div>}
      </aside>
    </>
  );
}

export default function Results({ result, runId }) {
  const [mid, setMid] = useState(result.materials[0].original.id);
  const [tier, setTier] = useState("AHMEDABAD");
  const [f, setF] = useState({ q: "", match: new Set(["EXACT", "NEAR", "CATEGORY", "UNVERIFIED"]), conf: new Set(["HIGH", "MEDIUM", "LOW"]), shortlistedOnly: true });
  const [sel, setSel] = useState(null);
  const evidence = useMemo(() => Object.fromEntries(result.evidence.map((e) => [e.id, e])), [result]);
  const weights = useMemo(() => result.meta.weights, [result]);
  const nm = result.materials.find((m) => m.original.id === mid);

  const rows = result.vendors
    .filter((v) => v.tier === tier && v.assessments[mid])
    .map((v) => ({ v, a: v.assessments[mid] }))
    .filter(({ v, a }) => f.match.has(a.match_class) && f.conf.has(a.confidence) && (!f.shortlistedOnly || a.shortlisted || tier === "UNRESOLVED")
      && (!f.q || `${v.name} ${v.city || ""} ${v.country || ""} ${v.domain || ""}`.toLowerCase().includes(f.q.toLowerCase())))
    .sort((x, y) => (x.a.rank ?? 999) - (y.a.rank ?? 999));
  const count = (t) => result.vendors.filter((v) => v.tier === t && v.assessments[mid]?.shortlisted).length;
  const toggle = (key, val) => { const s = new Set(f[key]); s.has(val) ? s.delete(val) : s.add(val); setF({ ...f, [key]: s }); };

  return (
    <div className="panel">
      <h2>3 · Results</h2>
      <div className="small muted">
        {result.vendors.length} vendors · {result.evidence.length} evidence items admitted · {result.dropped_claims.length} claims dropped by the evidence gate ·
        search: {result.meta.search_provider} · LLM: {result.meta.llm_mode} · calls used {JSON.stringify(result.meta.budget_used)}
      </div>

      <details open style={{ marginTop: 8 }}>
        <summary><b>Requirement ambiguities and assumptions</b> (read before sending any RFQ)</summary>
        {result.materials.map((m) => (
          <div key={m.original.id}>
            <h3>{m.original.id} — <code>{m.original.description_raw}</code> · {m.original.quantity} {m.original.unit || "(no unit)"}</h3>
            <div className="small muted">
              Resolved: DN{m.resolved.dn ?? "?"}, OD {m.resolved.od_mm ?? "?"} mm <Badge v={m.resolved.basis.od_mm || "ASSUMED"} />, wall {m.resolved.wall_mm ?? "?"} mm <Badge v={m.resolved.basis.wall_mm || "ASSUMED"} />, {m.resolved.standard || "no standard stated"}
              {m.derived.kg_per_m && <> · <Badge v={m.derived.provenance} /> {m.derived.kg_per_m} kg/m → {Math.round(m.quantity_tonnes).toLocaleString()} t ≈ {m.derived.quantity_metres.toLocaleString()} m</>}
            </div>
            <Flags flags={m.flags.filter((x) => x.code !== "STANDARD_SCOPE_NOTE")} />
          </div>
        ))}
        {(() => { const n = result.materials[0].flags.find((x) => x.code === "STANDARD_SCOPE_NOTE"); return n ? <><h3>Applies to all items</h3><Flags flags={[n]} /></> : null; })()}
      </details>

      <h3>Coverage</h3>
      <div className="table-scroll"><table>
        <thead><tr><th>Material</th><th>Geography</th><th>Found</th><th>Shortlisted</th><th>By match class</th><th>Status</th></tr></thead>
        <tbody>{result.coverage.map((c, i) => (
          <tr key={i}><td>{c.material_id}</td><td>{TIERS.find((t) => t[0] === c.tier)[1]}</td><td>{c.found}</td><td>{c.shortlisted}</td>
            <td className="small">{Object.entries(c.by_match_class).map(([k, n]) => `${k} ${n}`).join(", ") || "—"}</td>
            <td><span className={`badge ${c.status === "OK" ? "HIGH" : "MEDIUM"}`}>{c.status}</span></td></tr>))}</tbody>
      </table></div>

      <div className="tabs">{result.materials.map((m) => <button key={m.original.id} className={`tab ${mid === m.original.id ? "on" : ""}`} onClick={() => setMid(m.original.id)}>{m.original.id}</button>)}</div>
      <div className="small muted">{nm.original.description_raw}</div>
      <div className="tabs">{TIERS.map(([k, label]) => <button key={k} className={`tab ${tier === k ? "on" : ""}`} onClick={() => setTier(k)}>{label}{k !== "UNRESOLVED" && ` (${count(k)})`}</button>)}</div>

      <div className="filters small" style={{ margin: "6px 0 10px" }}>
        <input placeholder="Search name / city / domain" value={f.q} onChange={(e) => setF({ ...f, q: e.target.value })} style={{ marginRight: 10 }} />
        {["EXACT", "NEAR", "CATEGORY", "UNVERIFIED"].map((m) => <label key={m}><input type="checkbox" checked={f.match.has(m)} onChange={() => toggle("match", m)} />{m}</label>)}
        <span className="muted">|</span>&nbsp;
        {["HIGH", "MEDIUM", "LOW"].map((m) => <label key={m}><input type="checkbox" checked={f.conf.has(m)} onChange={() => toggle("conf", m)} />{m}</label>)}
        <span className="muted">|</span>&nbsp;
        <label><input type="checkbox" checked={f.shortlistedOnly} onChange={() => setF({ ...f, shortlistedOnly: !f.shortlistedOnly })} />shortlisted only</label>
      </div>
      {tier === "UNRESOLVED" && <div className="small muted" style={{ marginBottom: 6 }}>These leads had no address in any source (page blocked / JS-rendered / outside the verification budget). They are not placed in any geography.</div>}

      <div className="table-scroll"><table>
        <thead><tr><th>#</th><th>Vendor</th><th>Type</th><th>Location</th><th>Match</th><th>Confidence</th><th>Score</th><th>Contact</th></tr></thead>
        <tbody>
          {rows.map(({ v, a }) => (
            <tr key={v.id} className="click" onClick={() => setSel({ v, a })}>
              <td>{a.rank}</td><td><b>{v.name}</b>{!a.shortlisted && <div className="small muted">not shortlisted</div>}</td><td className="small">{v.vendor_type}</td>
              <td className="small">{[v.city, v.country].filter(Boolean).join(", ") || "?"} <Badge v={v.geo_status} /></td>
              <td><Badge v={a.match_class} /></td><td><Badge v={a.confidence} /></td><td>{a.score.toFixed(2)}</td>
              <td className="small">{v.contact.phones[0] || v.contact.emails[0] || "—"}</td>
            </tr>
          ))}
          {rows.length === 0 && <tr><td colSpan={8} className="muted">No vendors match the current filters.</td></tr>}
        </tbody>
      </table></div>

      <h3>Export</h3>
      <div className="row">
        <a href={exportUrl(runId, "json")}><button>JSON</button></a>
        <a href={exportUrl(runId, "md")}><button>Markdown report</button></a>
        <a href={exportUrl(runId, "csv")}><button>CSV (all)</button></a>
        <a href={exportUrl(runId, "csv", "AHMEDABAD")}><button>CSV Ahmedabad</button></a>
        <a href={exportUrl(runId, "csv", "INDIA_OTHER")}><button>CSV India</button></a>
        <a href={exportUrl(runId, "csv", "GLOBAL")}><button>CSV Global</button></a>
      </div>

      <details style={{ marginTop: 12 }}>
        <summary><b>Run details</b> — assumptions, failures, exclusions</summary>
        <h3>Assumptions in force</h3><ul>{result.assumptions.map((a, i) => <li key={i} className="small">{a}</li>)}</ul>
        <h3>Page-fetch failures ({result.fetch_failures.length})</h3>
        <ul>{result.fetch_failures.slice(0, 25).map((x, i) => <li key={i} className="small">{x.url} — {x.error}</li>)}</ul>
        <h3>Claims dropped by the evidence gate ({result.dropped_claims.length})</h3>
        <ul>{result.dropped_claims.slice(0, 15).map((x, i) => <li key={i} className="small">{x.vendor_id}: “{x.quote}” — {x.reason}</li>)}</ul>
        <h3>Search results excluded before becoming vendors ({result.excluded_candidates.length})</h3>
        <ul>{result.excluded_candidates.slice(0, 25).map((x, i) => <li key={i} className="small">{(x.title || x.url).slice(0, 70)} — {x.reason}</li>)}</ul>
      </details>

      {sel && <Drawer vendor={sel.v} assessment={sel.a} evidence={evidence} weights={weights} onClose={() => setSel(null)} />}
    </div>
  );
}
