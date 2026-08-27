import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const outputPath = path.join(root, "research", "171_redhat_entitlements_client_june_2026_candidate_assessment.json");
const packageName = "@redhat-cloud-services/entitlements-client";
const registryUrl = "https://registry.npmjs.org/%40redhat-cloud-services%2Fentitlements-client";
const affectedVersions = ["4.0.11", "4.0.12"];
const response = await fetch(registryUrl, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-redhat-entitlements-client-candidate-assessment/1.0" } });
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
  study: "redhat-entitlements-client-june-2026-bounded-package-event-candidate-assessment", artifactVersion: 1, artifactDate: new Date().toISOString().slice(0, 10),
  decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
  candidate: { recordId: "redhat-cloud-services-entitlements-client-2026-06-01", packageName, affectedVersions, affectedVersionScopeRule: "strict_intersection_of_Unit_42_and_Aikido_exact_version_reporting;_Unit_42_lists_4.0.11_4.0.12_4.0.14_and_Aikido_lists_4.0.11_4.0.12;_Red_Hat_bulletin_is_contextual_only", earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained, existingFamily: "mini_shai_hulud_atool_2026", familyDecision: "Unit 42 and Aikido independently identify the finite affected-version intersection 4.0.11 and 4.0.12 in the June 2026 Miasma/Mini Shai-Hulud context; Red Hat’s bulletin supplies context only. The row joins the existing family and creates neither a new family nor a new validation unit.", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
  sourceProvenance: { unit42: { url: "https://unit42.paloaltonetworks.com/miasma-npm-supply-chain-attack/", exactVersionsListed: ["4.0.11", "4.0.12", "4.0.14"] }, aikido: { url: "https://www.aikido.dev/blog/red-hat-npm-packages-compromised-credential-stealing-worm", exactVersionsListed: ["4.0.11", "4.0.12"] }, redHatBulletinContextOnly: "https://access.redhat.com/security/vulnerabilities/RHSB-2026-006", npmRegistry: { url: registryUrl, responseSha256: createHash("sha256").update(registryText).digest("hex") } },
  strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: selectedPreEventVersionObjectRetained },
  prohibitedInterpretations: ["Registry metadata establishes only publication-time selection, retained-object availability, direct declarations, and bounded SemVer sensitivity inputs.", "This existing-family admission does not establish historical installation, reach, blast radius, current maintainer state, causal effects, campaign completeness, or statistical independence.", "No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created."],
};
await mkdir(path.dirname(outputPath), { recursive: true });
await writeFile(outputPath, `${JSON.stringify(assessment, null, 2)}\n`);
console.log(JSON.stringify({ decision: assessment.decision, earliestAffectedVersion, strictFeatureCutoffUtc, selectedPreEventVersion, selectedPreEventVersionObjectRetained }, null, 2));
