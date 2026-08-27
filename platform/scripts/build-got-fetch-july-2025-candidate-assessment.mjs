import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "154_got_fetch_july_2025_candidate_assessment.json");
const npmRegistry = "https://registry.npmjs.org/got-fetch";
const affectedVersions = ["5.1.11", "5.1.12"];
const response = await fetch(npmRegistry, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-got-fetch-candidate-assessment/1.0" } });
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);
const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((value) => !value)) throw new Error("Missing official affected-version publication time.");
const earliestAffectedVersion = Object.entries(affectedPublicationTimes).map(([version, publishedUtc]) => ({ version, publishedUtc })).sort((a, b) => Date.parse(a.publishedUtc) - Date.parse(b.publishedUtc))[0];
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffectedVersion.publishedUtc) - 1).toISOString();
const selectedPreEventVersion = Object.entries(registry.time ?? {}).filter(([version, time]) => version !== "created" && version !== "modified" && Date.parse(time) <= Date.parse(strictFeatureCutoffUtc)).sort((a, b) => Date.parse(a[1]) - Date.parse(b[1])).at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = Boolean(selectedPreEventVersion && registry.versions?.[selectedPreEventVersion]);
const artifact = {
  study: "got-fetch-july-2025-bounded-package-event-candidate-assessment", artifactVersion: 1, artifactDate: new Date().toISOString().slice(0, 10),
  decision: selectedPreEventVersionObjectRetained ? "eligible_pending_relatedness_adjudication_before_governed_primary_temporal_ledger_reconstruction" : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
  candidate: { recordId: "got-fetch-2025-07-17", packageName: "got-fetch", eventFamilyCandidate: "got_fetch_july_2025_phishing_compromise_unresolved_relatedness", affectedVersions, affectedVersionScopeRule: "strict_two_version_intersection_of_independent_sources_only", earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained, documentedIncidentContext: "phishing_compromise_context_with_reported_other_affected_packages", distinctFromExistingLedgerFamilies: "unresolved_requires_explicit_adjudication" },
  sourceProvenance: { checkmarx: "https://checkmarx.com/zero-post/supply-chain-phishing-campaign-drops-more-malware-into-npm-got-fetch-5-1/", snyk: "https://security.snyk.io/vuln/SNYK-JS-GOTFETCH-10873306", npmRegistry: { url: npmRegistry, responseSha256: createHash("sha256").update(registryText).digest("hex") } },
  strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion, selectedPreEventVersionObjectRetained, relatednessAdjudicated: false, eligibleForGovernedReconstruction: false },
  currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, calibrationResultsCreated: 0, predictiveMetricsComputed: 0 },
  nextDecisionBoundary: "Do not admit until documented campaign relatedness to the existing eslint-config-prettier family has been adjudicated from independently reviewable sources.",
  prohibitedInterpretations: ["Registry metadata establishes publication-time selection and retained-object availability only; it does not establish historical installations, reach, blast radius, current state, or causal effects.", "The reported other affected packages do not establish a governed-family assignment, campaign completeness, actor linkage, or statistical independence.", "No cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric is created."],
};
await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
