import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "152_dydx_solo_september_2022_candidate_assessment.json");
const sources = {
  bleepingComputer: "https://www.bleepingcomputer.com/news/security/npm-packages-used-by-crypto-exchanges-compromised/",
  githubAdvisory: "https://github.com/advisories/GHSA-xjr5-5w2w-3233",
  mend: "https://www.mend.io/blog/popular-cryptocurrency-exchange-dydx-has-had-its-npm-account-hacked/",
  npmRegistry: "https://registry.npmjs.org/%40dydxprotocol%2Fsolo",
};
const affectedVersions = ["0.41.1", "0.41.2"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function retainedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const response = await fetch(sources.npmRegistry, {
  headers: { Accept: "application/json", "User-Agent": "supply-chain-research-dydx-solo-candidate-assessment/1.0" },
});
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);

const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((publishedAt) => !publishedAt)) {
  throw new Error("Official registry metadata does not retain a publication time for every independently corroborated dYdX Solo affected version.");
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
  study: "dydx-solo-september-2022-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "dydx-solo-2022-09-23",
    packageName: "@dydxprotocol/solo",
    eventFamilyCandidate: "dydx_solo_september_2022_npm_account_compromise",
    affectedVersions,
    affectedVersionScopeRule: "strict_two_version_intersection_of_independently_reviewed_sources_only",
    earliestAffectedVersion,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    documentedIncidentContext: "dydx_owned_npm_package_event_with_mend_reported_account_compromise",
    distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
  },
  corroboration: {
    bleepingComputer: { publishedDate: "2022-09-23", statement: "Independent reporting identifies @dydxprotocol/solo versions 0.41.1 and 0.41.2 in the September 2022 npm compromise." },
    githubAdvisory: { publishedDate: "2022-09-23", statement: "GitHub’s reviewed malware advisory identifies @dydxprotocol/solo affected versions >= 0.41.1 and <= 0.41.2, intersecting as versions 0.41.1 and 0.41.2." },
    mend: { publishedDate: "2022-09-23", statement: "Independent report supplies package-level dYdX npm account-compromise context but is not used as version-specific corroboration in this screen." },
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
    bleepingComputer: { url: sources.bleepingComputer, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
    githubAdvisory: { url: sources.githubAdvisory, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
    mend: { url: sources.mend, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
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
    "The documented dYdX package context and temporal difference from the governed 2026 dYdX record do not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, actor linkage, or a statistical-independence claim.",
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
