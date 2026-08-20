import fs from "node:fs/promises";
import path from "node:path";
import { BenchmarkSnapshot, ExperimentResult, IncidentLabel, LiteratureStudy, ResearchDocument } from "./researchTypes";

const researchRoot = path.join(process.cwd(), "research");

const documents: ResearchDocument[] = [
  { slug: "literature-review", title: "Literature Review", category: "literature", sourceFile: "10_literature_review.md", summary: "Related work across ecosystem structure, propagation, package detection, and CI/CD security." },
  { slug: "gap-analysis", title: "Gap Analysis", category: "gap", sourceFile: "20_novelty_and_gap_analysis.md", summary: "A conditional novelty assessment and research-gap map." },
  { slug: "benchmark-findings", title: "Benchmark Findings", category: "benchmark", sourceFile: "90_final_research_report.md", summary: "Current snapshot evidence and the qualified go recommendation." },
  { slug: "methodology", title: "Methodology", category: "methodology", sourceFile: "30_proposed_methodology.md", summary: "Study design, temporal controls, feature families, and evaluation protocol." },
  { slug: "incident-labels", title: "Incident Labels", category: "governance", sourceFile: "32_labeling_protocol.md", summary: "High-precision incident-labeling protocol and evidence hierarchy." },
  { slug: "experiment-results", title: "Experiment Results", category: "benchmark", sourceFile: "92_priority_backlog.md", summary: "The current experiment plan and evidence requirements." },
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
]; }

export function getExperiments(): ExperimentResult[] { return [
  { id: "baseline", model: "Interpretable baseline suite", featureSet: "Popularity, dependency reach, maintainer reach, workflow observability", evaluation: "Rolling-origin ranking benchmark", status: "planned", note: "Must establish incremental value before graph-learning claims." },
  { id: "resolution", model: "Version-aware graph comparison", featureSet: "Resolved versus package-level dependency edges", evaluation: "Rank correlation and incident recall", status: "planned", note: "Tests the impact of npm-specific dependency resolution." },
  { id: "hgat", model: "Heterogeneous graph attention model", featureSet: "Package, maintainer, repository, dependency, workflow relations", evaluation: "Matched temporal split against baselines", status: "blocked", note: "Blocked until labels, temporal snapshots, and baselines are reproducible." },
]; }
