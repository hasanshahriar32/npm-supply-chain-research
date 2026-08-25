import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const ledgerPath = resolve(root, "research/64_temporal_package_event_ledger.csv");
const keyvAssessmentPath = resolve(root, "research/92_keyv_compromise_candidate_assessment.json");
const outputPath = resolve(root, "research/94_campaign_relatedness_and_grouped_inference_protocol.json");

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    const next = text[index + 1];
    if (char === '"' && quoted && next === '"') {
      field += '"';
      index += 1;
    } else if (char === '"') {
      quoted = !quoted;
    } else if (char === "," && !quoted) {
      row.push(field);
      field = "";
    } else if ((char === "\n" || char === "\r") && !quoted) {
      if (char === "\r" && next === "\n") index += 1;
      row.push(field);
      if (row.some((value) => value.length > 0)) rows.push(row);
      row = [];
      field = "";
    } else {
      field += char;
    }
  }
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

function asObjects(csv) {
  const [header, ...rows] = parseCsv(csv);
  return rows.map((row) => Object.fromEntries(header.map((column, index) => [column, row[index] ?? ""])));
}

const [ledgerText, keyvAssessmentText] = await Promise.all([
  readFile(ledgerPath, "utf8"),
  readFile(keyvAssessmentPath, "utf8"),
]);
const ledger = asObjects(ledgerText);
const keyvAssessment = JSON.parse(keyvAssessmentText);

if (ledger.length < 14) {
  throw new Error(`Expected at least 14 strict ledger records, found ${ledger.length}.`);
}
if (!keyvAssessment.familyRelationship?.crossCampaign?.includes("no statistical independence")) {
  throw new Error("Keyv assessment does not retain the required cross-campaign non-independence boundary.");
}

const familyToRecords = new Map();
for (const record of ledger) {
  const family = record.event_family;
  if (!familyToRecords.has(family)) familyToRecords.set(family, []);
  familyToRecords.get(family).push(record.record_id);
}

const familyInventory = [...familyToRecords.entries()]
  .map(([familyId, recordIds]) => ({
    familyId,
    recordIds,
    recordCount: recordIds.length,
    splitRule: "All member records must remain in the same development, validation, or final-test partition.",
  }))
  .sort((left, right) => left.familyId.localeCompare(right.familyId));

const keyvPayloadLineageFamilies = ["mini_shai_hulud_atool_2026", "keyv_cacheable_august_2026"];
const standaloneValidationUnits = familyInventory
  .filter((family) => !keyvPayloadLineageFamilies.includes(family.familyId))
  .map((family) => ({ validationClusterId: family.familyId, familyIds: [family.familyId] }));
const validationUnits = [
  ...standaloneValidationUnits,
  {
    validationClusterId: "mini_shai_hulud_payload_lineage_cluster",
    familyIds: keyvPayloadLineageFamilies,
  },
].sort((left, right) => left.validationClusterId.localeCompare(right.validationClusterId));

