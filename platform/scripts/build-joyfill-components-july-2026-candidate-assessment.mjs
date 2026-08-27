import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "146_joyfill_components_july_2026_candidate_assessment.json");

const artifact = {
  study: "joyfill-components-july-2026-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "exclude_from_new_independent_primary_family_due_to_documented_polinrider_relatedness",
  candidate: {
    recordId: "joyfill-components-2026-07-28",
    packageName: "@joyfill/components",
    sourceOneAffectedVersions: ["4.0.0-rc24-2773-beta.4", "4.0.0-rc24-2773-beta.5", "4.0.0-rc24-2773-beta.6"],
    sourceTwoAffectedVersions: ["4.0.0-rc24-2773-beta.4"],
    affectedVersionIntersection: ["4.0.0-rc24-2773-beta.4"],
    affectedVersionScopeRule: "single_version_intersection_of_independently_reviewed_sources_only",
    documentedRelatedCampaign: "PolinRider",
    existingRelatedGovernedFamily: "common_stack_generate_plugin_polinrider_hijack_2026",
    distinctFromExistingLedgerFamilies: false,
  },
  corroboration: {
    stepSecurity: {
      url: "https://www.stepsecurity.io/blog/joyfill-npm-supply-chain-compromise",
      statement: "Independent technical report identifies three @joyfill/components 2773 beta versions as malicious.",
    },
    socket: {
      url: "https://socket.dev/blog/joyfill-npm-beta-releases-compromised",
      statement: "Independent report identifies @joyfill/components@4.0.0-rc24-2773-beta.4 and explicitly links the package to the ongoing PolinRider supply-chain attack.",
    },
  },
  registryBoundary: {
    officialRegistryRequestAttempted: false,
    strictFeatureCutoffUtc: null,
    selectedPreEventVersion: null,
    selectedPreEventVersionObjectRetained: null,
    reason: "Registry access is not permitted because the documented PolinRider relation fails the prior genuinely-separate-family gate for this autonomous screen.",
  },
  strictExclusionReason: {
    condition: "documented_relatedness_to_existing_governed_polinrider_family",
    consequence: "Do not add @joyfill/components as a new independent primary-ledger family or future validation unit in this screen.",
  },
  currentDecision: {
    primaryLedgerRecordsAdded: 0,
    primaryLedgerFamiliesAdded: 0,
    futureValidationUnitsAdded: 0,
    exactPreEventSourceSnapshotsCreated: 0,
    dependencyDeclarationsCreated: 0,
    isolatedSemverApproximationsCreated: 0,
    recursiveGraphEdgesCreated: 0,
    controlsCreated: 0,
    benignLabelsCreated: 0,
    historicalInstallTracesCreated: 0,
    reachOrBlastRadiusValuesCreated: 0,
    scoresComputed: 0,
    modelsFitted: 0,
    rankingsComputed: 0,
    uncertaintyIntervalsComputed: 0,
    calibrationResultsCreated: 0,
    predictiveMetricsComputed: 0,
  },
  prohibitedInterpretations: [
    "This exclusion does not dispute the independently reported malicious release or establish that it is benign, safe, unchanged, or a non-event.",
    "The documented PolinRider relation does not establish campaign completeness, a complete related-package set, a current publisher state, or a statistical-independence claim.",
    "No registry response, package payload, archive, source extraction, installation, historical-install trace, reach value, blast-radius value, control, score, model, rank, interval, calibration result, or predictive metric is created.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, affectedVersionIntersection: artifact.candidate.affectedVersionIntersection, registryRequestAttempted: artifact.registryBoundary.officialRegistryRequestAttempted }, null, 2));
