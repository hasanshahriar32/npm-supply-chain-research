import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "108_debug_september_2025_candidate_assessment.json");

const sources = {
  maintainerIncidentIssue: "https://github.com/debug-js/debug/issues/1005",
  wizTechnicalReport: "https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk",
  stepSecurityTechnicalReport: "https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi",
  npmRegistry: "https://registry.npmjs.org/debug",
};

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-debug-september-2025-candidate-assessment/1.0",
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

const [maintainerIssueText, wizText, stepSecurityText, registryText] = await Promise.all([
  fetchText(sources.maintainerIncidentIssue, "text/html, text/plain;q=0.9"),
  fetchText(sources.wizTechnicalReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.stepSecurityTechnicalReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

const registry = JSON.parse(registryText);
const affectedVersion = "4.4.2";
const affectedVersionPublishedUtc = registry.time?.[affectedVersion] ?? null;
const strictFeatureCutoffUtc = affectedVersionPublishedUtc
  ? new Date(Date.parse(affectedVersionPublishedUtc) - 1).toISOString()
  : null;
const preEventVersions = orderedVersionTimes(registry)
  .filter(([, publishedAt]) => strictFeatureCutoffUtc && Date.parse(publishedAt) <= Date.parse(strictFeatureCutoffUtc));
const selectedPreEventVersion = preEventVersions.at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;

assert(maintainerIssueText.includes("debug@4.4.2") && maintainerIssueText.includes("My account has been restored"), "The Debug maintainer issue no longer retains the exact affected version and compromise context.");
assert(wizText.includes("debug@4.4.2") && wizText.includes("social engineering"), "The Wiz report no longer retains the exact Debug version and compromise context.");
assert(stepSecurityText.toLowerCase().includes("debug") && stepSecurityText.includes("4.4.2") && stepSecurityText.includes("phishing"), "The StepSecurity report no longer retains the exact Debug version and phishing context.");
assert(affectedVersionPublishedUtc, "The official npm registry no longer retains a publication timestamp for debug@4.4.2.");
assert(selectedPreEventVersion, "The official npm registry no longer retains a strict pre-event version selection for debug@4.4.2.");

const strictEligibility = {
  finiteExactAffectedVersionIndependentlyCorroborated: true,
  officialAffectedVersionTimestampRetained: true,
  selectedPreEventVersion,
  selectedPreEventVersionObjectRetained,
};

const decision = selectedPreEventVersionObjectRetained
  ? "eligible_for_governed_primary_temporal_ledger_reconstruction"
  : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object";

const artifact = {
  study: "debug-september-2025-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision,
  candidate: {
    recordId: "debug-2025-09-08",
    packageName: "debug",
    affectedVersions: [affectedVersion],
    eventFamilyCandidate: "qix_npm_phishing_september_2025",
    relatednessStatus: "documented_shared_maintainer_compromise_context_requires_one_family_and_one_validation_unit_if_admitted",
    eventStartRule: "The official registry timestamp of independently corroborated debug@4.4.2 defines the strict cutoff; independent reports document the 8 September 2025 compromise context but do not substitute for the registry timestamp.",
    affectedVersionPublishedUtc,
    strictFeatureCutoffUtc,
    timeMapSelectedPreEventVersion: selectedPreEventVersion,
  },
  corroboration: {
    maintainerIncidentIssue: {
      statement: "The Debug project issue identifies debug@4.4.2 among affected releases and reports a phishing-driven npm account compromise.",
    },
    wizTechnicalReport: {
      statement: "Wiz identifies debug@4.4.2 in its exact affected-version list and describes control of the maintainer npm account through social engineering.",
    },
    stepSecurityTechnicalReport: {
      statement: "StepSecurity identifies debug@4.4.2 in its confirmed affected-version list and describes the phishing attack on the maintainer.",
    },
    officialRegistry: {
      boundedMetadataOnly: true,
      affectedVersionPublishedUtc,
      selectedPreEventVersion,
      selectedPreEventVersionObjectRetained,
      retainedVersionObjectKeysIncludeAffectedVersion: Boolean(registry.versions?.[affectedVersion]),
    },
  },
  strictEligibility,
  sourceProvenance: Object.fromEntries([
    ["maintainerIncidentIssue", { url: sources.maintainerIncidentIssue, responseSha256: sha256(maintainerIssueText) }],
    ["wizTechnicalReport", { url: sources.wizTechnicalReport, responseSha256: sha256(wizText) }],
    ["stepSecurityTechnicalReport", { url: sources.stepSecurityTechnicalReport, responseSha256: sha256(stepSecurityText) }],
    ["npmRegistry", { url: sources.npmRegistry, responseSha256: sha256(registryText) }],
  ]),
  nextDecisionBoundary: selectedPreEventVersionObjectRetained
    ? "The candidate may proceed to a separate governed reconstruction only after all ledger-dependent artifacts are updated atomically and the shared-campaign family boundary is retained."
    : "Do not add debug to the primary ledger or create a source snapshot, declaration, range selection, graph edge, campaign family, or validation unit.",
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
    "This evidence screen does not establish campaign completeness, common actor identity beyond the documented maintainer-compromise context, causality, or statistical independence among package rows.",
    "No later package, repository, maintainer, workflow, lockfile, download, payload, installation, or dependency-reach state may be substituted for the selected strict pre-event source object.",
    "An eligible source-object screen alone does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, blast-radius estimate, score, model, ranking, interval, calibration result, or predictive metric.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision, affectedVersionPublishedUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
