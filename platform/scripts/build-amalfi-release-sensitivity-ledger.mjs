import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const corpusPath = path.join(researchDir, "76_amalfi_basic_corpus.csv");
const commit = JSON.parse(await readFile(path.join(researchDir, "76_amalfi_artifact_commit.json"), "utf8"));
const corpusText = await readFile(corpusPath, "utf8");

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/);
  const columns = header.split(",").map(value => value.replaceAll('"', ""));
  return lines.filter(Boolean).map(line => Object.fromEntries(columns.map((column, index) => [column, line.split(",")[index] ?? ""])));
}

function escapeCsv(value) {
  const text = value == null ? "" : String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

async function getRegistry(packageName, cache) {
  if (cache.has(packageName)) return cache.get(packageName);
  const response = await fetch(`https://registry.npmjs.org/${encodeURIComponent(packageName)}`, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-amalfi-ledger/1.0" } });
  const body = await response.text();
  const entry = response.ok
    ? { status: "available", metadata: JSON.parse(body), sha256: createHash("sha256").update(body).digest("hex") }
    : { status: "unavailable", error: `registry response ${response.status}`, sha256: "" };
  cache.set(packageName, entry);
  return entry;
}

const sourceRows = parseCsv(corpusText).filter(row => row.analysis === "malicious" || row.analysis === "benign");
const registryCache = new Map();
const output = [];
for (const row of sourceRows) {
  const registry = await getRegistry(row.package, registryCache);
  const published = registry.metadata?.time?.[row.version];
  const manifestPresent = Boolean(registry.metadata?.versions?.[row.version]);
  const publishedMs = Date.parse(published ?? "");
  const artifactMs = Date.parse(commit.committed_at);
  const status = registry.status !== "available" ? "registry_unavailable" : !manifestPresent ? "version_not_retained" : !Number.isFinite(publishedMs) ? "missing_or_invalid_publication_time" : "registry_reconstructed";
  output.push({
    package_name: row.package,
    package_version: row.version,
    corpus_content_hash: row.hash,
    corpus_analysis_label: row.analysis,
    corpus_artifact_commit_sha: commit.sha,
    corpus_artifact_committed_utc: commit.committed_at,
    registry_snapshot_status: status,
    registry_version_published_utc: Number.isFinite(publishedMs) ? new Date(publishedMs).toISOString() : "",
    published_before_artifact_commit: Number.isFinite(publishedMs) ? publishedMs <= artifactMs : false,
    registry_response_sha256: registry.sha256,
    label_scope: "retrospective_release_classification_sensitivity_only",
    primary_temporal_benchmark_eligibility: "excluded",
    interpretation_limit: "The corpus supplies an explicit author-assigned release label, not a future-outcome control. It is not an at-risk population for the incident-family compromise benchmark and must not be merged with that primary label ledger.",
  });
}

const header = Object.keys(output[0] ?? { package_name: "" });
await writeFile(path.join(researchDir, "77_amalfi_release_sensitivity_ledger.csv"), [header.join(","), ...output.map(row => header.map(key => escapeCsv(row[key])).join(","))].join("\n") + "\n");
const known = output.filter(row => row.registry_snapshot_status === "registry_reconstructed");
const diagnostics = {
  study: "amalfi-explicit-label-release-sensitivity-provenance",
  corpus: {
    source: "https://github.com/githubnext/amalfi-artifact/blob/main/data/basic-corpus.csv",
    sha256: createHash("sha256").update(corpusText).digest("hex"),
    artifactCommit: commit,
    explicitLabelRows: sourceRows.length,
    maliciousRows: sourceRows.filter(row => row.analysis === "malicious").length,
    benignRows: sourceRows.filter(row => row.analysis === "benign").length,
    distinctPackages: new Set(sourceRows.map(row => row.package)).size,
  },
  registryProvenance: {
    retainedExactVersionObjects: known.length,
    unavailableOrMissingVersions: output.length - known.length,
    retainedVersionsPublishedByArtifactCommit: known.filter(row => row.published_before_artifact_commit).length,
    distinctRegistryResponses: registryCache.size,
  },
  primaryBenchmarkGate: {
    status: "blocked",
    reason: "The corpus has explicit retrospective release labels but lacks per-row review/outcome horizon timestamps and does not define an at-risk population for the independently adjudicated future-compromise target.",
  },
  allowedUse: "Descriptive provenance and separately labelled retrospective release-classification sensitivity only; no future-compromise ranking, calibration, blast-radius, or attack-return inference.",
};
await writeFile(path.join(researchDir, "77_amalfi_release_sensitivity_diagnostics.json"), JSON.stringify(diagnostics, null, 2) + "\n");
console.log(JSON.stringify(diagnostics, null, 2));
