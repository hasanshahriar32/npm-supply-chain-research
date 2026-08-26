import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "110_solana_web3_js_december_2024_candidate_assessment.json");

const sources = {
  projectSecurityAdvisory: "https://github.com/solana-foundation/solana-web3.js/security/advisories/GHSA-jcxm-7wvp-g6p5",
  socketTechnicalReport: "https://socket.dev/blog/supply-chain-attack-solana-web3-js-library",
  npmRegistry: "https://registry.npmjs.org/%40solana%2Fweb3.js",
};
const affectedVersions = ["1.95.6", "1.95.7"];

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-solana-web3-js-december-2024-candidate-assessment/1.0",
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

function orderedVersionTimes(registry) {
  return Object.entries(registry.time ?? {})
    .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
    .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]));
}

const [advisoryText, socketText, registryText] = await Promise.all([
  fetchText(sources.projectSecurityAdvisory, "text/html, text/plain;q=0.9"),
  fetchText(sources.socketTechnicalReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

const registry = JSON.parse(registryText);
const affectedVersionTimes = affectedVersions.map((version) => ({ version, publishedUtc: registry.time?.[version] ?? null }));
assert(affectedVersionTimes.every(({ publishedUtc }) => publishedUtc), "The official npm registry no longer retains publication timestamps for both exact affected versions.");

const earliestAffected = [...affectedVersionTimes].sort((left, right) => Date.parse(left.publishedUtc) - Date.parse(right.publishedUtc))[0];
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffected.publishedUtc) - 1).toISOString();
const selectedPreEventVersion = orderedVersionTimes(registry)
  .filter(([, publishedUtc]) => Date.parse(publishedUtc) <= Date.parse(strictFeatureCutoffUtc))
  .at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;

for (const version of affectedVersions) {
  assert(advisoryText.includes(version), `The project security advisory no longer retains the exact affected version ${version}.`);
  assert(socketText.includes(version), `The independent Socket report no longer retains the exact affected version ${version}.`);
}
assert(advisoryText.includes("publish-access account was compromised"), "The project security advisory no longer retains the publish-access compromise context.");
assert(socketText.toLowerCase().includes("phishing") || socketText.toLowerCase().includes("social engineering"), "The independent Socket report no longer retains a phishing or social-engineering compromise context.");
assert(selectedPreEventVersion, "The official npm registry no longer retains a strict pre-event version selection.");

const decision = selectedPreEventVersionObjectRetained
  ? "eligible_for_governed_primary_temporal_ledger_reconstruction"
  : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object";

const artifact = {
  study: "solana-web3-js-december-2024-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision,
  candidate: {
    recordId: "solana-web3-js-2024-12-03",
    packageName: "@solana/web3.js",
    affectedVersions,
    eventFamilyCandidate: "solana_web3_js_publish_access_compromise_2024",
    relatednessStatus: "no_existing_related_primary_ledger_family_identified_in_this_bounded_screen",
    eventStartRule: "The earliest official registry timestamp among the independently corroborated affected versions defines the strict cutoff; incident-report chronology does not substitute for the registry timestamp.",
    affectedVersionPublicationTimes: affectedVersionTimes,
    eventStartUtc: earliestAffected.publishedUtc,
    strictFeatureCutoffUtc,
    timeMapSelectedPreEventVersion: selectedPreEventVersion,
  },
  corroboration: {
    projectSecurityAdvisory: {
      statement: "The Solana web3.js advisory identifies versions 1.95.6 and 1.95.7, reports a compromised publish-access account, and calls both unauthorized versions.",
    },
    socketTechnicalReport: {
      statement: "Socket independently identifies versions 1.95.6 and 1.95.7 and reports a phishing or social-engineering attack against the maintainers.",
    },
    officialRegistry: {
      boundedMetadataOnly: true,
      affectedVersionPublicationTimes: affectedVersionTimes,
      earliestAffectedVersion: earliestAffected.version,
      eventStartUtc: earliestAffected.publishedUtc,
      selectedPreEventVersion,
      selectedPreEventVersionObjectRetained,
      affectedVersionObjectsRetained: Object.fromEntries(affectedVersions.map((version) => [version, Boolean(registry.versions?.[version])])),
    },
  },
  strictEligibility: {
    finiteExactAffectedVersionsIndependentlyCorroborated: true,
    officialAffectedVersionTimestampsRetained: true,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
  },
  sourceProvenance: Object.fromEntries([
    ["projectSecurityAdvisory", { url: sources.projectSecurityAdvisory, responseSha256: sha256(advisoryText) }],
    ["socketTechnicalReport", { url: sources.socketTechnicalReport, responseSha256: sha256(socketText) }],
    ["npmRegistry", { url: sources.npmRegistry, responseSha256: sha256(registryText) }],
  ]),
  nextDecisionBoundary: selectedPreEventVersionObjectRetained
    ? "The candidate may proceed to a separate governed reconstruction only after all ledger-dependent artifacts are updated atomically and the source-object and family boundaries are preserved."
    : "Do not add @solana/web3.js to the primary ledger or create a source snapshot, declaration, range selection, graph edge, campaign family, or validation unit.",
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
    "This evidence screen does not establish campaign completeness, a common actor identity beyond the documented account-compromise context, causality beyond the source descriptions, or statistical independence from any other package event.",
    "No later package, repository, maintainer, workflow, lockfile, download, payload, installation, or dependency-reach state may be substituted for the selected strict pre-event source object.",
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, blast-radius estimate, score, model, ranking, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision, affectedVersionTimes, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
