import pg from "pg";

const { Pool } = pg;
const connectionString = process.env.POSTGRES_DATABASE_URL;
if (!connectionString) throw new Error("POSTGRES_DATABASE_URL is required");

const pool = new Pool({ connectionString, max: 1, ssl: { rejectUnauthorized: false } });

const content = [
  ["literature-review", "Literature Review", "literature", "10_literature_review.md", "Related work across ecosystem structure, propagation, package detection, and CI/CD security."],
  ["gap-analysis", "Gap Analysis", "gap", "20_novelty_and_gap_analysis.md", "A conditional novelty assessment and research-gap map."],
  ["benchmark-findings", "Benchmark Findings", "benchmark", "90_final_research_report.md", "Current snapshot evidence and the qualified go recommendation."],
  ["methodology", "Methodology", "methodology", "30_proposed_methodology.md", "Study design, temporal controls, feature families, and evaluation protocol."],
  ["incident-labels", "Incident Labels", "governance", "32_labeling_protocol.md", "High-precision incident-labeling protocol and evidence hierarchy."],
  ["experiment-results", "Experiment Results", "benchmark", "92_priority_backlog.md", "Current experiment plan and evidence requirements."],
];

const incidents = [
  ["Shai-Hulud", "Widespread npm supply-chain compromise", "2025-09-23T00:00:00Z", "CISA reported more than 500 compromised npm packages in a multi-package campaign.", "High-impact campaign anchor; preserve package-level evidence and timing before modeling.", "CISA alert", "confirmed"],
  ["Axios", "Maintainer account compromise", "2026-03-31T00:00:00Z", "axios@1.14.1 and axios@0.30.4 injected plain-crypto-js@4.2.1 during a short publication window.", "Version-specific incident anchor suited to strict temporal-label construction.", "CISA alert and Axios post-mortem", "confirmed"],
];

const experiments = [
  ["Interpretable baseline suite", "Popularity, dependency reach, maintainer reach, workflow observability", "Rolling-origin ranking benchmark", "planned", "Must establish incremental value before graph-learning claims."],
  ["Version-aware graph comparison", "Resolved versus package-level dependency edges", "Rank correlation and incident recall", "planned", "Tests the impact of npm-specific dependency resolution."],
  ["Heterogeneous graph attention model", "Package, maintainer, repository, dependency, workflow relations", "Matched temporal split against baselines", "blocked", "Blocked until labels, temporal snapshots, and baselines are reproducible."],
];

try {
  for (const row of content) {
    await pool.query(`INSERT INTO content_records (slug, title, category, source_file, status, summary) VALUES ($1, $2, $3, $4, 'published', $5) ON CONFLICT (slug) DO UPDATE SET title = EXCLUDED.title, category = EXCLUDED.category, source_file = EXCLUDED.source_file, summary = EXCLUDED.summary, updated_at = NOW()`, row);
  }
  await pool.query(`UPDATE benchmark_snapshots SET is_current = false WHERE is_current = true`);
  const snapshot = await pool.query(`SELECT id FROM benchmark_snapshots WHERE snapshot_date = $1 LIMIT 1`, ["2026-08-20T00:00:00Z"]);
  if (!snapshot.rows.length) await pool.query(`INSERT INTO benchmark_snapshots (snapshot_date, packages, versions, maintainers, dependency_edges, repository_mappings, workflow_checks, workflow_detections, advisory_records, metrics_records, is_current) VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,true)`, ["2026-08-20T00:00:00Z", 25228, 22340, 12217, 121885, 21527, 21523, 15300, 153488, 25228]);
  for (const row of incidents) {
    await pool.query(`INSERT INTO incident_labels (name, incident_type, event_date, scope, assessment, evidence_source, status) SELECT $1,$2,$3,$4,$5,$6,$7 WHERE NOT EXISTS (SELECT 1 FROM incident_labels WHERE name = $1)`, row);
  }
  for (const row of experiments) {
    await pool.query(`INSERT INTO experiment_results (model, feature_set, evaluation, status, note) SELECT $1,$2,$3,$4,$5 WHERE NOT EXISTS (SELECT 1 FROM experiment_results WHERE model = $1)`, row);
  }
  console.log("Seeded repository-backed research records.");
} finally {
  await pool.end();
}
