import Link from "next/link";
import { useMemo, useState } from "react";

type QueueRow = { noteFile: string; assessmentFile: string | null; packageName: string; decision: string; disposition: string; ledgerRecords: number };

export function QueueAudit({ rows }: { rows: QueueRow[] }) {
  const [filter, setFilter] = useState("all");
  const counts = useMemo(() => rows.reduce<Record<string, number>>((acc, row) => { acc[row.disposition] = (acc[row.disposition] ?? 0) + 1; return acc; }, {}), [rows]);
  const visible = filter === "all" ? rows : rows.filter((row) => row.disposition === filter);
  const summary = [{ label: "Admitted / contextual", key: "admitted/contextual" }, { label: "Excluded", key: "excluded" }, { label: "Reviewed", key: "reviewed" }, { label: "Awaiting assessment", key: "awaiting assessment" }];
  const download = (format: "csv" | "json") => {
    const exportedAtUtc = new Date().toISOString(); const repositoryCommit = "36a4a40f3fb04331905c624ddf4a1d981a7bcb11";
    const payload = format === "json" ? JSON.stringify({ exportedAtUtc, repositoryCommit, filter, rowCount: visible.length, rows: visible }, null, 2) : [`# exportedAtUtc=${exportedAtUtc}`, `# repositoryCommit=${repositoryCommit}`, `# filter=${filter}`, `# rowCount=${visible.length}`, "noteFile,assessmentFile,packageName,decision,disposition,ledgerRecords", ...visible.map((row) => [row.noteFile, row.assessmentFile ?? "", row.packageName, row.decision, row.disposition, row.ledgerRecords].map((value) => `"${String(value).replace(/"/g, '""')}"`).join(","))].join("\n");
    const blob = new Blob([payload], { type: format === "json" ? "application/json" : "text/csv" });
    const url = URL.createObjectURL(blob); const anchor = document.createElement("a"); anchor.href = url; anchor.download = `candidate-queue-${filter}.${format}`; anchor.click(); URL.revokeObjectURL(url);
  };
  const downloadReadme = () => {
    const readme = `# Candidate Queue Export\n\nExported at (UTC): ${new Date().toISOString()}\nFilter: ${filter}\nRows: ${visible.length}\nRepository commit: 8d0e348bf9b9a2968ecdfa4fa9b15b2281c605e1\n\n## Fields\n\n- noteFile: retained candidate discovery or screening note filename.\n- assessmentFile: machine-readable governed assessment filename, when present.\n- packageName: package or bounded package scope recorded by the assessment.\n- decision: exact governed decision string.\n- disposition: normalized queue grouping used by the workspace.\n- ledgerRecords: primary temporal-ledger rows created by the assessment.\n\n## Evidence boundaries\n\nThis export is a research-workflow index, not an installation census, reach estimate, blast-radius measurement, safety claim, or predictive model output. A zero ledgerRecords value means that the candidate was not admitted to the primary ledger; it does not establish benignness or absence of an incident. Source files must be interpreted with their cited evidence and protocol amendments.\n`;
    const blob = new Blob([readme], { type: "text/markdown" }); const url = URL.createObjectURL(blob); const anchor = document.createElement("a"); anchor.href = url; anchor.download = `candidate-queue-${filter}-README.md`; anchor.click(); URL.revokeObjectURL(url);
  };
  return <>
    <div className="audit-summary">
      <button className={filter === "all" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("all")}>All <strong>{rows.length}</strong></button>
      <button className={filter === "admitted/contextual" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("admitted/contextual")}>Admitted / contextual <strong>{counts["admitted/contextual"] ?? 0}</strong></button>
      <button className={filter === "excluded" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("excluded")}>Excluded <strong>{counts.excluded ?? 0}</strong></button>
      <button className={filter === "awaiting assessment" ? "audit-filter active" : "audit-filter"} onClick={() => setFilter("awaiting assessment")}>Awaiting <strong>{counts["awaiting assessment"] ?? 0}</strong></button>
    </div>
    <section className="audit-summary-chart">{summary.map((item) => <div className="audit-bar-row" key={item.key}><div><span>{item.label}</span><strong>{counts[item.key] ?? 0}</strong></div><i style={{ width: `${rows.length ? ((counts[item.key] ?? 0) / rows.length) * 100 : 0}%` }} /></div>)}</section><div className="audit-export"><span>Export current filter: <strong>{visible.length}</strong> rows</span><button onClick={() => download("csv")}>CSV</button><button onClick={() => download("json")}>JSON</button><button onClick={downloadReadme}>README</button></div><section className="section-card"><div className="matrix-wrap"><table className="matrix audit-table"><thead><tr><th>Candidate note</th><th>Package / scope</th><th>Assessment artifact</th><th>Disposition</th><th>Primary rows</th></tr></thead><tbody>{visible.map((row) => <tr key={row.noteFile}><td><Link href={`/workspace/evidence/${encodeURIComponent(row.noteFile)}`}><code>{row.noteFile}</code></Link></td><td>{row.packageName}</td><td>{row.assessmentFile ? <Link href={`/workspace/evidence/${encodeURIComponent(row.assessmentFile)}`}><code>{row.assessmentFile}</code></Link> : <span className="muted">Not found</span>}</td><td><span className={row.disposition === "excluded" ? "tag tag-review" : "tag"}>{row.disposition}</span><small className="audit-decision">{row.decision}</small></td><td>{row.ledgerRecords}</td></tr>)}</tbody></table></div></section>
  </>;
}
