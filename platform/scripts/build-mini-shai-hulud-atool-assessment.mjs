import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

const sources = {
  openssfRecord: {
    url: "https://raw.githubusercontent.com/ossf/malicious-packages/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/amapcn/MAL-2026-4127.json",
    commit: "c04e75e38121768f82fef0495de77b68b7054d7c",
  },
  safeDepReport: "https://safedep.io/mini-shai-hulud-strikes-again-314-npm-packages-compromised/",
  socketReport: "https://socket.dev/blog/antv-packages-compromised",
  npmRegistry: "https://registry.npmjs.org/amapcn",
};

async function fetchText(url) {
  const response = await fetch(url, {
    headers: {
      Accept: "application/json,text/plain;q=0.9,*/*;q=0.8",
      "User-Agent": "supply-chain-research-mini-shai-hulud-assessment/1.0",
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

const [openssfText, registryText] = await Promise.all([
  fetchText(sources.openssfRecord.url),
  fetchText(sources.npmRegistry),
]);

const openssf = JSON.parse(openssfText);
const registry = JSON.parse(registryText);
const expectedVersions = ["0.2.2", "0.3.2"];
const affected = openssf.affected?.find(entry => entry.package?.ecosystem === "npm" && entry.package?.name === "amapcn");
const affectedVersions = [...(affected?.versions ?? [])].sort();
const referenceUrls = openssf.references?.map(reference => reference.url) ?? [];
const registryTimes = {
  preEvent: registry.time?.["0.1.2"] ?? null,
  earliestAffected: registry.time?.["0.2.2"] ?? null,
  laterAffected: registry.time?.["0.3.2"] ?? null,
};

assert(openssf.id === "MAL-2026-4127", "Unexpected OpenSSF record identifier for amapcn.");
assert(JSON.stringify(affectedVersions) === JSON.stringify([...expectedVersions].sort()), "OpenSSF affected versions do not match the expected amapcn pair.");
assert(referenceUrls.includes(sources.safeDepReport), "OpenSSF record does not retain the SafeDep incident-report reference.");
assert(referenceUrls.includes(sources.socketReport), "OpenSSF record does not retain the Socket incident-report reference.");
assert(registryTimes.preEvent && registryTimes.earliestAffected && registryTimes.laterAffected, "Official registry response is missing required amapcn timestamps.");
assert(registry.versions?.["0.1.2"], "Official registry response does not retain amapcn@0.1.2 for strict pre-event reconstruction.");

const artifact = {
  study: "mini-shai-hulud-atool-bounded-package-event-assessment",
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_one_bounded_package_event_record",
  candidateRecord: {
    recordId: "amapcn-2026-05-19",
    packageName: "amapcn",
    affectedVersions: expectedVersions,
    eventFamily: "mini_shai_hulud_atool_2026",
    eventStartUtc: registryTimes.earliestAffected,
    labelClass: "confirmed_targeted_compromise",
    primaryPackageTargetEligible: true,
  },
  corroboration: {
    openssfRecordId: openssf.id,
    openssfPublishedUtc: openssf.published,
    openssfModifiedUtc: openssf.modified,
    retainedIndependentSources: {
      safeDep: sources.safeDepReport,
      socket: sources.socketReport,
      origins: openssf.database_specific?.["malicious-packages-origins"] ?? [],
    },
    registryVersionTimesUtc: registryTimes,
    preEventLatestVersion: "0.1.2",
    strictFeatureCutoffUtc: new Date(Date.parse(registryTimes.earliestAffected) - 1).toISOString(),
  },
  sourceProvenance: {
    openssfRecord: { ...sources.openssfRecord, responseSha256: sha256(openssfText) },
    npmRegistry: { url: sources.npmRegistry, responseSha256: sha256(registryText) },
  },
  inclusionBoundary: [
    "This assessment admits only amapcn@0.2.2 and amapcn@0.3.2 after version-level agreement between the inspected SafeDep table and the frozen OpenSSF record.",
    "The Mini Shai-Hulud atool campaign is one incident family; the hundreds of reported packages are not converted into independent families or control observations.",
    "The strict feature cutoff is the official registry timestamp of amapcn@0.2.2 minus one millisecond, selecting amapcn@0.1.2 as the latest retained pre-event source object.",
  ],
  prohibitedInterpretations: [
    "This artifact does not establish campaign-wide completeness or independently count the reported package lists.",
    "This artifact does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, or blast-radius estimate.",
    "This artifact does not license ranking, calibration, PR-AUC, Recall@K, logistic regression, or attack-return claims.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(path.join(researchDir, "84_mini_shai_hulud_atool_candidate_assessment.json"), `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, recordId: artifact.candidateRecord.recordId, eventStartUtc: artifact.candidateRecord.eventStartUtc, preEventLatestVersion: artifact.corroboration.preEventLatestVersion }, null, 2));
