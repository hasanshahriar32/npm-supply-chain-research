import fs from "node:fs/promises";
import path from "node:path";
import { BenchmarkSnapshot, ExperimentResult, IncidentLabel, LiteratureStudy, ResearchDocument } from "./researchTypes";

const researchRoot = path.join(process.cwd(), "research");

const documents: ResearchDocument[] = [
  { slug: "literature-review", title: "Literature Review", category: "literature", sourceFile: "10_literature_review.md", summary: "Related work across ecosystem structure, propagation, package detection, and CI/CD security." },
  { slug: "gap-analysis", title: "Gap Analysis", category: "gap", sourceFile: "68_temporal_reconstruction_and_baseline_results.md", summary: "Cutoff-valid temporal reconstruction, bounded registry-graph sensitivity, explicit-label corpus review, and evidence-based limits on predictive inference." },
  { slug: "benchmark-findings", title: "Benchmark Findings", category: "benchmark", sourceFile: "51_current_snapshot_findings.md", summary: "Reproducible current-snapshot leverage findings with strict limits on predictive interpretation." },
  { slug: "methodology", title: "Methodology", category: "methodology", sourceFile: "50_gap_resolution_study_protocol.md", summary: "Time-aware targets, feature ledger, queue definitions, temporal controls, and evaluation protocol." },
  { slug: "incident-labels", title: "Incident Labels", category: "governance", sourceFile: "69_temporal_incident_label_adjudication.md", summary: "An expanded, family-aware register of independently sourced package-event labels and adjudication limits." },
  { slug: "experiment-results", title: "Experiment Results", category: "benchmark", sourceFile: "68_temporal_reconstruction_and_baseline_results.md", summary: "Measured temporal feasibility, bounded registry-graph sensitivity, and explicit-label corpus review; no predictive model metrics are reported." },
];

function parseCsvRow(line: string) {
  const values: string[] = []; let value = ""; let quoted = false;
  for (let i = 0; i < line.length; i += 1) { const char = line[i]; if (char === '"') quoted = !quoted; else if (char === "," && !quoted) { values.push(value); value = ""; } else value += char; }
  values.push(value);
  return values.map((item) => item.replace(/^"|"$/g, "").trim());
}

export async function getDocuments() { return documents; }

export async function getDocument(slug: string) {
  const document = documents.find((item) => item.slug === slug);
  if (!document) return null;
  const markdown = await fs.readFile(path.join(researchRoot, document.sourceFile), "utf8");
  return { ...document, markdown };
}

export async function getLiterature() {
  const raw = await fs.readFile(path.join(researchRoot, "11_literature_matrix.csv"), "utf8");
  const [header, ...rows] = raw.trim().split(/\r?\n/);
  const columns = parseCsvRow(header);
  return rows.map((line) => { const row = parseCsvRow(line); return Object.fromEntries(columns.map((column, index) => [column, row[index] ?? ""])) as LiteratureStudy; });
}

export async function getChartData() {
  const raw = await fs.readFile(path.join(researchRoot, "benchmark_chart_data.json"), "utf8");
  return JSON.parse(raw) as {
    source: string; generatedAt: string; recordCount: number;
    blastRadiusDistribution: Array<{ bucket: string; packages: number }>;
    topBlastRadius: Array<{ packageName: string; blastRadius: number; transitiveDependents: number }>;
    topAttackerRoi: Array<{ packageName: string; attackerRoi: number; blastRadius: number }>;
  };
}

export async function getSourceSnapshot(): Promise<BenchmarkSnapshot> {
  const raw = await fs.readFile(path.join(researchRoot, "benchmark_snapshot_manifest.json"), "utf8");
  const manifest = JSON.parse(raw) as { packages: number; versions: number; maintainers: number; dependencyEdges: number; repositoryMappings: number; workflowChecks: number; workflowDetections: number; advisoryRecords: number; metricsRecords: number };
  return { packages: manifest.packages, versions: manifest.versions, maintainers: manifest.maintainers, dependencyEdges: manifest.dependencyEdges, repositoryMappings: manifest.repositoryMappings, workflowChecks: manifest.workflowChecks, workflowCoverage: manifest.workflowDetections / manifest.workflowChecks, advisoryRecords: manifest.advisoryRecords, metricsRecords: manifest.metricsRecords };
}

