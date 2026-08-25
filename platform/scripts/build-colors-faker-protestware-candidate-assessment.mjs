import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "105_colors_faker_protestware_candidate_assessment.json");

const sources = {
  snyk: "https://snyk.io/blog/open-source-npm-packages-colors-faker/",
  sonatype: "https://www.sonatype.com/blog/npm-libraries-colors-and-faker-sabotaged-in-protest-by-their-maintainer-what-to-do-now",
  russCox: "https://research.swtch.com/npm-colors",
  colorsRegistry: "https://registry.npmjs.org/colors",
  fakerRegistry: "https://registry.npmjs.org/faker",
};

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function assert(condition, message) {
  if (!condition) throw new Error(message);
}

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-colors-faker-candidate-assessment/1.0",
    },
  });
  const text = await response.text();
  if (!response.ok) throw new Error(`Source request failed (${response.status}) for ${url}`);
  return text;
}

function strictPreEventSource(metadata, cutoffUtc) {
  const cutoffMs = Date.parse(cutoffUtc) - 1;
  const entries = Object.entries(metadata.time ?? {})
    .filter(([version, timestamp]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(timestamp)))
    .map(([version, timestamp]) => ({ version, timestamp, ms: Date.parse(timestamp) }))
    .filter((entry) => entry.ms <= cutoffMs)
    .sort((a, b) => a.ms - b.ms);
  const selected = entries.at(-1) ?? null;
  return {
    selectedVersion: selected?.version ?? null,
    selectedPublishedUtc: selected?.timestamp ?? null,
    exactSourceObjectRetained: Boolean(selected && metadata.versions?.[selected.version]),
    priorVersionCount: entries.length,
  };
}

const [snykText, sonatypeText, russCoxText, colorsRegistryText, fakerRegistryText] = await Promise.all([
  fetchText(sources.snyk, "text/html, text/plain;q=0.9"),
  fetchText(sources.sonatype, "text/html, text/plain;q=0.9"),
  fetchText(sources.russCox, "text/html, text/plain;q=0.9"),
  fetchText(sources.colorsRegistry, "application/json"),
  fetchText(sources.fakerRegistry, "application/json"),
]);

assert(snykText.includes("colors@1.4.1") && snykText.includes("colors@1.4.44-liberty-2") && snykText.includes("6.6.6") && snykText.includes("same maintainer"), "The Snyk report does not retain the expected colors/faker candidate facts.");
assert(sonatypeText.includes("1.4.1, 1.4.2, and 1.4.44-liberty-2") && sonatypeText.includes("faker' package in version 6.6.6") && sonatypeText.includes("same author"), "The Sonatype report does not retain the expected candidate facts.");
assert(russCoxText.includes("intentionally sabotaged") && russCoxText.includes("colors") && russCoxText.includes("faker"), "The independent Russ Cox account does not retain the expected common-maintainer incident context.");

const colorsRegistry = JSON.parse(colorsRegistryText);
const fakerRegistry = JSON.parse(fakerRegistryText);
const colorsAffectedVersions = ["1.4.44-liberty-2", "1.4.1", "1.4.2"];
const fakerAffectedVersions = ["6.6.6"];
const colorsEventEntries = colorsAffectedVersions.map((version) => ({ version, timestamp: colorsRegistry.time?.[version] ?? null }));
const fakerEventEntries = fakerAffectedVersions.map((version) => ({ version, timestamp: fakerRegistry.time?.[version] ?? null }));

assert(colorsEventEntries.every((entry) => Number.isFinite(Date.parse(entry.timestamp))), "Official registry metadata must retain a timestamp for every assessed colors affected version.");
assert(fakerEventEntries.every((entry) => Number.isFinite(Date.parse(entry.timestamp))), "Official registry metadata must retain a timestamp for every assessed faker affected version.");

