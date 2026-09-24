import Link from "next/link";
import { useMemo, useState } from "react";

type QueueRow = { noteFile: string; assessmentFile: string | null; packageName: string; decision: string; disposition: string; ledgerRecords: number };

export function QueueAudit({ rows }: { rows: QueueRow[] }) {
  const [filter, setFilter] = useState("all");
  const counts = useMemo(() => rows.reduce<Record<string, number>>((acc, row) => { acc[row.disposition] = (acc[row.disposition] ?? 0) + 1; return acc; }, {}), [rows]);
  const visible = filter === "all" ? rows : rows.filter((row) => row.disposition === filter);
  const summary = [{ label: "Admitted / contextual", key: "admitted/contextual" }, { label: "Excluded", key: "excluded" }, { label: "Reviewed", key: "reviewed" }, { label: "Awaiting assessment", key: "awaiting assessment" }];
  return <>
    <div className="audit-summary">
      <button className={filter === "all" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("all")}>All <strong>{rows.length}</strong></button>
      <button className={filter === "admitted/contextual" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("admitted/contextual")}>Admitted / contextual <strong>{counts["admitted/contextual"] ?? 0}</strong></button>
      <button className={filter === "excluded" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("excluded")}>Excluded <strong>{counts.excluded ?? 0}</strong></button>
      <button className={filter === "awaiting assessment" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("awaiting assessment")}>Awaiting <strong>{counts["awaiting assessment"] ?? 0}</strong></button>
    </div>
    <section className="audit-summary-chart">{summary.map((item) => <div className="audit-bar-row" key={item.key}><div><span>{item.label}</span><strong>{counts[item.key] ?? 0}</strong></div><i style={{ width: `${rows.length ? ((counts[item.key] ?? 0) / rows.length) * 100 : 0}%` }} /></div>)}</section><section className="section-card"><div className="matrix-wrap"><table className="matrix audit-table"><thead><tr><th>Candidate note</th><th>Package / scope</th><th>Assessment artifact</th><th>Disposition</th><th>Primary rows</th></tr></thead><tbody>{visible.map((row) => <tr key={row.noteFile}><td><Link href={`/workspace/evidence/${encodeURIComponent(row.noteFile)}`}><code>{row.noteFile}</code></Link></td><td>{row.packageName}</td><td>{row.assessmentFile ? <Link href={`/workspace/evidence/${encodeURIComponent(row.assessmentFile)}`}><code>{row.assessmentFile}</code></Link> : <span className="muted">Not found</span>}</td><td><span className={row.disposition === "excluded" ? "tag tag-review" : "tag"}>{row.disposition}</span><small className="audit-decision">{row.decision}</small></td><td>{row.ledgerRecords}</td></tr>)}</tbody></table></div></section>
  </>;
}
