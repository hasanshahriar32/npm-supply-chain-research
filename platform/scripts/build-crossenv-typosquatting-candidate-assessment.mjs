import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "103_crossenv_typosquatting_candidate_assessment.json");

const sources = {
  npmIncidentNotice: "https://blog.npmjs.org/post/163723642530/crossenv-malware-on-the-npm-registry",
  independentTechnicalAccount: "https://iamakulov.com/notes/npm-malicious-packages/",
  independentSnykAdvisory: "https://security.snyk.io/vuln/npm:crossenv:20170802",
  npmRegistry: "https://registry.npmjs.org/crossenv",
};

const candidate = {
  recordId: "crossenv-2017-07-19",
  packageName: "crossenv",
  independentlyReportedAffectedVersion: "6.1.1",
  priorVersionByOfficialTimeMap: "6.0.7",
};

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-crossenv-candidate-assessment/1.0",
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

function latestTimeMappedVersionBefore(registry, cutoffUtc) {
  const cutoff = Date.parse(cutoffUtc);
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)) && Date.parse(publishedAt) <= cutoff)
    .sort((left, right) => Date.parse(right[1]) - Date.parse(left[1]))[0]?.[0] ?? null;
}

const [npmNoticeText, technicalAccountText, snykText, registryText] = await Promise.all([
  fetchText(sources.npmIncidentNotice, "text/html, text/plain;q=0.9"),
  fetchText(sources.independentTechnicalAccount, "text/html, text/plain;q=0.9"),
  fetchText(sources.independentSnykAdvisory, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

const registry = JSON.parse(registryText);
const affectedVersionTimeUtc = registry.time?.[candidate.independentlyReportedAffectedVersion] ?? null;
assert(affectedVersionTimeUtc, "The official registry time map lacks crossenv@6.1.1.");
const strictFeatureCutoffUtc = new Date(Date.parse(affectedVersionTimeUtc) - 1).toISOString();
const selectedPreEventVersion = latestTimeMappedVersionBefore(registry, strictFeatureCutoffUtc);
assert(selectedPreEventVersion === candidate.priorVersionByOfficialTimeMap, "Unexpected crossenv predecessor selected by the official time map.");

const retainedVersionObjectKeys = Object.keys(registry.versions ?? {}).sort();
const selectedPreEventVersionObjectRetained = Boolean(registry.versions?.[selectedPreEventVersion]);
const affectedVersionObjectRetained = Boolean(registry.versions?.[candidate.independentlyReportedAffectedVersion]);

assert(npmNoticeText.includes("July 19") && npmNoticeText.includes("crossenv") && npmNoticeText.includes("hacktask") && npmNoticeText.includes("packages have been removed"), "The npm notice does not retain the expected crossenv incident context.");
assert(technicalAccountText.includes("crossenv - v6.1.1") && technicalAccountText.includes("npm has also"), "The independent technical account does not retain crossenv@6.1.1 and npm-confirmation context.");
assert(snykText.includes("crossenv - v6.1.1") && snykText.includes("one of 37 malicious packages"), "The independent Snyk advisory does not retain crossenv@6.1.1 and typosquatting context.");
assert(!selectedPreEventVersionObjectRetained, "The candidate must not be excluded if an exact retained pre-event source object is available.");

const artifact = {
  study: "crossenv-2017-typosquatting-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "exclude_from_primary_temporal_ledger_due_to_no_retained_pre_event_source_object",
  candidate: {
    recordId: candidate.recordId,
    packageName: candidate.packageName,
    independentlyReportedAffectedVersion: candidate.independentlyReportedAffectedVersion,
    affectedVersionPublishedUtc: affectedVersionTimeUtc,
    strictFeatureCutoffUtc,
    timeMapSelectedPreEventVersion: selectedPreEventVersion,
    eventFamilyCandidate: "hacktask_typosquatting_2017",
    candidateLabelEvidenceStatus: "independently_corroborated_exact_package_version_but_not_primary_ledger_admitted",
  },
  corroboration: {
    npmIncidentNotice: {
      statement: "npm reports that hacktask published deliberate malicious typo-squatted packages on July 19, that crossenv exfiltrated environment variables, and that all hacktask packages were removed.",
      publicNoticeDate: "2017-08-02",
    },
    independentTechnicalAccount: {
      statement: "The account lists crossenv@6.1.1 and links its list to npm confirmation.",
    },
    independentSnykAdvisory: {
      advisoryId: "npm:crossenv:20170802",
      publishedAndDisclosedDate: "2017-08-02",
      statement: "The advisory lists crossenv@6.1.1 as one of the malicious typosquatted packages and says to avoid it.",
    },
    officialRegistry: {
      boundedMetadataOnly: true,
      affectedVersionTimeUtc,
      selectedPreEventVersion,
      selectedPreEventVersionTimeUtc: registry.time?.[selectedPreEventVersion] ?? null,
      affectedVersionObjectRetained,
      selectedPreEventVersionObjectRetained,
      retainedVersionObjectKeys,
    },
  },
  sourceProvenance: {
    npmIncidentNotice: { url: sources.npmIncidentNotice, responseSha256: sha256(npmNoticeText) },
    independentTechnicalAccount: { url: sources.independentTechnicalAccount, responseSha256: sha256(technicalAccountText) },
    independentSnykAdvisory: { url: sources.independentSnykAdvisory, responseSha256: sha256(snykText) },
    npmRegistry: { url: sources.npmRegistry, responseSha256: sha256(registryText) },
  },
  strictExclusionReason: {
    requiredRule: "A primary temporal-ledger record requires a retained official-registry version object selected strictly before the candidate event cutoff so the companion builder can reproduce an exact source snapshot.",
    observedState: "The official registry time map selects crossenv@6.0.7 immediately before the independently reported crossenv@6.1.1 timestamp, but the current bounded response retains only 1.0.0 and 1.0.1 version objects; the selected 6.0.7 object is absent.",
    consequence: "Do not add crossenv to the current primary ledger, do not create a companion source snapshot, direct declarations, range approximations, recursive graph edges, campaign-family count, or validation unit from this candidate.",
  },
  currentDecision: {
    primaryLedgerRecordsAdded: 0,
    primaryLedgerFamiliesAdded: 0,
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
    "This exclusion does not dispute the independently corroborated crossenv incident evidence or convert the candidate into a benign, safe, unchanged, no-known-event, or control row.",
    "Current registry retention is not a release-time package observation and cannot be used as an authority, dependency, workflow, provenance, or historical-installation feature.",
    "This assessment does not create a broader hacktask campaign census, prove campaign completeness, or establish that its packages are independent observations.",
    "This artifact does not license reach, blast-radius, attack-return, ranking, calibration, PR-AUC, Recall@K, logistic regression, uncertainty, or predictive claims.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, recordId: artifact.candidate.recordId, affectedVersionPublishedUtc: affectedVersionTimeUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained, retainedVersionObjectKeys, primaryLedgerRecordsAdded: artifact.currentDecision.primaryLedgerRecordsAdded }, null, 2));