export function getIncidents(): IncidentLabel[] { return [
  { id: "shai-hulud", name: "Shai-Hulud", incidentType: "Widespread npm supply-chain compromise", eventDate: "2025-09-23", scope: "CISA reported more than 500 compromised npm packages in a multi-package campaign.", assessment: "High-impact campaign anchor; preserve package-level evidence and timing before modeling.", evidenceSource: "CISA alert", status: "confirmed" },
  { id: "axios", name: "Axios", incidentType: "Maintainer account compromise", eventDate: "2026-03-31", scope: "axios@1.14.1 and axios@0.30.4 injected plain-crypto-js@4.2.1 during a short publication window.", assessment: "Version-specific incident anchor suited to strict temporal-label construction.", evidenceSource: "CISA alert and Axios post-mortem", status: "confirmed" },
  { id: "nodejs-2021", name: "2021 Node.js package compromises", incidentType: "Credential and maintainer compromise campaign", eventDate: "2021-10-22", scope: "The adjudicated register contains ua-parser-js, coa, and rc package-event records from one correlated campaign family.", assessment: "Treat the three package records as one incident family in temporal splits and uncertainty calculations.", evidenceSource: "CISA and Mandiant", status: "confirmed" },
  { id: "event-stream", name: "event-stream", incidentType: "Targeted package compromise", eventDate: "2018-11-26", scope: "npm documented the removal of event-stream@3.3.6 after incident triage.", assessment: "Included as a high-confidence package-event anchor with a strict pre-event metadata cutoff.", evidenceSource: "npm incident report", status: "confirmed" },
  { id: "eslint-2018", name: "ESLint 2018 publishes", incidentType: "Malicious package publish incident", eventDate: "2018-07-12", scope: "The adjudicated register contains eslint-scope@3.7.2 and eslint-config-eslint@5.0.2.", assessment: "The two package records remain grouped as a single ESLint incident family.", evidenceSource: "ESLint maintainer postmortem", status: "confirmed" },
]; }

export function getExperiments(): ExperimentResult[] { return [
  { id: "baseline", model: "Current-snapshot interpretable audit", featureSet: "Structural leverage, maintainer concentration, repository and workflow observability", evaluation: "Reproducible cross-sectional descriptive analysis", status: "baseline", note: "Completed on 25,228 repository-backed package metrics; this is not a temporal compromise-prediction result." },
  { id: "temporal-feasibility", model: "Pre-event metadata, bounded registry graph, and label-provenance audit", featureSet: "Registry-selected source versions, direct declarations, cutoff-valid SemVer targets, depth-three runtime-dependency sensitivity, explicit release labels", evaluation: "Eight package-event records, seven exact snapshots, 45 bounded sensitivity edges, and a pre-registered no-fit gate", status: "baseline", note: "Completed with 20 exact declarations, 20 isolated range targets, and 45 bounded registry-only sensitivity edges. A labelled 1,790-row release corpus was checked but its current-registry retention is 9 malicious versus 1,093 benign, so no classifier or primary benchmark metric was fitted." },
  { id: "resolution", model: "Version-aware graph comparison", featureSet: "Release-point-resolved package-version dependency edges", evaluation: "Family-grouped temporal ranking and recall after a registered control design", status: "blocked", note: "Blocked pending an archival resolver source and frozen at-risk control frame. The CHRONO-RESOLUTION release is monolithic and its August 2024 snapshot cannot cover the 2026 family; the registry-only graph is sensitivity-only." },
  { id: "hgat", model: "Heterogeneous graph attention model", featureSet: "Package, maintainer, repository, dependency, workflow relations", evaluation: "Matched temporal split against baselines", status: "blocked", note: "Blocked until labels, temporal snapshots, and baselines are reproducible." },
]; }
