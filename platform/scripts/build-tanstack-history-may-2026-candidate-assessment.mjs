import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(root, "research", "155_tanstack_history_may_2026_candidate_assessment.json");
const packageName = "@tanstack/history";
const registryUrl = "https://registry.npmjs.org/%40tanstack%2Fhistory";
const affectedVersions = ["1.161.9", "1.161.12"];
const response = await fetch(registryUrl, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-tanstack-history-candidate-assessment/1.0" } });
const registryText = await response.text();
if (!response.ok) throw new Error(`Official npm registry request failed (${response.status}).`);
const registry = JSON.parse(registryText);
const affectedPublicationTimes = Object.fromEntries(affectedVersions.map((version) => [version, registry.time?.[version] ?? null]));
if (Object.values(affectedPublicationTimes).some((time) => !time)) throw new Error("Missing official publication time for a finite affected version.");
const earliestAffectedVersion = Object.entries(affectedPublicationTimes).map(([version, publishedUtc]) => ({ version, publishedUtc })).sort((a, b) => Date.parse(a.publishedUtc) - Date.parse(b.publishedUtc))[0];
const strictFeatureCutoffUtc = new Date(Date.parse(earliestAffectedVersion.publishedUtc) - 1).toISOString();
const retainedBeforeCutoff = Object.entries(registry.time ?? {}).filter(([version, time]) => version !== "created" && version !== "modified" && Date.parse(time) <= Date.parse(strictFeatureCutoffUtc)).sort((a, b) => Date.parse(a[1]) - Date.parse(b[1]));
const selectedPreEventVersion = retainedBeforeCutoff.at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = Boolean(selectedPreEventVersion && registry.versions?.[selectedPreEventVersion]);
const assessment = {
  study: "tanstack-history-may-2026-bounded-package-event-candidate-assessment", artifactVersion: 1, artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
  candidate: { recordId: "tanstack-history-2026-05-11", packageName, affectedVersions, affectedVersionScopeRule: "strict_intersection_of_TanStack_postmortem_and_StepSecurity_exact_version_lists", earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained, existingFamily: "mini_shai_hulud_atool_2026", familyDecision: "external StepSecurity reporting explicitly describes the event as TeamPCP Mini Shai-Hulud; the new row is not a distinct family or validation unit", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
  sourceProvenance: { tanStackPostmortem: "https://tanstack.com/blog/npm-supply-chain-compromise-postmortem", stepSecurity: "https://www.stepsecurity.io/blog/mini-shai-hulud-is-back-a-self-spreading-supply-chain-attack-hits-the-npm-ecosystem", npmRegistry: { url: registryUrl, responseSha256: createHash("sha256").update(registryText).digest("hex") } },
  strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: selectedPreEventVersionObjectRetained },
  prohibitedInterpretations: ["Registry metadata establishes only publication-time selection, retained-object availability, direct declarations, and bounded SemVer sensitivity inputs.", "The admitted row does not establish historical installation, reach, blast radius, current maintainer state, causal effects, campaign completeness, actor identity beyond source language, or statistical independence.", "No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created."],
};
await mkdir(path.dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(assessment, null, 2)}\n`);
console.log(JSON.stringify({ decision: assessment.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
