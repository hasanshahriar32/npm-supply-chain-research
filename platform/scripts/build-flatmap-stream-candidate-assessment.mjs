import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "104_flatmap_stream_candidate_assessment.json");

const sources = {
  npmIncidentNotice: "https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident",
  independentSnykPostmortem: "https://snyk.io/blog/a-post-mortem-of-the-malicious-event-stream-backdoor/",
  independentMicrosoftNotice: "https://devblogs.microsoft.com/devops/blocking-malicious-versions-of-event-stream-and-flatmap-stream-packages/",
  npmRegistry: "https://registry.npmjs.org/flatmap-stream",
};

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-flatmap-stream-candidate-assessment/1.0",
    },
  });
  const text = await response.text();
  if (!response.ok) throw new Error(`Source request failed (${response.status}) for ${url}`);
  return text;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

const [npmNoticeText, snykText, microsoftText, registryText] = await Promise.all([
  fetchText(sources.npmIncidentNotice, "text/html, text/plain;q=0.9"),
  fetchText(sources.independentSnykPostmortem, "text/html, text/plain;q=0.9"),
  fetchText(sources.independentMicrosoftNotice, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

const registry = JSON.parse(registryText);
const retainedVersionObjectKeys = Object.keys(registry.versions ?? {}).sort();
const timeMap = registry.time ?? {};
const affectedVersionTimeUtc = timeMap["0.1.1"] ?? null;
const knownBlockedVersions = ["0.1.0", "0.1.1", "0.1.2"];
const blockedVersionObjectRetention = Object.fromEntries(knownBlockedVersions.map((version) => [version, Boolean(registry.versions?.[version])]));
const blockedVersionTimeRetention = Object.fromEntries(knownBlockedVersions.map((version) => [version, timeMap[version] ?? null]));

assert(npmNoticeText.includes("malicious package was version 0.1.1") && npmNoticeText.includes("event-stream") && npmNoticeText.includes("September 9, 2018"), "The npm notice does not retain the expected flatmap-stream incident context.");
assert(snykText.includes("flatmap-stream@0.1.1") && snykText.includes("October 5, 2018"), "The independent Snyk post-mortem does not retain the expected injected release timeline.");
assert(microsoftText.includes("flatmap-stream") && microsoftText.includes("0.1.0, 0.1.1, and 0.1.2") && microsoftText.includes("event-stream"), "The independent Microsoft notice does not retain the expected blocked-version context.");
assert(affectedVersionTimeUtc === null, "The candidate must not use this exclusion if the official registry retains flatmap-stream@0.1.1 timing.");
assert(knownBlockedVersions.every((version) => !registry.versions?.[version]), "The candidate must not use this exclusion if the registry retains a historically relevant blocked version object.");

const artifact = {
  study: "flatmap-stream-2018-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "exclude_from_primary_temporal_ledger_due_to_no_official_affected_release_timestamp_or_retained_pre_event_source_object",
  candidate: {
    recordId: "flatmap-stream-2018-10-05",
    packageName: "flatmap-stream",
    independentlyReportedAffectedVersion: "0.1.1",
    independentlyReportedInjectionDate: "2018-10-05",
    relatedExistingFamily: "event_stream_2018",
    relatednessRule: "If future evidence ever makes this candidate ledger-eligible, it must remain a second package-event record within the existing event_stream_2018 family and must not create a new independent campaign family or validation unit.",
    officialAffectedVersionTimeUtc: affectedVersionTimeUtc,
    strictFeatureCutoffUtc: null,
  },
  corroboration: {
    npmIncidentNotice: {
      statement: "npm identifies flatmap-stream@0.1.1 as the malicious package and reports that it was added as a direct dependency of event-stream@3.3.6 on September 9, 2018.",
    },
    independentSnykPostmortem: {
      statement: "Snyk identifies flatmap-stream@0.1.1 as the injected release and records an October 5, 2018 release timeline.",
    },
    independentMicrosoftNotice: {
      statement: "Microsoft identifies flatmap-stream as malicious and records blocks for 0.1.0, 0.1.1, and 0.1.2 alongside event-stream@3.3.6.",
    },
    officialRegistry: {
      boundedMetadataOnly: true,
      affectedVersionTimeUtc,
      blockedVersionTimeRetention,
      blockedVersionObjectRetention,
      retainedVersionObjectKeys,
      laterRetainedTimeMapEntry: timeMap["11.1.1"] ?? null,
    },
  },
  sourceProvenance: {
    npmIncidentNotice: { url: sources.npmIncidentNotice, responseSha256: sha256(npmNoticeText) },
    independentSnykPostmortem: { url: sources.independentSnykPostmortem, responseSha256: sha256(snykText) },
    independentMicrosoftNotice: { url: sources.independentMicrosoftNotice, responseSha256: sha256(microsoftText) },
    npmRegistry: { url: sources.npmRegistry, responseSha256: sha256(registryText) },
  },
  strictExclusionReason: {
    requiredRule: "A primary temporal-ledger record requires an official registry timestamp for an independently corroborated affected release and a retained official-registry source object selected strictly before the resulting cutoff.",
    observedState: "The bounded current registry response lacks a 0.1.1 time-map entry, lacks all 0.1.x time-map entries, and retains no historically relevant 0.1.x version object. A later security-holder object does not supply event-time or pre-event source evidence. Therefore no official exact cutoff or pre-event source-object selection can be reconstructed.",
    consequence: "Do not add flatmap-stream to the 14-record primary ledger, do not create a companion source snapshot, direct declarations, range approximations, recursive graph edges, a new campaign family, or a new validation unit from this candidate.",
  },
  currentDecision: {
    primaryLedgerRecordsAdded: 0,
    primaryLedgerFamiliesAdded: 0,
    primaryLedgerValidationUnitsAdded: 0,
    exactPreEventSourceSnapshotsCreated: 0,
    packageMetadataValuesExtracted: 0,
    dependencyDeclarationsCreated: 0,
    resolvedTargetsCreated: 0,
    recursiveGraphEdgesCreated: 0,
    controlsCreated: 0,
    benignLabelsCreated: 0,
    historicalInstallTracesCreated: 0,
    reachOrBlastRadiusValuesCreated: 0,
    scoresComputed: 0,
    modelsFitted: 0,
    rankingsComputed: 0,
    uncertaintyIntervalsComputed: 0,
    predictiveMetricsComputed: 0,
  },
  prohibitedInterpretations: [
    "This exclusion does not dispute the independently corroborated flatmap-stream incident evidence or convert any unretained version into a benign, safe, unchanged, no-known-event, or control row.",
    "Current registry retention is not historical release evidence and cannot supply a package source, authority, dependency, workflow, provenance, installation, or outcome feature.",
    "The documented relationship to event-stream is relatedness evidence only; it does not establish a new independent campaign family, validation unit, causal pathway, or campaign-complete census.",
    "This artifact does not license reach, blast-radius, attack-return, ranking, calibration, PR-AUC, Recall@K, logistic regression, uncertainty, or predictive claims.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, recordId: artifact.candidate.recordId, affectedVersionTimeUtc, retainedVersionObjectKeys, primaryLedgerRecordsAdded: artifact.currentDecision.primaryLedgerRecordsAdded }, null, 2));
