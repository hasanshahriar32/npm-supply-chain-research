import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "148_asyncapi_generator_july_2026_candidate_assessment.json");
const sources = {
  aikido: "https://www.aikido.dev/blog/asyncapi-npm-packages-backdoored-via-github-actions",
  microsoft: "https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/",
  npmRegistry: "https://registry.npmjs.org/%40asyncapi%2Fgenerator",
};
const affectedVersions = ["3.3.1"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function retainedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const response = await fetch(sources.npmRegistry, {
  headers: { Accept: "application/json", "User-Agent": "supply-chain-research-asyncapi-generator-candidate-assessment/1.0" },
});
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);

const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((publishedAt) => !publishedAt)) {
  throw new Error("Official registry metadata does not retain publication time for every independently corroborated AsyncAPI generator affected version.");
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
  study: "asyncapi-generator-july-2026-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "asyncapi-generator-2026-07-14",
    packageName: "@asyncapi/generator",
    eventFamilyCandidate: "asyncapi_github_actions_release_pipeline_compromise_2026",
    affectedVersions,
    affectedVersionScopeRule: "single_version_intersection_of_independently_reviewed_sources_only",
    earliestAffectedVersion,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    documentedIncidentContext: "github_actions_release_pipeline_compromise_with_unresolved_attribution",
    distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
  },
  corroboration: {
    aikido: { publishedDate: "2026-07-14", statement: "Independent technical report identifies @asyncapi/generator@3.3.1 as an affected AsyncAPI package and states that first compromised packages were published after malicious commits in the next branch." },
    microsoft: { publishedDate: "2026-07-15", statement: "Independent technical report lists @asyncapi/generator@3.3.1 as affected and supplies a package-specific path and tarball SHA-256." },
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
    aikido: { url: sources.aikido, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
    microsoft: { url: sources.microsoft, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
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
    "The documented unresolved attribution and reported tooling overlap do not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, or a statistical-independence claim.",
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