const output = {
  study: "campaign-relatedness-and-grouped-inference-protocol",
  artifactVersion: 1,
  executionStatus: "protocol_only_no_control_frame_or_model_eligible_dataset",
  generatedAtUtc: new Date().toISOString(),
  sourceInputs: {
    strictLedger: {
      path: "research/64_temporal_package_event_ledger.csv",
      sha256: createHash("sha256").update(ledgerText).digest("hex"),
      recordCount: ledger.length,
      familyCount: familyInventory.length,
    },
    keyvAssessment: {
      path: "research/92_keyv_compromise_candidate_assessment.json",
      sha256: createHash("sha256").update(keyvAssessmentText).digest("hex"),
      crossCampaignBoundary: keyvAssessment.familyRelationship.crossCampaign,
    },
  },
  recordInventory: ledger
    .map((record) => ({
      recordId: record.record_id,
      incidentFamily: record.event_family,
      eventStartUtc: record.event_start_utc,
    }))
    .sort((left, right) => left.recordId.localeCompare(right.recordId)),
  familyInventory,
  documentedCrossFamilyRelatedness: [
    {
      relationshipId: "mini_shai_hulud_atool_to_keyv_cacheable_payload_lineage",
      sourceFamilyId: "mini_shai_hulud_atool_2026",
      relatedFamilyId: "keyv_cacheable_august_2026",
      relationshipType: "documented_payload_lineage",
      evidenceStatus: "documented_by_frozen_wiz_and_preserved_in_keyv_assessment",
      permittedInterpretation: "The families remain separately dated campaign-family observations, but their statistical independence is not asserted.",
      requiredValidationClusterId: "mini_shai_hulud_payload_lineage_cluster",
      prohibitedInterpretations: [
        "Do not call payload-lineage evidence proof of independent incidents.",
        "Do not allow the related families to straddle train and test partitions.",
        "Do not resample the two related families as independently exchangeable units.",
      ],
    },
  ],
  validationUnits: {
    unitDefinition: "Connected components of the documented family-relatedness graph, not package-event rows.",
    unitCount: validationUnits.length,
    units: validationUnits,
  },
  futureEligibleOnlyRules: {
    activationPrerequisites: [
      "A frozen package-version population with a documented inclusion rule is available.",
      "A separately adjudicated, target-matched malicious-publication or maintainer-compromise outcome manifest covers a pre-registered horizon.",
      "Historical feature availability and leakage audits pass for the intended split cutoffs.",
      "The final validation-unit registry is frozen before any model fitting or metric inspection.",
    ],
    splitRules: [
      "Use forward-in-time development, validation, and final-test periods; no later event or feature may enter an earlier partition.",
      "Assign every package-event record by its validationClusterId; all records in a cluster must occupy the same partition.",
      "Exclude a proposed split if a target class or required validation unit is absent from its evaluation partition; do not repair this by record-level leakage or by inventing controls.",
      "Store every split definition, random seed, cutoff, validation-unit roster, and exclusion reason before model fitting.",
    ],
    resamplingRules: [
      "If uncertainty is eligible, resample validation units rather than individual package-event rows.",
      "Use only pre-registered cluster-level resampling; report the number of unique validation units and any degenerate replicate exclusions.",
      "Never present fold dispersion, bootstrap percentiles, or cluster-resampling output while the control-frame and model-eligibility gate remains blocked.",
    ],
    reportingRules: [
      "Report package-event count, incident-family count, and validation-unit count separately.",
      "Label Keyv/Cacheable and Mini Shai-Hulud atool as a documented related-family cluster in every eligible split manifest.",
      "Do not equate campaign-family labels, related-family clusters, package-event rows, or downstream affected packages with independent observations.",
    ],
  },
  methodContext: [
    {
      source: "scikit-learn GroupKFold documentation",
      url: "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html",
      permittedUse: "Documents non-overlapping group handling as an implementation reference only; no GroupKFold run occurred.",
    },
    {
      source: "scikit-learn GroupShuffleSplit documentation",
      url: "https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html",
      permittedUse: "Documents randomized splits over domain-defined groups and reproducibility through fixed random states; no split generation occurred.",
    },
    {
      source: "scikit-learn cross-validation user guide",
      url: "https://scikit-learn.org/stable/modules/cross_validation.html",
      permittedUse: "Documents that group structure warrants group-wise validation and time-dependent processes warrant time-aware validation; no model evaluation occurred.",
    },
  ],
  currentDecision: {
    controlsCreated: 0,
    modelsFitted: 0,
    temporalSplitsGenerated: 0,
    uncertaintyIntervalsComputed: 0,
    rankingsComputed: 0,
    predictiveMetricsComputed: 0,
    status: "blocked_pending_control_frame_and_model_eligibility",
  },
  prohibitedInterpretations: [
    "This protocol is not a model, a model evaluation, a confidence interval, or a predictive result.",
    "Do not infer controls, benign labels, outcome prevalence, or non-event rates from this artifact.",
    "Do not treat the 14 package-event rows, 10 incident families, or 9 validation units as sufficient evidence for a fitted model.",
    "Do not convert documented payload lineage into a claim about attacker identity, campaign completeness, or causal transmission.",
  ],
};

await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ outputPath, strictRecords: ledger.length, incidentFamilies: familyInventory.length, validationUnits: output.validationUnits.unitCount, controlsCreated: output.currentDecision.controlsCreated, modelsFitted: output.currentDecision.modelsFitted }, null, 2));
