import { mkdir, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "129_nx_august_2025_candidate_assessment.json");

const sources = {
  nxPostmortem: "https://nx.dev/blog/s1ngularity-postmortem",
  githubSecurityAdvisory: "https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c",
  snykIncidentReport: "https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/",
  stepSecurityIncidentReport: "https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware",
  npmRegistry: "https://registry.npmjs.org/nx",
};
const affectedVersions = ["21.5.0", "20.9.0", "20.10.0", "21.6.0", "20.11.0", "21.7.0", "21.8.0", "20.12.0"];

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: { Accept: accept, "User-Agent": "supply-chain-research-nx-candidate-assessment/1.0" },
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

const [snykText, stepSecurityText, registryText] = await Promise.all([
  fetchText(sources.snykIncidentReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.stepSecurityIncidentReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

for (const version of affectedVersions) {
  if (!snykText.includes(version) || !stepSecurityText.includes(version)) {
    throw new Error(`The independent Nx incident reports do not both retain affected version ${version}.`);
  }
}
if (!snykText.includes("compromised npm token") || !stepSecurityText.includes("token")) {
  throw new Error("The accessible independent Nx reports do not retain the publishing-token compromise context.");
}

const registry = JSON.parse(registryText);
const orderedTimes = retainedVersionTimes(registry);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((publishedAt) => publishedAt === null)) {
  throw new Error("Official registry metadata no longer retains all selected Nx affected-version timestamps.");
}
const earliestAffected = affectedVersions
  .map((version) => ({ version, publishedUtc: affectedPublicationTimes[version] }))
  .sort((left, right) => Date.parse(left.publishedUtc) - Date.parse(right.publishedUtc))[0];
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffected.publishedUtc) - 1).toISOString();
const selectedPreEventVersion = orderedTimes.filter(([, publishedAt]) => Date.parse(publishedAt) <= Date.parse(strictFeatureCutoffUtc)).at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;

const artifact = {
  study: "nx-august-2025-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: {
    recordId: "nx-2025-08-26",
    packageName: "nx",
    eventFamilyCandidate: "nx_s1ngularity_publish_token_compromise_2025",
    affectedVersions,
    earliestAffectedVersion: earliestAffected,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    distinctFromExistingLedgerFamilies: true,
  },
  corroboration: {
    nxPostmortem: { publishedDate: "2025-09-05", statement: "Primary project postmortem identifies the stolen npm publishing token and same finite eight-version nx release set." },
    githubSecurityAdvisory: { advisoryId: "GHSA-cxm3-wv7p-598c", statement: "Reviewed advisory lists the same finite nx release set and publication timeline." },
    snykIncidentReport: { publishedDate: "2025-08-27", statement: "Independent report lists the same eight nx versions and compromised npm-token context." },
    stepSecurityIncidentReport: { publishedDate: "2025-08-27", statement: "Independent report lists the same eight nx versions and token-compromise context." },
    officialRegistry: { boundedMetadataOnly: true, affectedPublicationTimes, retainedAffectedVersionObjects: Object.fromEntries(affectedVersions.map((version) => [version, Boolean(registry.versions?.[version])])), selectedPreEventVersion, selectedPreEventVersionObjectRetained, retainedVersionObjectKeys: Object.keys(registry.versions ?? {}).sort() },
  },
  sourceProvenance: Object.fromEntries([
    ["nxPostmortem", { url: sources.nxPostmortem, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null }],
    ["githubSecurityAdvisory", { url: sources.githubSecurityAdvisory, separatelyReviewedWebText: true, directScriptRequestAttempted: false, responseSha256: null }],
    ["snykIncidentReport", { url: sources.snykIncidentReport, responseSha256: sha256(snykText) }],
    ["stepSecurityIncidentReport", { url: sources.stepSecurityIncidentReport, responseSha256: sha256(stepSecurityText) }],
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
