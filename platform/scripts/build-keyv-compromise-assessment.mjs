import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

const sources = {
  openssfRecord: {
    url: "https://raw.githubusercontent.com/ossf/malicious-packages/88b1340754c17c3d9ae43642c9b2de22b1bbfc10/osv/malicious/npm/keyv/MAL-2026-11524.json",
    commit: "88b1340754c17c3d9ae43642c9b2de22b1bbfc10",
  },
  wizIocList: {
    url: "https://raw.githubusercontent.com/wiz-sec-public/wiz-research-iocs/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/keyv-packages.csv",
    commit: "22752e7cc55ece6a053e3277b60b914e0260e65d",
  },
  wizIncidentReport: "https://www.wiz.io/blog/keyv-and-cacheable-npm-supply-chain-attack",
  snykIncidentReport: "https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/",
  npmRegistry: "https://registry.npmjs.org/keyv",
};

const expectedVersions = ["6.0.0"];

async function fetchText(url) {
  const response = await fetch(url, {
    headers: {
      Accept: "application/json,text/plain;q=0.9,text/csv;q=0.8,text/html;q=0.7,*/*;q=0.6",
      "User-Agent": "supply-chain-research-keyv-compromise-assessment/1.0",
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

function latestVersionAtOrBefore(registry, cutoff) {
  const cutoffMillis = Date.parse(cutoff);
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)) && Date.parse(publishedAt) <= cutoffMillis && registry.versions?.[version])
    .sort((left, right) => Date.parse(right[1]) - Date.parse(left[1]))[0]?.[0] ?? null;
}

const [openssfText, wizListText, wizReportText, snykReportText, registryText] = await Promise.all([
  fetchText(sources.openssfRecord.url),
  fetchText(sources.wizIocList.url),
  fetchText(sources.wizIncidentReport),
  fetchText(sources.snykIncidentReport),
  fetchText(sources.npmRegistry),
]);

const openssf = JSON.parse(openssfText);
const registry = JSON.parse(registryText);
const affected = openssf.affected?.find((entry) => entry.package?.ecosystem === "npm" && entry.package?.name === "keyv");
const affectedVersions = [...(affected?.versions ?? [])].sort();
const registryVersionTimesUtc = Object.fromEntries(expectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
const earliestAffectedUtc = Object.values(registryVersionTimesUtc).sort()[0];

assert(openssf.id === "MAL-2026-11524", "Unexpected OpenSSF record identifier for keyv.");
assert(JSON.stringify(affectedVersions) === JSON.stringify(expectedVersions), "OpenSSF affected versions do not match the bounded keyv candidate.");
assert(registryVersionTimesUtc["6.0.0"], "Official registry response is missing the keyv@6.0.0 publication timestamp.");
assert(/(^|\n)keyv,6\.0\.0(?:\r?\n|$)/.test(wizListText), "Frozen Wiz IOC list does not retain keyv@6.0.0.");
assert(wizReportText.includes("keyv") && wizReportText.includes("over 400 distinct npm packages"), "Wiz incident report does not retain the expected keyv/cacheable campaign context.");
assert(snykReportText.includes("keyv@6.0.0") && snykReportText.includes("published at 09:35:00 UTC"), "Independent Snyk report does not retain keyv@6.0.0 and the publication-time statement.");

const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffectedUtc) - 1).toISOString();
const preEventLatestVersion = latestVersionAtOrBefore(registry, strictFeatureCutoffUtc);
assert(preEventLatestVersion, "Official registry response did not retain a strict pre-event keyv source version.");

const artifact = {
  study: "keyv-compromise-bounded-package-event-assessment",
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_one_bounded_campaign_family_record_without_cross_campaign_independence_claim",
  candidateRecord: {
    recordId: "keyv-2026-08-04",
    packageName: "keyv",
    affectedVersions: expectedVersions,
    eventFamily: "keyv_cacheable_august_2026",
    eventStartUtc: earliestAffectedUtc,
    labelClass: "confirmed_targeted_compromise",
    primaryPackageTargetEligible: true,
  },
  corroboration: {
    openssfRecordId: openssf.id,
    openssfPublishedUtc: openssf.published,
    openssfModifiedUtc: openssf.modified,
    openssfOrigins: openssf.database_specific?.["malicious-packages-origins"] ?? [],
    frozenWizIocList: sources.wizIocList,
    independentSnykIncidentReport: sources.snykIncidentReport,
    registryVersionTimesUtc,
    preEventLatestVersion,
    strictFeatureCutoffUtc,
  },
  familyRelationship: {
    withinCampaign: "This artifact represents only keyv@6.0.0, not the hundreds of packages reported in the August 2026 keyv/cacheable campaign.",
    crossCampaign: "Wiz describes the payload as a descendant of the Mini Shai-Hulud malware family. The August 2026 keyv/cacheable event is retained as a separate dated campaign family, but no statistical independence from the May 2026 Mini Shai-Hulud atool family is asserted.",
  },
  sourceProvenance: {
    openssfRecord: { ...sources.openssfRecord, responseSha256: sha256(openssfText) },
    wizIocList: { ...sources.wizIocList, responseSha256: sha256(wizListText) },
    wizIncidentReport: { url: sources.wizIncidentReport, responseSha256: sha256(wizReportText) },
    independentSnykIncidentReport: { url: sources.snykIncidentReport, responseSha256: sha256(snykReportText) },
    npmRegistry: { url: sources.npmRegistry, responseSha256: sha256(registryText) },
  },
  inclusionBoundary: [
    "This assessment admits only keyv@6.0.0 after agreement among the frozen OpenSSF record, frozen Wiz version list, Wiz incident report, independent Snyk report, and official npm registry version-time map.",
    "The strict cutoff is one millisecond before keyv@6.0.0's official registry timestamp and selects the latest retained source object strictly before that time.",
    "The record is one bounded August 2026 campaign-family observation and does not expand to the reported campaign list or establish cross-campaign independence.",
  ],
  prohibitedInterpretations: [
    "This artifact does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, or blast-radius estimate.",
    "This artifact does not convert a shared malware-family description into evidence that the keyv/cacheable and Mini Shai-Hulud atool campaigns are independent samples.",
    "This artifact does not license ranking, calibration, PR-AUC, Recall@K, logistic regression, or attack-return claims.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(path.join(researchDir, "92_keyv_compromise_candidate_assessment.json"), `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, recordId: artifact.candidateRecord.recordId, eventStartUtc: artifact.candidateRecord.eventStartUtc, preEventLatestVersion: artifact.corroboration.preEventLatestVersion }, null, 2));
