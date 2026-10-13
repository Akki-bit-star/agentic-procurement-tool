const j = async (r) => {
  if (!r.ok) {
    let msg = r.statusText;
    try { msg = (await r.json()).detail || msg; } catch { /* ignore */ }
    throw new Error(`${r.status}: ${msg}`);
  }
  return r.json();
};

export const getDefaults = () => fetch("/api/defaults").then(j);
export const getDemoResult = () => fetch("/api/demo-result").then(j);
export const normalize = (request) =>
  fetch("/api/normalize", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(request) }).then(j);
export const startRun = (body) =>
  fetch("/api/runs", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) }).then(j);
export const getRun = (id) => fetch(`/api/runs/${id}`).then(j);
export const subscribe = (id, onEvent) => {
  const es = new EventSource(`/api/runs/${id}/events`);
  es.onmessage = (m) => {
    const ev = JSON.parse(m.data);
    onEvent(ev);
    if (ev.type === "end") es.close();
  };
  es.onerror = () => es.close();
  return () => es.close();
};
export const exportUrl = (runId, format, tier) =>
  runId
    ? `/api/runs/${runId}/export?format=${format}${tier ? `&tier=${tier}` : ""}`
    : `/api/demo-file/${format === "json" ? "result.json" : format === "md" ? "report.md" :
        tier === "AHMEDABAD" ? "vendors_ahmedabad.csv" : tier === "INDIA_OTHER" ? "vendors_india_outside_ahmedabad.csv" :
        tier === "GLOBAL" ? "vendors_global.csv" : "vendors_all.csv"}`;
