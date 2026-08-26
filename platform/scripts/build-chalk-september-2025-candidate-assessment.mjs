import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const output = path.join(root, "research", "112_chalk_september_2025_candidate_assessment.json");
const urls = {
  maintainerIssue: "https://github.com/chalk/chalk/issues/656",
  independentReport: "https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi",
  registry: "https://registry.npmjs.org/chalk",
};
const affectedVersion = "5.6.1";
const sha256 = (text) => createHash("sha256").update(text).digest("hex");
const fetchText = async (url, accept) => {
  const response = await fetch(url, { headers: { Accept: accept, "User-Agent": "supply-chain-research-chalk-september-2025-candidate-assessment/1.0" } });
  const text = await response.text();
  if (!response.ok) throw new Error(`Source request failed (${response.status}) for ${url}`);
  return text;
};
const assert = (condition, message) => { if (!condition) throw new Error(message); };

const [issueText, reportText, registryText] = await Promise.all([
  fetchText(urls.maintainerIssue, "text/html, text/plain;q=0.9"),
  fetchText(urls.independentReport, "text/html, text/plain;q=0.9"),
  fetchText(urls.registry, "application/json"),
]);
const registry = JSON.parse(registryText);
assert(issueText.includes(`chalk@${affectedVersion}`), "The Chalk maintainer issue no longer retains the finite affected version.");
assert(issueText.toLowerCase().includes("compromised account"), "The Chalk maintainer issue no longer retains the compromised-account context.");
assert(reportText.toLowerCase().includes("chalk") && reportText.includes(affectedVersion), "The independent report no longer retains the finite Chalk version.");
assert(reportText.toLowerCase().includes("phishing"), "The independent report no longer retains the phishing compromise context.");
const eventStartUtc = registry.time?.[affectedVersion];
assert(eventStartUtc, "The official registry no longer retains the affected Chalk publication timestamp.");
const cutoffUtc = new Date(Date.parse(eventStartUtc) - 1).toISOString();
const selectedPreEventVersion = Object.entries(registry.time ?? {})
  .filter(([version, published]) => version !== "created" && version !== "modified" && Date.parse(published) <= Date.parse(cutoffUtc))
  .sort((a, b) => Date.parse(a[1]) - Date.parse(b[1])).at(-1)?.[0] ?? null;
const retained = selectedPreEventVersion ? Boolean(registry.versions?.[selectedPreEventVersion]) : false;
assert(selectedPreEventVersion, "The registry retains no strict pre-event Chalk version selection.");
const decision = retained ? "eligible_for_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object";
const artifact = {
  study: "chalk-september-2025-bounded-package-event-candidate-assessment", artifactVersion: 1, artifactDate: new Date().toISOString().slice(0, 10), decision,
  candidate: { recordId: "chalk-2025-09-08", packageName: "chalk", affectedVersions: [affectedVersion], existingFamily: "qix_npm_phishing_september_2025", relatednessBoundary: "This record joins the existing Debug September 2025 Qix family and cannot add an independent family or validation unit.", eventStartRule: "The official registry timestamp of the independently corroborated affected version defines the strict cutoff.", eventStartUtc, strictFeatureCutoffUtc: cutoffUtc, timeMapSelectedPreEventVersion: selectedPreEventVersion },
  corroboration: { maintainerIssue: "Chalk issue #656 identifies chalk@5.6.1 and a compromised account.", independentTechnicalReport: "StepSecurity independently lists chalk@5.6.1 and documents the phishing campaign.", officialRegistry: { boundedMetadataOnly: true, affectedVersionPublicationUtc: eventStartUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained: retained, affectedVersionObjectRetained: Boolean(registry.versions?.[affectedVersion]) } },
  strictEligibility: { finiteExactAffectedVersionIndependentlyCorroborated: true, officialAffectedVersionTimestampRetained: true, selectedPreEventVersion, selectedPreEventVersionObjectRetained: retained, joinsExistingFamily: true },
  sourceProvenance: Object.fromEntries([["maintainerIssue", { url: urls.maintainerIssue, responseSha256: sha256(issueText) }], ["independentReport", { url: urls.independentReport, responseSha256: sha256(reportText) }], ["npmRegistry", { url: urls.registry, responseSha256: sha256(registryText) }]]),
  nextDecisionBoundary: retained ? "The candidate may proceed only as a second package-event row in the existing Qix family; all ledger-dependent artifacts must be regenerated atomically and validation-unit count must remain unchanged." : "Do not add a ledger row, snapshot, declaration, edge, family, or validation unit.",
  currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
  prohibitedInterpretations: ["This screen does not establish campaign completeness, a causal pathway across packages, a common actor identity beyond documented sources, or statistical independence from Debug or any unadjudicated candidate.", "No later package, repository, maintainer, workflow, lockfile, download, payload, installation, or dependency-reach state may substitute for the strict source object.", "An eligible screen alone does not create controls, benign labels, historical installations, reach, blast-radius estimates, scores, models, rankings, intervals, calibration, or predictive metrics."],
};
await mkdir(path.dirname(output), { recursive: true });
await writeFile(output, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision, eventStartUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained: retained }, null, 2));
