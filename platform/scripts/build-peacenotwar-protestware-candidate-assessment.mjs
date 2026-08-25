import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "106_peacenotwar_protestware_candidate_assessment.json");

const sources = {
  snykIncidentReport: "https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/",
  snykAdvisory: "https://security.snyk.io/vuln/SNYK-JS-PEACENOTWAR-2426724",
  cncfCompromiseCatalogue: "https://tag-security.cncf.io/community/catalog/compromises/2022/node-ipc-peacenotwar/",
  npmRegistry: "https://registry.npmjs.org/peacenotwar",
};

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-peacenotwar-candidate-assessment/1.0",
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

function versionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const [snykReportText, snykAdvisoryText, cncfText, registryText] = await Promise.all([
  fetchText(sources.snykIncidentReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.snykAdvisory, "text/html, text/plain;q=0.9"),
  fetchText(sources.cncfCompromiseCatalogue, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

const registry = JSON.parse(registryText);
const orderedVersionTimes = versionTimes(registry);
const firstRegistryVersion = orderedVersionTimes[0]?.[0] ?? null;
const firstRegistryVersionPublishedUtc = orderedVersionTimes[0]?.[1] ?? null;
const strictFeatureCutoffUtc = firstRegistryVersionPublishedUtc
  ? new Date(Date.parse(firstRegistryVersionPublishedUtc) - 1).toISOString()
  : null;
const preEventVersions = orderedVersionTimes.filter(([, publishedAt]) => strictFeatureCutoffUtc && Date.parse(publishedAt) <= Date.parse(strictFeatureCutoffUtc));
const selectedPreEventVersion = preEventVersions.at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;

assert(snykReportText.includes("published an npm package called") && snykReportText.includes("peacenotwar") && snykReportText.includes("March 8"), "The Snyk incident report does not retain the peacenotwar publication context.");
assert(/peacenotwar[\s\S]{0,320}package, versions[\s\S]{0,180}>\*<\/strong>/i.test(snykAdvisoryText) && snykAdvisoryText.includes("creates files on users' desktops") && snykAdvisoryText.includes("OneDrive"), "The Snyk advisory does not retain its all-versions scope and stated behavior.");
assert(cncfText.includes("npm Library ‘node-ipc’ Sabotaged with npm Library ‘peacenotwar’") && cncfText.includes("malicious maintainer"), "The CNCF catalogue does not retain the peacenotwar compromise classification.");
assert(firstRegistryVersion === "9.1.1", "The official registry no longer selects peacenotwar@9.1.1 as its first retained publication.");
assert(selectedPreEventVersion === null, "A pre-event version must not be inferred before the first retained peacenotwar publication.");

const artifact = {
  study: "peacenotwar-2022-protestware-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "exclude_from_primary_temporal_ledger_due_to_no_strict_pre_event_source_object_and_no_exact_version_specific_advisory_target",
  candidate: {
    recordId: "peacenotwar-2022-03-08",
    packageName: "peacenotwar",
    eventFamilyCandidate: "node_ipc_peacenotwar_protestware_2022",
    relatednessStatus: "potentially_related_to_node_ipc_protestware_context_but_no_new_family_or_validation_unit_created",
    advisoryAffectedVersionScope: "all_versions",
    registryFirstVersion: firstRegistryVersion,
    registryFirstVersionPublishedUtc: firstRegistryVersionPublishedUtc,
    strictFeatureCutoffUtc,
    timeMapSelectedPreEventVersion: selectedPreEventVersion,
  },
  corroboration: {
    snykIncidentReport: {
      publishedDate: "2022-03-16",
      statement: "Snyk reports that the maintainer wrote source and published peacenotwar on March 8 before adding it to node-ipc.",
    },
    snykAdvisory: {
      advisoryId: "SNYK-JS-PEACENOTWAR-2426724",
      publishedAndDisclosedDate: "2022-03-16",
      statement: "Snyk describes all peacenotwar versions as affected and the package as creating files on users' desktops and OneDrive.",
    },
    cncfCompromiseCatalogue: {
      statement: "The CNCF TAG Security catalogue classifies the node-ipc/peacenotwar incident as malicious maintainer behavior and identifies intentional corrupt versions.",
    },
    officialRegistry: {
      boundedMetadataOnly: true,
      retainedVersionTimes: orderedVersionTimes,
      retainedVersionObjectKeys: Object.keys(registry.versions ?? {}).sort(),
      firstRegistryVersion,
      firstRegistryVersionPublishedUtc,
      selectedPreEventVersion,
      selectedPreEventVersionObjectRetained,
    },
  },
  sourceProvenance: Object.fromEntries([
    ["snykIncidentReport", { url: sources.snykIncidentReport, responseSha256: sha256(snykReportText) }],
    ["snykAdvisory", { url: sources.snykAdvisory, responseSha256: sha256(snykAdvisoryText) }],
    ["cncfCompromiseCatalogue", { url: sources.cncfCompromiseCatalogue, responseSha256: sha256(cncfText) }],
    ["npmRegistry", { url: sources.npmRegistry, responseSha256: sha256(registryText) }],
  ]),
  strictExclusionReason: {
    requiredRule: "A primary ledger record requires an independently corroborated exact affected release or finite release set and an official registry version object selected strictly before the registered event cutoff.",
    observedState: "The advisory scope is all peacenotwar versions and the incident report supplies a March 8 publication context, but no inspected independent source identifies a finite event-specific peacenotwar version. The official registry's first retained publication is 9.1.1, so no strictly earlier source version exists to reconstruct an exact pre-event snapshot.",
    consequence: "Do not add peacenotwar to the primary ledger, do not create a companion source snapshot, direct declarations, range selections, graph edges, campaign family, or validation unit from this candidate.",
  },
  currentDecision: {
    primaryLedgerRecordsAdded: 0,
    primaryLedgerFamiliesAdded: 0,
    futureValidationUnitsAdded: 0,
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
    "This exclusion does not dispute the documented peacenotwar behavior or convert the candidate into a benign, safe, unchanged, no-known-event, or control row.",
    "Downstream node-ipc version evidence cannot be substituted for an independently corroborated exact peacenotwar event version.",
    "The all-versions advisory scope cannot be collapsed into a finite exact release target without a source that explicitly identifies the candidate version set.",
    "This artifact does not license reach, blast-radius, attack-return, ranking, calibration, PR-AUC, Recall@K, logistic regression, uncertainty, or predictive claims.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, firstRegistryVersion, selectedPreEventVersion, primaryLedgerRecordsAdded: artifact.currentDecision.primaryLedgerRecordsAdded }, null, 2));
