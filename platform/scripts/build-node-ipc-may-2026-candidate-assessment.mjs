import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(root, "research", "168_node_ipc_may_2026_candidate_assessment.json");
const packageName = "node-ipc";
const registryUrl = "https://registry.npmjs.org/node-ipc";
const affectedVersions = ["9.1.6", "9.2.3", "12.0.1"];
const response = await fetch(registryUrl, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-node-ipc-candidate-assessment/1.0" } });
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);
const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((time) => !time)) throw new Error("Missing official publication time for a finite affected version.");
const earliestAffectedVersion = Object.entries(affectedPublicationTimes).map(([version, publishedUtc]) => ({ version, publishedUtc })).sort((a, b) => Date.parse(a.publishedUtc) - Date.parse(b.publishedUtc))[0];
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffectedVersion.publishedUtc) - 1).toISOString();
const selectedPreEventVersion = Object.entries(registry.time ?? {}).filter(([version, time]) => version !== "created" && version !== "modified" && Date.parse(time) <= Date.parse(strictFeatureCutoffUtc)).sort((a, b) => Date.parse(a[1]) - Date.parse(b[1])).at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = Boolean(selectedPreEventVersion && registry.versions?.[selectedPreEventVersion]);
const assessment = {
  study: "node-ipc-may-2026-bounded-package-event-candidate-assessment", artifactVersion: 1, artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_as_one_bounded_record_in_a_distinct_node_ipc_may_2026_maintainer_account_compromise_family",
  candidate: { recordId: "node-ipc-2026-05-14", packageName, affectedVersions, affectedVersionScopeRule: "strict_intersection_of_StepSecurity_and_Snyk_exact_version_reporting", earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained, eventFamily: "node_ipc_may_2026_maintainer_account_compromise", familyDecision: "Both sources explicitly distinguish the May 2026 event from node-ipc's March 2022 peacenotwar incident, so this is one separate family and one future validation unit.", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
  sourceProvenance: { stepSecurity: "https://www.stepsecurity.io/blog/node-ipc-npm-supply-chain-attack", snyk: "https://snyk.io/blog/malicious-node-ipc-versions-published-npm/", npmRegistry: { url: registryUrl, responseSha256: createHash("sha256").update(registryText).digest("hex") } },
  strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: selectedPreEventVersionObjectRetained },
  prohibitedInterpretations: ["Registry metadata establishes only publication-time selection, retained-object availability, direct declarations, and bounded SemVer sensitivity inputs.", "This new family admission does not establish historical installation, reach, blast radius, current maintainer state, causal effects, campaign completeness, or statistical independence.", "No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created."],
};
await mkdir(path.dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(assessment, null, 2)}\n`);
console.log(JSON.stringify({ decision: assessment.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
