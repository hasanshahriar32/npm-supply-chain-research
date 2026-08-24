import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

const sources = {
  openssfRecord: {
    url: "https://raw.githubusercontent.com/ossf/malicious-packages/063a778886548231828c8e476eecdb5c5c04fbcb/osv/malicious/npm/is/MAL-2025-6020.json",
    commit: "063a778886548231828c8e476eecdb5c5c04fbcb",
  },
  independentTechnicalReport: "https://www.stepsecurity.io/blog/another-npm-supply-chain-attack-the-is-package-compromise",
  maintainerRemediationChangelog: "https://raw.githubusercontent.com/enricomarino/is/0fe137a5946e4ecb0e649bd7dea48d5415a242fc/CHANGELOG.md",
  maintainerRemediationCommit: "https://github.com/enricomarino/is/commit/0fe137a5946e4ecb0e649bd7dea48d5415a242fc",
  npmRegistry: "https://registry.npmjs.org/is",
};

const expectedVersions = ["3.3.1", "5.0.0"];

async function fetchText(url) {
  const response = await fetch(url, {
    headers: {
      Accept: "application/json,text/plain;q=0.9,text/html;q=0.8,*/*;q=0.7",
      "User-Agent": "supply-chain-research-is-compromise-assessment/1.0",
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

const [openssfText, reportText, changelogText, registryText] = await Promise.all([
  fetchText(sources.openssfRecord.url),
  fetchText(sources.independentTechnicalReport),
  fetchText(sources.maintainerRemediationChangelog),
  fetchText(sources.npmRegistry),
]);

const openssf = JSON.parse(openssfText);
const registry = JSON.parse(registryText);
const affected = openssf.affected?.find((entry) => entry.package?.ecosystem === "npm" && entry.package?.name === "is");
const affectedVersions = [...(affected?.versions ?? [])].sort();
const registryVersionTimesUtc = Object.fromEntries(expectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
const affectedVersionObjectsRetained = Object.fromEntries(expectedVersions.map((version) => [version, Boolean(registry.versions?.[version]) ]));
const earliestAffectedUtc = Object.values(registryVersionTimesUtc).sort()[0];

assert(openssf.id === "MAL-2025-6020", "Unexpected OpenSSF record identifier for is.");
assert(JSON.stringify(affectedVersions) === JSON.stringify([...expectedVersions].sort()), "OpenSSF affected versions do not match the bounded is candidate.");
assert(expectedVersions.every((version) => registryVersionTimesUtc[version]), "Official registry response is missing a required is affected-release timestamp.");
assert(reportText.includes("versions 3.3.1 and 5.0.0") && reportText.includes("July 19, 2025"), "Independent technical report does not retain the expected version pair and timeline.");
assert(changelogText.includes("v3.3.1 (and v5.0.0) were published with malware in them by a hijacked account"), "Maintainer remediation changelog does not corroborate the affected versions and account hijack.");

const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffectedUtc) - 1).toISOString();
const preEventLatestVersion = latestVersionAtOrBefore(registry, strictFeatureCutoffUtc);
assert(preEventLatestVersion, "Official registry response did not retain a pre-event is source version.");

const artifact = {
  study: "is-package-compromise-bounded-package-event-assessment",
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_one_bounded_package_event_record",
  candidateRecord: {
    recordId: "is-2025-07-19",
    packageName: "is",
    affectedVersions: expectedVersions,
    eventFamily: "is_maintainer_compromise_2025",
    eventStartUtc: earliestAffectedUtc,
    labelClass: "confirmed_targeted_compromise",
    primaryPackageTargetEligible: true,
  },
  corroboration: {
    openssfRecordId: openssf.id,
    openssfPublishedUtc: openssf.published,
    openssfModifiedUtc: openssf.modified,
    independentTechnicalReport: sources.independentTechnicalReport,
    maintainerRemediationCommit: sources.maintainerRemediationCommit,
    maintainerChangelogStatement: "v3.3.1 (and v5.0.0) were published with malware in them by a hijacked account",
    origins: openssf.database_specific?.["malicious-packages-origins"] ?? [],
    registryVersionTimesUtc,
    affectedVersionObjectsRetained,
    preEventLatestVersion,
    strictFeatureCutoffUtc,
  },
  sourceProvenance: {
    openssfRecord: { ...sources.openssfRecord, responseSha256: sha256(openssfText) },
    independentTechnicalReport: { url: sources.independentTechnicalReport, responseSha256: sha256(reportText) },
    maintainerRemediationChangelog: { url: sources.maintainerRemediationChangelog, responseSha256: sha256(changelogText) },
    npmRegistry: { url: sources.npmRegistry, responseSha256: sha256(registryText) },
  },
  inclusionBoundary: [
    "This assessment admits only is@3.3.1 and is@5.0.0 after agreement among the frozen OpenSSF record, a dated independent technical report, the project maintainer’s remediation changelog, and the official npm registry version-time map.",
    "The strict cutoff is one millisecond before the earliest affected-release timestamp and selects the latest registry-retained package source object strictly before that time.",
    "The record is one new incident family and does not assert that it is complete for a broader phishing campaign or that any reported downstream effect occurred.",
  ],
  prohibitedInterpretations: [
    "This artifact does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, or blast-radius estimate.",
    "This artifact does not establish campaign-wide completeness or turn correlated campaign packages into independent incident families.",
    "This artifact does not license ranking, calibration, PR-AUC, Recall@K, logistic regression, or attack-return claims.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(path.join(researchDir, "91_is_package_compromise_candidate_assessment.json"), `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, recordId: artifact.candidateRecord.recordId, eventStartUtc: artifact.candidateRecord.eventStartUtc, preEventLatestVersion: artifact.corroboration.preEventLatestVersion }, null, 2));
