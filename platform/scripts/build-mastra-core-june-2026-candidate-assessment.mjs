import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(root, "research", "165_mastra_core_june_2026_candidate_assessment.json");
const packageName = "@mastra/core";
const registryUrl = "https://registry.npmjs.org/%40mastra%2Fcore";
const affectedVersions = ["1.42.1"];
const response = await fetch(registryUrl, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-mastra-core-candidate-assessment/1.0" } });
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
  study: "mastra-core-june-2026-bounded-package-event-candidate-assessment", artifactVersion: 1, artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_as_one_bounded_record_in_a_distinct_mastra_scope_compromise_family",
  candidate: { recordId: "mastra-core-2026-06-17", packageName, affectedVersions, affectedVersionScopeRule: "strict_intersection_of_StepSecurity_and_Snyk_exact_version_reporting", earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained, eventFamily: "mastra_scope_easy_day_js_compromise_2026", familyDecision: "sources document a Mastra scope takeover but do not establish a relation to a pre-existing governed family; one separate family and validation unit are used", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
  sourceProvenance: { stepSecurity: "https://www.stepsecurity.io/blog/mastra-npm-packages-compromised-using-easy-day-js", snyk: "https://snyk.io/blog/a-forgotten-contributor-account-compromised-the-entire-mastra-npm-package-scope/", npmRegistry: { url: registryUrl, responseSha256: createHash("sha256").update(registryText).digest("hex") } },
  strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: selectedPreEventVersionObjectRetained },
  prohibitedInterpretations: ["Registry metadata establishes only publication-time selection, retained-object availability, direct declarations, and bounded SemVer sensitivity inputs.", "The admitted row does not establish historical installation, reach, blast radius, current maintainer state, causal effects, campaign completeness, actor identity beyond source language, or statistical independence.", "No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created."],
};
await mkdir(path.dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(assessment, null, 2)}\n`);
console.log(JSON.stringify({ decision: assessment.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
