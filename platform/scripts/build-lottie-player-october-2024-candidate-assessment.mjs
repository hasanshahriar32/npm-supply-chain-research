import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "127_lottie_player_october_2024_candidate_assessment.json");

const sources = {
  lottieFilesIncidentResolution: "https://lottiefiles.com/blog/inside-lottiefiles/resolution-of-security-incident-with-lottiefiles-lottie-player-package",
  sonatypeIncidentReport: "https://www.sonatype.com/blog/lottie-player-compromised-in-supply-chain-attack-all-you-need-to-know",
  snykIncidentReport: "https://snyk.io/blog/lottie-player-npm-package-compromised-crypto-wallet-theft/",
  npmRegistry: "https://registry.npmjs.org/%40lottiefiles%2Flottie-player",
};
const affectedVersions = ["2.0.5", "2.0.6", "2.0.7"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-lottie-player-candidate-assessment/1.0",
    },
  });
  const text = await response.text();
  if (!response.ok) throw new Error(`Source request failed (${response.status}) for ${url}`);
  return text;
}

function retainedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const [sonatypeText, snykText, registryText] = await Promise.all([
  fetchText(sources.sonatypeIncidentReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.snykIncidentReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

for (const version of affectedVersions) {
  if (!sonatypeText.includes(version) || !snykText.includes(version)) {
    throw new Error(`The independently reviewed incident reports do not both retain affected version ${version}.`);
  }
}
if (!sonatypeText.includes("compromised access token") || !snykText.includes("compromised")) {
  throw new Error("The accessible independent reports do not retain the package-compromise context.");
}

const registry = JSON.parse(registryText);
const orderedTimes = retainedVersionTimes(registry);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((publishedAt) => publishedAt === null)) {
  throw new Error("Official registry metadata no longer retains all selected Lottie Player affected-version timestamps.");
}
const earliestAffected = affectedVersions
  .map((version) => ({ version, publishedUtc: affectedPublicationTimes[version] }))
  .sort((left, right) => Date.parse(left.publishedUtc) - Date.parse(right.publishedUtc))[0];
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffected.publishedUtc) - 1).toISOString();
const selectedPreEventVersion = orderedTimes.filter(([, publishedAt]) => Date.parse(publishedAt) <= Date.parse(strictFeatureCutoffUtc)).at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;

const artifact = {
  study: "lottie-player-october-2024-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "lottie-player-2024-10-30",
    packageName: "@lottiefiles/lottie-player",
    eventFamilyCandidate: "lottie_player_npm_account_takeover_2024",
    affectedVersions,
    earliestAffectedVersion: earliestAffected,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    distinctFromExistingLedgerFamilies: true,
  },
  corroboration: {
    lottieFilesIncidentResolution: { publishedDate: "2024-11-02", statement: "The separately reviewed project incident resolution identifies account takeover and unauthorized versions 2.0.5, 2.0.6, and 2.0.7; the current direct script request returned access-denied, so it is cited context rather than a runtime source input." },
    sonatypeIncidentReport: { publishedDate: "2024-10-31", statement: "Independent report identifies the same three versions and package-compromise context." },
    snykIncidentReport: { publishedDate: "2024-10-31", statement: "Independent report identifies the same three malicious versions and compromised publishing-token context." },
    officialRegistry: { boundedMetadataOnly: true, affectedPublicationTimes, retainedAffectedVersionObjects: Object.fromEntries(affectedVersions.map((version) => [version, Boolean(registry.versions?.[version])])), selectedPreEventVersion, selectedPreEventVersionObjectRetained, retainedVersionObjectKeys: Object.keys(registry.versions ?? {}).sort() },
  },
  sourceProvenance: Object.fromEntries([
    ["lottieFilesIncidentResolution", { url: sources.lottieFilesIncidentResolution, retrievalMode: "separately_reviewed_web_text_extraction", directScriptRequestAttempted: false, responseSha256: null }],
    ["sonatypeIncidentReport", { url: sources.sonatypeIncidentReport, responseSha256: sha256(sonatypeText) }],
    ["snykIncidentReport", { url: sources.snykIncidentReport, responseSha256: sha256(snykText) }],
    ["npmRegistry", { url: sources.npmRegistry, responseSha256: sha256(registryText) }],
  ]),
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
console.log(JSON.stringify({ decision: artifact.decision, earliestAffected, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