const colorsEventStartUtc = colorsEventEntries.map((entry) => entry.timestamp).sort()[0];
const fakerEventStartUtc = fakerEventEntries.map((entry) => entry.timestamp).sort()[0];
const colorsPreEvent = strictPreEventSource(colorsRegistry, colorsEventStartUtc);
const fakerPreEvent = strictPreEventSource(fakerRegistry, fakerEventStartUtc);

assert(colorsPreEvent.exactSourceObjectRetained, "The candidate requires a retained exact pre-event colors source object.");
assert(fakerPreEvent.exactSourceObjectRetained, "The candidate requires a retained exact pre-event faker source object.");

const candidates = [
  {
    recordId: "colors-2022-01-08",
    packageName: "colors",
    affectedVersions: colorsAffectedVersions,
    eventStartUtc: colorsEventStartUtc,
    sourceSelection: colorsPreEvent,
  },
  {
    recordId: "faker-2022-01-05",
    packageName: "faker",
    affectedVersions: fakerAffectedVersions,
    eventStartUtc: fakerEventStartUtc,
    sourceSelection: fakerPreEvent,
  },
];

const artifact = {
  study: "colors-faker-2022-bounded-related-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_two_related_records_to_existing_primary_temporal_ledger_under_single_new_related_family",
  eventFamily: "colors_faker_protestware_2022",
  relatednessRule: "colors and faker are two package-event records in one related family because independent sources identify a common maintainer and coordinated intentional disruption. They cannot create two independent validation units, and this relationship does not establish a causal mechanism beyond the documented shared-maintainer incident context.",
  labelClass: "confirmed_malicious_publication",
  evidenceTier: "independent_technical_and_vendor",
  candidates,
  corroboration: {
    snyk: "Snyk reports colors@1.4.1 and colors@1.4.44-liberty-2 as intentionally breaking publications and describes faker@6.6.6 as an empty package after a forced repository change by the same maintainer.",
    sonatype: "Sonatype independently reports colors 1.4.1, 1.4.2, and 1.4.44-liberty-2 as anomalous and faker@6.6.6 as a functional-code purge, identifying a shared author.",
    russCox: "Russ Cox independently documents intentional sabotage of both colors and faker and the contemporaneous impact of a newly published colors version on fresh installs.",
  },
  sourceProvenance: {
    snyk: { url: sources.snyk, responseSha256: sha256(snykText) },
    sonatype: { url: sources.sonatype, responseSha256: sha256(sonatypeText) },
    russCox: { url: sources.russCox, responseSha256: sha256(russCoxText) },
    colorsRegistry: { url: sources.colorsRegistry, responseSha256: sha256(colorsRegistryText) },
    fakerRegistry: { url: sources.fakerRegistry, responseSha256: sha256(fakerRegistryText) },
  },
  strictAdmissionRule: {
    required: "Each ledger record requires independently corroborated package/version scope, an official registry timestamp for the earliest assessed affected release, and a retained official registry package-version object strictly before the resulting cutoff.",
    result: "Both candidate records satisfy the bounded rule. The registry time map sets each strict cutoff; a retained source object exists for the immediate prior retained version selected only by the official time map.",
  },
  currentDecision: {
    primaryLedgerRecordsAdded: 2,
    primaryLedgerFamiliesAdded: 1,
    primaryLedgerValidationUnitsAdded: 1,
    exactPreEventSourceSnapshotsExpected: 2,
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
    "The two records are related and count as one future validation unit, not two independent observations.",
    "The selected registry source objects are cutoff-valid source metadata only; they are not package downloads, installs, lockfiles, historical installation trees, or evidence of runtime reach.",
    "Admission does not create controls, benign labels, a complete campaign census, authority features, release comparisons, causal conclusions, scores, models, rankings, calibration, uncertainty intervals, or predictive metrics.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, candidates: candidates.map((candidate) => ({ recordId: candidate.recordId, eventStartUtc: candidate.eventStartUtc, preEventVersion: candidate.sourceSelection.selectedVersion })), primaryLedgerRecordsAdded: artifact.currentDecision.primaryLedgerRecordsAdded }, null, 2));
