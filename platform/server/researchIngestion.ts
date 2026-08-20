import AdmZip from "adm-zip";
import { claimIngestionRun, createPendingSnapshot, getIngestionRun, recordIngestionRun } from "./platformDb";

const repository = "ashik-hstu/npm-supply-chain-research";
const archivePath = "data/metrics_summary.csv.zip";
const manifestPath = "research/benchmark_snapshot_manifest.json";

function parseCsvLine(line: string) {
  const values: string[] = []; let value = ""; let quoted = false;
  for (const char of line) { if (char === '"') quoted = !quoted; else if (char === "," && !quoted) { values.push(value); value = ""; } else value += char; }
  values.push(value); return values.map((item) => item.replace(/^"|"$/g, "").trim());
}

type MetricRecord = { package_name: string; blast_radius: string; transitive_dependents: string; attacker_roi: string };
type SnapshotManifest = { packages: number; versions: number; maintainers: number; dependencyEdges: number; repositoryMappings: number; workflowChecks: number; workflowDetections: number; advisoryRecords: number; metricsRecords: number };

function buildChartData(records: MetricRecord[]) {
  const buckets = [{ bucket: "0", min: 0, max: 0 }, { bucket: "1", min: 1, max: 1 }, { bucket: "2", min: 2, max: 2 }, { bucket: "3–5", min: 3, max: 5 }, { bucket: "6+", min: 6, max: Infinity }];
  return {
    recordCount: records.length,
    blastRadiusDistribution: buckets.map((bucket) => ({ bucket: bucket.bucket, packages: records.filter((record) => { const value = Number(record.blast_radius); return value >= bucket.min && value <= bucket.max; }).length })),
    topBlastRadius: [...records].sort((a, b) => Number(b.blast_radius) - Number(a.blast_radius) || Number(b.transitive_dependents) - Number(a.transitive_dependents)).slice(0, 10).map((record) => ({ packageName: record.package_name, blastRadius: Number(record.blast_radius), transitiveDependents: Number(record.transitive_dependents) })),
    topAttackerRoi: [...records].sort((a, b) => Number(b.attacker_roi) - Number(a.attacker_roi)).slice(0, 10).map((record) => ({ packageName: record.package_name, attackerRoi: Number(Number(record.attacker_roi).toFixed(3)), blastRadius: Number(record.blast_radius) })),
  };
}

async function fetchGitHubFile(token: string, filePath: string) {
  const response = await fetch(`https://api.github.com/repos/${repository}/contents/${filePath}`, { headers: { Accept: "application/vnd.github+json", Authorization: `Bearer ${token}`, "X-GitHub-Api-Version": "2022-11-28" } });
  if (!response.ok) throw new Error(`GitHub metadata request for ${filePath} failed with ${response.status}`);
  return response.json() as Promise<{ sha: string; download_url?: string }>;
}

async function fetchRaw(token: string, item: { download_url?: string }, filePath: string) {
  const response = await fetch(item.download_url ?? `https://api.github.com/repos/${repository}/contents/${filePath}`, { headers: { Accept: "application/vnd.github.raw", Authorization: `Bearer ${token}`, "X-GitHub-Api-Version": "2022-11-28" } });
  if (!response.ok) throw new Error(`GitHub content request for ${filePath} failed with ${response.status}`);
  return response;
}

export async function ingestMetricsArchive() {
  const token = process.env.GITHUB_TOKEN;
  if (!token) throw new Error("GITHUB_TOKEN is required for daily ingestion");
  const [archiveMeta, manifestMeta] = await Promise.all([fetchGitHubFile(token, archivePath), fetchGitHubFile(token, manifestPath)]);
  const sourceRef = `${archiveMeta.sha}:${manifestMeta.sha}`;
  const existing = await getIngestionRun(sourceRef);
  if (existing?.status === "completed") return { status: "skipped" as const, sourceRef, snapshotId: existing.snapshotId };
  const claim = await claimIngestionRun(sourceRef);
  if (!claim) return { status: "skipped" as const, sourceRef, snapshotId: existing?.snapshotId ?? null };
  try {
    const [archiveResponse, manifestResponse] = await Promise.all([fetchRaw(token, archiveMeta, archivePath), fetchRaw(token, manifestMeta, manifestPath)]);
    const manifest = await manifestResponse.json() as SnapshotManifest;
    const archive = new AdmZip(Buffer.from(await archiveResponse.arrayBuffer()));
    const entry = archive.getEntry("metrics_summary.csv");
    if (!entry) throw new Error("metrics_summary.csv was not found in the downloaded archive");
    const [header, ...lines] = entry.getData().toString("utf8").trim().split(/\r?\n/);
    const columns = parseCsvLine(header);
    const records = lines.map((line) => Object.fromEntries(columns.map((column, index) => [column, parseCsvLine(line)[index] ?? ""]))) as MetricRecord[];
    if (records.length !== manifest.metricsRecords || manifest.packages !== manifest.metricsRecords) throw new Error("Snapshot manifest and metrics archive record counts do not agree");
    const chartData = buildChartData(records);
    const snapshot = await createPendingSnapshot({ snapshotDate: new Date(), packages: manifest.packages, versions: manifest.versions, maintainers: manifest.maintainers, dependencyEdges: manifest.dependencyEdges, repositoryMappings: manifest.repositoryMappings, workflowChecks: manifest.workflowChecks, workflowDetections: manifest.workflowDetections, advisoryRecords: manifest.advisoryRecords, metricsRecords: manifest.metricsRecords, sourceRef, chartData });
    await recordIngestionRun({ sourceRef, status: "completed", detail: `Staged ${records.length.toLocaleString()} metrics records and paired snapshot manifest`, snapshotId: snapshot?.id ?? null });
    return { status: "staged" as const, sourceRef, snapshotId: snapshot?.id ?? null, recordCount: records.length };
  } catch (error) {
    await recordIngestionRun({ sourceRef, status: "failed", detail: error instanceof Error ? error.message : "Unknown ingestion failure" });
    throw error;
  }
}
