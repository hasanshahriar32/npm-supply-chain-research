import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const cutoff = "2026-03-31T00:00:00.000Z";
const horizonDays = 30;
const cutoffMs = Date.parse(cutoff);
const horizonEndMs = cutoffMs + horizonDays * 24 * 60 * 60 * 1000;

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/);
  const columns = header.split(",");
  return lines.map(line => Object.fromEntries(line.split(",").map((value, index) => [columns[index], value])));
}

function csvEscape(value) {
  const stringValue = value == null ? "" : String(value);
  return /[",\n]/.test(stringValue) ? `"${stringValue.replaceAll('"', '""')}"` : stringValue;
}

function isoOrBlank(value) {
  const milliseconds = Date.parse(value ?? "");
  return Number.isNaN(milliseconds) ? "" : new Date(milliseconds).toISOString();
}

function labelTiming(label) {
  const eventMs = Date.parse(label.event_start_utc);
  if (Number.isNaN(eventMs)) return "missing_event_time";
  if (eventMs <= cutoffMs) return "boundary_or_pre_cutoff";
  if (eventMs <= horizonEndMs) return "strict_future_horizon";
  return "outside_horizon";
}

async function fetchRegistryMetadata(packageName) {
  const response = await fetch(`https://registry.npmjs.org/${encodeURIComponent(packageName)}`, {
    headers: { Accept: "application/json", "User-Agent": "supply-chain-research-temporal-pilot/1.0" },
  });
  const body = await response.text();
  if (!response.ok) throw new Error(`Registry request for ${packageName} failed (${response.status}).`);
  return { json: JSON.parse(body), sha256: createHash("sha256").update(body).digest("hex"), status: response.status };
}

const labels = parseCsv(await readFile(path.join(researchDir, "52_seed_incident_registry.csv"), "utf8"));
const exactLabels = labels.filter(label => label.package_name && label.affected_version);
const packageNames = [...new Set(exactLabels.map(label => label.package_name))].sort();
const rows = [];
const labelAudit = [];
const provenance = [];

for (const packageName of packageNames) {
  const source = await fetchRegistryMetadata(packageName);
  const packageLabels = exactLabels.filter(label => label.package_name === packageName);
  provenance.push({ packageName, registryStatus: source.status, responseSha256: source.sha256, retrievedAt: new Date().toISOString() });

  for (const label of packageLabels) {
    const version = source.json.versions?.[label.affected_version];
    const publishedAt = source.json.time?.[label.affected_version] ?? "";
    const publishedMs = Date.parse(publishedAt);
    labelAudit.push({
      record_id: label.record_id,
      package_name: packageName,
      affected_version: label.affected_version,
      label_class: label.label_class,
      event_start_utc: label.event_start_utc,
      version_present_in_registry: Boolean(version),
      published_at: isoOrBlank(publishedAt),
      pre_cutoff_eligible: Number.isFinite(publishedMs) && publishedMs <= cutoffMs,
      timing_class: labelTiming(label),
      primary_target_eligible: label.primary_target_eligible,
    });
  }

  for (const [versionName, version] of Object.entries(source.json.versions ?? {})) {
    const publishedAt = source.json.time?.[versionName];
    const publishedMs = Date.parse(publishedAt);
    if (!Number.isFinite(publishedMs) || publishedMs > cutoffMs) continue;
    const matchingLabels = packageLabels.filter(label => label.affected_version === versionName);
    const directDependencies = version.dependencies ?? {};
    const scripts = version.scripts ?? {};
    rows.push({
      package_name: packageName,
      version: versionName,
      published_at: new Date(publishedMs).toISOString(),
      direct_dependency_count: Object.keys(directDependencies).length,
      has_direct_dependencies: Object.keys(directDependencies).length > 0,
      dependency_specification: JSON.stringify(directDependencies),
      has_install_script: Boolean(version.hasInstallScript ?? scripts.preinstall ?? scripts.install ?? scripts.postinstall),
      integrity_present: Boolean(version.dist?.integrity),
      historical_fidelity: "registry_reconstructed_exact",
      label_record_ids: matchingLabels.map(label => label.record_id).join("|"),
      label_classes: matchingLabels.map(label => label.label_class).join("|"),
      temporal_label_status: matchingLabels.length ? labelTiming(matchingLabels[0]) : "no_known_event_in_registry",
    });
  }
}

rows.sort((a, b) => a.package_name.localeCompare(b.package_name) || a.published_at.localeCompare(b.published_at));
const header = Object.keys(rows[0] ?? { package_name: "" });
const csv = [header.join(","), ...rows.map(row => header.map(column => csvEscape(row[column])).join(","))].join("\n") + "\n";
const strictFuturePositives = labelAudit.filter(row => row.pre_cutoff_eligible && row.timing_class === "strict_future_horizon").length;
const summary = {
  study: "exact-direct-metadata-temporal-pilot",
  cutoff,
  horizonDays,
  packages: packageNames,
  eligibleVersionObservations: rows.length,
  labelAudit,
  strictFuturePositiveCount: strictFuturePositives,
  feasibilityDecision: strictFuturePositives >= 10 && new Set(labelAudit.filter(row => row.timing_class === "strict_future_horizon").map(row => row.label_class)).size >= 2
    ? "eligible_for_pre_registered_baseline_design"
    : "not_eligible_for_predictive_or_calibration_inference",
  reason: "The pre-registered registry seed labels are at the cutoff boundary or lack sufficient independent incidents; report provenance and feasibility only.",
  provenance,
};

const adjudicationHeader = [
  "record_id",
  "package_name",
  "affected_version",
  "label_class",
  "event_start_utc",
  "published_at",
  "version_present_in_registry",
  "pre_cutoff_eligible",
  "timing_class",
  "primary_target_eligible",
  "adjudicated_primary_status",
  "exclusion_or_boundary_reason",
];
const adjudicationRows = labelAudit.map(row => ({
  ...row,
  adjudicated_primary_status: row.pre_cutoff_eligible && row.timing_class === "strict_future_horizon" && row.primary_target_eligible === "yes"
    ? "primary_positive"
    : "not_primary_positive",
  exclusion_or_boundary_reason: !row.version_present_in_registry
    ? "registry_version_object_unavailable"
    : !row.pre_cutoff_eligible
      ? "version_published_after_cutoff"
      : row.timing_class !== "strict_future_horizon"
        ? "event_not_strictly_after_cutoff_within_horizon"
        : "none",
}));
const adjudicationCsv = [
  adjudicationHeader.join(","),
  ...adjudicationRows.map(row => adjudicationHeader.map(column => csvEscape(row[column])).join(",")),
].join("\n") + "\n";

await mkdir(researchDir, { recursive: true });
await writeFile(path.join(researchDir, "62_temporal_pilot_metadata_ledger.csv"), csv);
await writeFile(path.join(researchDir, "62_temporal_pilot_summary.json"), JSON.stringify(summary, null, 2) + "\n");
await writeFile(path.join(researchDir, "63_temporal_label_adjudication_ledger.csv"), adjudicationCsv);
console.log(JSON.stringify({ eligibleVersionObservations: rows.length, strictFuturePositives, feasibilityDecision: summary.feasibilityDecision }, null, 2));
