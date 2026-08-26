import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "131_country_currency_map_march_2025_candidate_assessment.json");
const sources = {
  sonatype: "https://www.sonatype.com/blog/multiple-crypto-packages-hijacked-turned-into-info-stealers",
  bleepingComputer: "https://www.bleepingcomputer.com/news/security/infostealer-campaign-compromises-10-npm-packages-targets-devs/",
  npmRegistry: "https://registry.npmjs.org/country-currency-map",
};
const affectedVersions = ["2.1.8"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function retainedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const response = await fetch(sources.npmRegistry, {
  headers: { Accept: "application/json", "User-Agent": "supply-chain-research-country-currency-map-candidate-assessment/1.0" },
});
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);

const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (!affectedPublicationTimes["2.1.8"]) throw new Error("Official registry metadata does not retain country-currency-map@2.1.8 publication time.");

const earliestAffectedVersion = { version: "2.1.8", publishedUtc: affectedPublicationTimes["2.1.8"] };
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffectedVersion.publishedUtc) - 1).toISOString();
const selectedPreEventVersion = retainedVersionTimes(registry)
  .filter(([, publishedAt]) => Date.parse(publishedAt) <= Date.parse(strictFeatureCutoffUtc))
  .at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;

const artifact = {
  study: "country-currency-map-march-2025-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "country-currency-map-2025-03-26",
    packageName: "country-currency-map",
    eventFamilyCandidate: "country_currency_map_crypto_package_hijack_2025",
    affectedVersions,
    earliestAffectedVersion,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    distinctFromExistingLedgerFamilies: true,
  },
  corroboration: {
    sonatype: { publishedDate: "2025-03-27", statement: "Primary technical report identifies country-currency-map@2.1.8 as a hijacked malicious release in the crypto-package campaign." },
    bleepingComputer: { publishedDate: "2025-03-27", statement: "Independent report identifies country-currency-map@2.1.8 as the deprecated malicious version and reports 2.1.7 as the maintainer-recommended earlier version." },
    officialRegistry: { boundedMetadataOnly: true, affectedPublicationTimes, affectedVersionObjectRetained: Boolean(registry.versions?.["2.1.8"]), selectedPreEventVersion, selectedPreEventVersionObjectRetained, retainedVersionObjectKeys: Object.keys(registry.versions ?? {}).sort() },
  },
  sourceProvenance: {
    sonatype: { url: sources.sonatype, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null },
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
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
