import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

const sources = {
  wizIocCsv: {
    url: "https://raw.githubusercontent.com/wiz-sec-public/wiz-research-iocs/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/shai-hulud-2-packages.csv",
    commit: "22752e7cc55ece6a053e3277b60b914e0260e65d",
    blobSha: "119c5e0827a54af91cbeb68295059e138bc4ddbe",
  },
  openssfRecord: {
    url: "https://raw.githubusercontent.com/ossf/malicious-packages/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/wenk/MAL-2025-191155.json",
    commit: "c04e75e38121768f82fef0495de77b68b7054d7c",
  },
  npmRegistry: {
    url: "https://registry.npmjs.org/wenk",
  },
};

async function fetchText(url) {
  const response = await fetch(url, {
    headers: {
      Accept: "application/json,text/plain;q=0.9,*/*;q=0.8",
      "User-Agent": "supply-chain-research-shai-hulud-assessment/1.0",
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

const [wizCsv, openssfText, registryText] = await Promise.all([
  fetchText(sources.wizIocCsv.url),
  fetchText(sources.openssfRecord.url),
  fetchText(sources.npmRegistry.url),
]);

const openssf = JSON.parse(openssfText);
const registry = JSON.parse(registryText);
const wizLine = wizCsv.split(/\r?\n/).find(line => line === "wenk,= 1.0.10 || = 1.0.9");
const affected = openssf.affected?.find(entry => entry.package?.ecosystem === "npm" && entry.package?.name === "wenk");
const affectedVersions = [...(affected?.versions ?? [])].sort();
const expectedVersions = ["1.0.10", "1.0.9"].sort();
const references = openssf.references ?? [];
const referenceUrls = references.map(reference => reference.url);
const registryTimes = {
  "1.0.8": registry.time?.["1.0.8"] ?? null,
  "1.0.9": registry.time?.["1.0.9"] ?? null,
  "1.0.10": registry.time?.["1.0.10"] ?? null,
};

assert(wizLine, "Frozen Wiz IOC CSV does not contain the exact wenk affected-version row.");
assert(openssf.id === "MAL-2025-191155", "Unexpected OpenSSF record identifier for wenk.");
assert(JSON.stringify(affectedVersions) === JSON.stringify(expectedVersions), "OpenSSF affected versions do not match the expected wenk pair.");
assert(referenceUrls.some(url => url.includes("aikido.dev/blog/shai-hulud-strikes-again-hitting-zapier-ensdomains")), "OpenSSF record does not retain the Aikido campaign reference.");
assert(referenceUrls.some(url => url.includes("wiz.io/blog/shai-hulud-2-0-ongoing-supply-chain-attack")), "OpenSSF record does not retain the Wiz campaign reference.");
assert(referenceUrls.some(url => url.includes("stepsecurity.io/blog/sha1-hulud-the-second-coming")), "OpenSSF record does not retain the StepSecurity campaign reference.");
assert(registryTimes["1.0.8"] && registryTimes["1.0.9"] && registryTimes["1.0.10"], "Official registry response is missing required wenk timestamps.");

const eventStartUtc = registryTimes["1.0.9"];
const artifact = {
  study: "shai-hulud-second-coming-bounded-package-event-assessment",
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_one_bounded_package_event_record",
  candidateRecord: {
    recordId: "wenk-2025-11-24",
    packageName: "wenk",
    affectedVersions: ["1.0.9", "1.0.10"],
    eventFamily: "shai_hulud_second_coming_2025",
    eventStartUtc,
    labelClass: "confirmed_targeted_compromise",
    primaryPackageTargetEligible: true,
  },
  corroboration: {
    frozenWizIocRow: wizLine,
    openssfRecordId: openssf.id,
    openssfPublishedUtc: openssf.published,
    openssfModifiedUtc: openssf.modified,
    campaignReferencesRetained: referenceUrls.filter(url => /aikido\.dev|wiz\.io|stepsecurity\.io/.test(url)),
    registryVersionTimesUtc: registryTimes,
    preEventLatestVersion: "1.0.8",
    strictFeatureCutoffUtc: new Date(Date.parse(eventStartUtc) - 1).toISOString(),
  },
  sourceProvenance: {
    wizIocCsv: {
      ...sources.wizIocCsv,
      responseSha256: sha256(wizCsv),
      recordCountExcludingHeader: wizCsv.trim().split(/\r?\n/).length - 1,
    },
    openssfRecord: {
      ...sources.openssfRecord,
      responseSha256: sha256(openssfText),
    },
    npmRegistry: {
      ...sources.npmRegistry,
      responseSha256: sha256(registryText),
    },
  },
  inclusionBoundary: [
    "This bounded assessment admits only wenk@1.0.9 and wenk@1.0.10 after cross-source version agreement.",
    "It treats the second-wave campaign as one incident family and does not convert the full IOC CSV into independent families or event records.",
    "The strict feature cutoff is the official registry timestamp of the earliest selected wenk malicious version minus one millisecond.",
  ],
  prohibitedInterpretations: [
    "This artifact does not create a control population or benign labels.",
    "This artifact does not establish campaign-wide completeness, install exposure, dependency reach, or blast radius.",
    "This artifact does not license ranking, calibration, PR-AUC, Recall@K, logistic regression, or attack-return claims.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(path.join(researchDir, "82_shai_hulud_second_coming_candidate_assessment.json"), `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, recordId: artifact.candidateRecord.recordId, eventStartUtc, wizRows: artifact.sourceProvenance.wizIocCsv.recordCountExcludingHeader }, null, 2));
