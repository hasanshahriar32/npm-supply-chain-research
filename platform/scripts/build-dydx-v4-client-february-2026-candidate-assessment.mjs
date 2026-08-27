import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "150_dydx_v4_client_february_2026_candidate_assessment.json");
const sources = {
  socket: "https://socket.dev/blog/malicious-dydx-packages-published-to-npm-and-pypi",
  theHackerNews: "https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html",
  npmRegistry: "https://registry.npmjs.org/%40dydxprotocol%2Fv4-client-js",
};
const affectedVersions = ["3.4.1", "1.22.1", "1.15.2", "1.0.31"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function retainedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const response = await fetch(sources.npmRegistry, {
  headers: { Accept: "application/json", "User-Agent": "supply-chain-research-dydx-v4-client-candidate-assessment/1.0" },
});
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);

const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((publishedAt) => !publishedAt)) {
  throw new Error("Official registry metadata does not retain a publication time for every independently corroborated dYdX npm affected version.");
}

const earliestAffectedVersion = Object.entries(affectedPublicationTimes)
  .map(([version, publishedUtc]) => ({ version, publishedUtc }))
  .sort((left, right) => Date.parse(left.publishedUtc) - Date.parse(right.publishedUtc))[0];
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffectedVersion.publishedUtc) - 1).toISOString();
const selectedPreEventVersion = retainedVersionTimes(registry)
  .filter(([, publishedAt]) => Date.parse(publishedAt) <= Date.parse(strictFeatureCutoffUtc))
  .at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;

const artifact = {
  study: "dydx-v4-client-february-2026-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "dydx-v4-client-2026-02-06",
    packageName: "@dydxprotocol/v4-client-js",
    eventFamilyCandidate: "dydx_v4_client_npm_pypi_maintainer_compromise_2026",
    affectedVersions,
    affectedVersionScopeRule: "strict_four_version_intersection_of_independently_reviewed_sources_only",
    earliestAffectedVersion,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    documentedIncidentContext: "npm_and_pypi_package_event_with_unconfirmed_maintainer_compromise_attribution",
    distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
  },
  corroboration: {
    socket: { publishedDate: "2026-02-06", statement: "Independent technical report identifies @dydxprotocol/v4-client-js versions 3.4.1, 1.22.1, 1.15.2, and 1.0.31 as compromised npm releases." },
    theHackerNews: { publishedDate: "2026-02-06", statement: "Independent reporting lists @dydxprotocol/v4-client-js versions 3.4.1, 1.22.1, 1.15.2, and 1.0.31 as compromised npm releases." },
    officialRegistry: {
      boundedMetadataOnly: true,
      affectedPublicationTimes,
      affectedVersionObjectsRetained: Object.fromEntries(affectedVersions.map((version) => [version, Boolean(registry.versions?.[version])])),
      selectedPreEventVersion,
      selectedPreEventVersionObjectRetained,
      retainedVersionObjectKeys: Object.keys(registry.versions ?? {}).sort(),
    },
  },
  sourceProvenance: {
    socket: { url: sources.socket, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
    theHackerNews: { url: sources.theHackerNews, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
    npmRegistry: { url: sources.npmRegistry, responseSha256: sha256(registryText) },
  },
  strictEligibility: {
    finiteExactAffectedVersionsIndependentlyCorroborated: true,
    officialAffectedVersionTimestampsRetained: true,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    eligibleForGovernedReconstruction: selectedPreEventVersionObjectRetained,
  },
  currentDecision: {
    primaryLedgerRecordsAdded: 0,
    primaryLedgerFamiliesAdded: 0,
    futureValidationUnitsAdded: 0,
    exactPreEventSourceSnapshotsCreated: 0,
    dependencyDeclarationsCreated: 0,
    isolatedSemverApproximationsCreated: 0,
    recursiveGraphEdgesCreated: 0,
    controlsCreated: 0,
    benignLabelsCreated: 0,
    historicalInstallTracesCreated: 0,
    reachOrBlastRadiusValuesCreated: 0,
    scoresComputed: 0,
    modelsFitted: 0,
    rankingsComputed: 0,
    uncertaintyIntervalsComputed: 0,
    calibrationResultsCreated: 0,
    predictiveMetricsComputed: 0,
  },
  nextDecisionBoundary: selectedPreEventVersionObjectRetained
    ? "Any admission must atomically update the strict ledger and every dependent artifact; it must still create zero controls, installations, reach measures, scores, models, rankings, intervals, calibration results, and predictive metrics."
    : "The candidate cannot enter the strict ledger without a retained selected pre-event source object.",
  prohibitedInterpretations: [
    "Registry metadata establishes publication-time selection and retained-object availability only; it does not establish historical installations, downstream reach, blast radius, current maintainer state, or a causal effect.",
    "The unconfirmed maintainer-compromise attribution and cross-ecosystem context do not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, or a statistical-independence claim.",
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
