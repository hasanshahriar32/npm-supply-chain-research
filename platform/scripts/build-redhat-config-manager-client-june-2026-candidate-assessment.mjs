import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(root, "research", "170_redhat_config_manager_client_june_2026_candidate_assessment.json");
const packageName = "@redhat-cloud-services/config-manager-client";
const registryUrl = "https://registry.npmjs.org/%40redhat-cloud-services%2Fconfig-manager-client";
const affectedVersions = ["5.0.4", "5.0.5"];
const response = await fetch(registryUrl, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-redhat-config-manager-client-candidate-assessment/1.0" } });
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
  study: "redhat-config-manager-client-june-2026-bounded-package-event-candidate-assessment", artifactVersion: 1, artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
  candidate: { recordId: "redhat-cloud-services-config-manager-client-2026-06-01", packageName, affectedVersions, affectedVersionScopeRule: "strict_intersection_of_Red_Hat_primary_bulletin_and_Aikido_exact_version_reporting", earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained, existingFamily: "mini_shai_hulud_atool_2026", familyDecision: "Red Hat and Aikido identify this exact package in the June 2026 Miasma/Mini Shai-Hulud context; it joins the existing family and creates neither a new family nor a new validation unit.", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
  sourceProvenance: { redHatBulletin: "https://access.redhat.com/security/vulnerabilities/RHSB-2026-006", aikido: "https://www.aikido.dev/blog/red-hat-npm-packages-compromised-credential-stealing-worm", npmRegistry: { url: registryUrl, responseSha256: createHash("sha256").update(registryText).digest("hex") } },
  strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: selectedPreEventVersionObjectRetained },
  prohibitedInterpretations: ["Registry metadata establishes only publication-time selection, retained-object availability, direct declarations, and bounded SemVer sensitivity inputs.", "This existing-family admission does not establish historical installation, reach, blast radius, current maintainer state, causal effects, campaign completeness, or statistical independence.", "No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created."],
};
await mkdir(path.dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(assessment, null, 2)}\n`);
console.log(JSON.stringify({ decision: assessment.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
