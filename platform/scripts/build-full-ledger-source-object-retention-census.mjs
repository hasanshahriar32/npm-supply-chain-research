import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const snapshotsPath = path.join(researchDir, "65_package_temporal_companion_snapshots.csv");
const diagnosticsPath = path.join(researchDir, "65_package_temporal_companion_diagnostics.json");
const outputPath = path.join(researchDir, "98_full_ledger_source_object_retention_census.json");

const parseCsv = (text) => {
  const [header, ...rows] = text.trim().split("\n");
  const headers = header.split(",");
  return rows.map((row) => Object.fromEntries(row.split(",").map((value, index) => [headers[index], value])));
};

const [snapshotsText, diagnosticsText] = await Promise.all([
  readFile(snapshotsPath, "utf8"),
  readFile(diagnosticsPath, "utf8"),
]);
const snapshots = parseCsv(snapshotsText);
const diagnostics = JSON.parse(diagnosticsText);

if (snapshots.length !== diagnostics.observations) {
  throw new Error("The source-object retention census requires one snapshot-status row for every strict companion observation.");
}
const diagnosticByPackage = new Map(diagnostics.provenance.map((entry) => [entry.packageName, entry]));

const records = snapshots.map((row) => {
  const provenance = diagnosticByPackage.get(row.package_name);
  if (!provenance || provenance.responseSha256 !== row.registry_response_sha256) {
    throw new Error(`Missing or mismatched registry provenance for ${row.record_id}.`);
  }

  let retentionState;
  let selectionEligibility;
  let exceptionReason = null;
  if (row.snapshot_status === "registry_reconstructed_exact") {
    retentionState = "current_registry_response_retains_selected_pre_event_version_object";
    selectionEligibility = "eligible_for_strict_pre_event_source_object";
  } else if (row.pre_event_latest_version) {
    retentionState = "current_registry_time_map_has_pre_cutoff_version_but_selected_version_object_fails_strict_retention";
    selectionEligibility = "label_only_no_strict_source_object";
    exceptionReason = "A timestamped pre-cutoff version selection exists in the companion output, but the selected version object fails the strict object-retention requirement.";
  } else {
    retentionState = "current_registry_response_has_no_retained_pre_cutoff_version_selection";
    selectionEligibility = "label_only_no_strict_source_object";
    exceptionReason = "The companion output cannot select a version object published at or before the strict cutoff from the current registry response.";
  }

  return {
    recordId: row.record_id,
    packageName: row.package_name,
    eventFamily: row.event_family,
    eventStartUtc: row.event_start_utc,
    featureCutoffUtc: row.feature_cutoff_utc,
    snapshotStatus: row.snapshot_status,
    selectionEligibility,
    retentionState,
    selectedPreEventVersionIdentifier: row.pre_event_latest_version || null,
    selectedPreEventPublishedUtc: row.pre_event_latest_published_utc || null,
    currentRegistryResponseSha256: provenance.responseSha256,
    currentRegistryResponseRetrievedAtUtc: provenance.retrievedAt,
    exceptionReason,
  };
});

const exact = records.filter((record) => record.selectionEligibility === "eligible_for_strict_pre_event_source_object");
const labelOnly = records.filter((record) => record.selectionEligibility === "label_only_no_strict_source_object");
const output = {
  study: "full-ledger-source-object-retention-census",
  artifactVersion: 1,
  executionStatus: "current_registry_retention_census_only_no_package_feature_or_outcome_analysis",
  generatedAtUtc: new Date().toISOString(),
  sourceInputs: {
    snapshots: {
      path: "research/65_package_temporal_companion_snapshots.csv",
      sha256: createHash("sha256").update(snapshotsText).digest("hex"),
    },
    diagnostics: {
      path: "research/65_package_temporal_companion_diagnostics.json",
      sha256: createHash("sha256").update(diagnosticsText).digest("hex"),
      observations: diagnostics.observations,
      incidentFamilyCount: diagnostics.incidentFamilyCount,
    },
  },
  censusDefinition: {
    unit: "One pre-registered package-event record in the strict temporal incident ledger.",
    scope: "Current npm registry-response retention for selecting a pre-event source version object before each recorded event cutoff.",
    notHistoricalEvidence: "Present access to a registry response describes current retention and reconstruction eligibility only; it is not evidence of what package metadata, maintainer authority, repository state, provenance, workflow, or dependency resolution looked like at release time beyond an exact retained selected version object.",
    noPayloadPolicy: "No package tarball, package installation, lockfile resolution, repository content, workflow content, or external attestation bundle is retrieved.",
  },
  summary: {
    incidentRecords: records.length,
    incidentFamilies: new Set(records.map((record) => record.eventFamily)).size,
    currentRegistryResponsesWithProvenance: records.length,
    strictPreEventSourceObjectsRetained: exact.length,
    labelOnlyExceptions: labelOnly.length,
    currentRetentionIsNotHistoricalEvidence: true,
  },
  records,
  exceptionCategories: {
    timeMapSelectionButStrictObjectRetentionFailure: labelOnly.filter((record) => record.retentionState === "current_registry_time_map_has_pre_cutoff_version_but_selected_version_object_fails_strict_retention").map((record) => record.recordId),
    noPreCutoffVersionSelectionInCurrentResponse: labelOnly.filter((record) => record.retentionState === "current_registry_response_has_no_retained_pre_cutoff_version_selection").map((record) => record.recordId),
  },
  currentDecision: {
    packageMetadataValuesExtracted: 0,
    maintainerOrPublisherValuesExtracted: 0,
    repositoryOrWorkflowValuesExtracted: 0,
    provenanceOrAttestationStatesClassified: 0,
    packageFeaturesDerived: 0,
    controlsCreated: 0,
    scoresComputed: 0,
    modelsFitted: 0,
    rankingsComputed: 0,
    predictiveMetricsComputed: 0,
  },
  prohibitedInterpretations: [
    "Do not treat a current registry retention state as a historical package, maintainer, repository, provenance, workflow, or dependency-state observation.",
    "Do not treat a label-only exception, missing selected object, or unavailable current response as safe, benign, unchanged, or no-known-event.",
    "Do not derive package features, compare metadata values, classify authority deltas, create controls, or fit or evaluate a model from this census.",
    "Do not interpret records within one campaign family as independent observations merely because their source-object retention differs.",
  ],
};

await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ outputPath, ...output.summary, exceptions: output.exceptionCategories, noFeatures: output.currentDecision.packageFeaturesDerived, controls: output.currentDecision.controlsCreated, models: output.currentDecision.modelsFitted }, null, 2));
