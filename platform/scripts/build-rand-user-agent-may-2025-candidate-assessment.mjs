import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "144_rand_user_agent_may_2025_candidate_assessment.json");
const sources = {
  aikido: "https://www.aikido.dev/blog/catching-a-rat-remote-access-trojian-rand-user-agent-supply-chain-compromise",
  bleepingComputer: "https://www.bleepingcomputer.com/news/security/supply-chain-attack-hits-npm-package-with-45-000-weekly-downloads/",
  npmRegistry: "https://registry.npmjs.org/rand-user-agent",
};
const affectedVersions = ["2.0.83", "2.0.84", "1.0.110"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function retainedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const response = await fetch(sources.npmRegistry, {
  headers: { Accept: "application/json", "User-Agent": "supply-chain-research-rand-user-agent-candidate-assessment/1.0" },
});
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);

const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((publishedAt) => !publishedAt)) {
  throw new Error("Official registry metadata does not retain publication time for every independently corroborated rand-user-agent affected version.");
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
  study: "rand-user-agent-may-2025-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "rand-user-agent-2025-05-05",
    packageName: "rand-user-agent",
    eventFamilyCandidate: "rand_user_agent_unauthorized_npm_publications_2025",
    affectedVersions,
    affectedVersionScopeRule: "strict_three_version_intersection_of_independently_reviewed_sources_only",
    earliestAffectedVersion,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    documentedIncidentContext: "unauthorized_npm_publications_after_last_legitimate_project_release",
    distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
  },
  corroboration: {
    aikido: { publishedDate: "2025-05-06", statement: "Independent technical analysis identifies rand-user-agent versions 2.0.83, 2.0.84, and 1.0.110 as malicious-version indicators in a supply-chain compromise." },
    bleepingComputer: { publishedDate: "2025-05-08", statement: "Independent report identifies rand-user-agent versions 2.0.83, 2.0.84, and 1.0.110 as malicious unauthorized releases and records direct developer confirmation of the three versions." },
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
    bleepingComputer: { url: sources.bleepingComputer, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
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
    "The documented unauthorized-publication context does not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, or a statistical-independence claim.",
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
