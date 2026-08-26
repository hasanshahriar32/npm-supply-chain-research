import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "133_html_to_gutenberg_may_2026_candidate_assessment.json");
const sources = {
  jfrog: "https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/",
  hackerNews: "https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html",
  githubAdvisory: "https://github.com/advisories/GHSA-2gqj-wrf5-35w8",
  npmRegistry: "https://registry.npmjs.org/html-to-gutenberg",
};
const affectedVersions = ["4.2.11", "4.2.14"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function retainedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const response = await fetch(sources.npmRegistry, {
  headers: { Accept: "application/json", "User-Agent": "supply-chain-research-html-to-gutenberg-candidate-assessment/1.0" },
});
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);

const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((publishedAt) => !publishedAt)) {
  throw new Error("Official registry metadata does not retain publication time for every independently corroborated html-to-gutenberg affected version.");
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
  study: "html-to-gutenberg-may-2026-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "html-to-gutenberg-2026-05-25",
    packageName: "html-to-gutenberg",
    eventFamilyCandidate: "html_to_gutenberg_vscode_task_hijack_2026",
    affectedVersions,
    earliestAffectedVersion,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
  },
  corroboration: {
    jfrog: { publishedDate: "2026-06-24", statement: "Technical report identifies hijacked html-to-gutenberg@4.2.11 and places the package uploads during 25 May 2026." },
    hackerNews: { publishedDate: "2026-06-29", statement: "Independent report corroborates the package-level incident, package name, and 25 May 2026 upload date." },
    githubAdvisory: { reviewedDate: "2026-06-24", statement: "Reviewed malware advisory GHSA-2gqj-wrf5-35w8 identifies the finite affected set html-to-gutenberg@4.2.11 and @4.2.14." },
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
    jfrog: { url: sources.jfrog, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
    hackerNews: { url: sources.hackerNews, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
    githubAdvisory: { url: sources.githubAdvisory, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
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
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
