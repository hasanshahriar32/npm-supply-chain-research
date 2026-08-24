import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const availabilityPath = path.join(researchDir, "95_release_authority_metadata_availability_audit.json");
const outputPath = path.join(researchDir, "96_release_authority_delta_semantics_protocol.json");

const availabilityText = await readFile(availabilityPath, "utf8");
const availability = JSON.parse(availabilityText);
if (availability.executionStatus !== "availability_audit_only_no_feature_values_deltas_scores_or_models") {
  throw new Error("The availability audit no longer has the required availability-only status.");
}
if (availability.summary?.deltasClassified !== 0 || availability.summary?.releaseAuthorityScoresComputed !== 0) {
  throw new Error("The availability audit must not contain classified deltas or authority scores.");
}

const output = {
  study: "future-only-release-authority-delta-semantics-protocol",
  artifactVersion: 1,
  executionStatus: "protocol_only_no_metadata_values_compared_or_deltas_classified",
  generatedAtUtc: new Date().toISOString(),
  inputGate: {
    strictAvailabilityAudit: {
      path: "research/95_release_authority_metadata_availability_audit.json",
      sha256: createHash("sha256").update(availabilityText).digest("hex"),
      requiredStatus: availability.executionStatus,
      observedAvailabilitySummary: {
        exactPreEventSourceSnapshots: availability.summary.exactPreEventSourceSnapshots,
        predecessorAvailable: availability.summary.predecessorAvailable,
        repositoryDescriptorComparisonAvailable: availability.summary.repositoryDescriptorComparisonAvailable,
        gitHeadComparisonAvailable: availability.summary.gitHeadComparisonAvailable,
        publishConfigComparisonAvailable: availability.summary.publishConfigComparisonAvailable,
      },
    },
    mandatoryActivationPrerequisites: [
      "A frozen package-version population and target-matched, horizon-covered outcome manifest satisfy the primary control-frame contract.",
      "The selected release and its immediate predecessor are independently retained, version-addressable historical source objects that precede the relevant release cutoff.",
      "The raw field source, retrieval time, response checksum, canonicalization function, and field-specific semantics are fixed before inspecting outcome labels or metrics.",
      "The campaign-relatedness validation-unit registry is frozen before any future split, resampling, or metric computation.",
    ],
  },
  comparisonUnit: {
    definition: "One candidate release and its immediate earlier retained release for the same package coordinate, both evaluated using their version-specific historical evidence.",
    disallowedSubstitutes: [
      "A current package root document, current dist-tag, current maintainer roster, or current repository state.",
      "A nearest semantic-version predecessor when a later timestamped pre-release or retained release is the immediate historical predecessor.",
      "A package-event incident row, campaign family, or downstream dependent as an authority-comparison unit.",
    ],
  },
  eligibilityDecisionVocabulary: {
    eligible_for_opaque_comparison: "Both source objects and all field-specific evidence prerequisites are retained and time-valid; comparison remains unpublished until the full benchmark gate opens.",
    not_eligible_missing_or_ambiguous_evidence: "One or more required source objects, field values, canonicalization inputs, provenance references, or time-validity checks are absent or ambiguous.",
    not_applicable_to_release_regime: "The named delta type is not meaningful for the release regime or registry evidence available.",
    prohibitedFallback: "Never map unavailable, missing, current-only, or ambiguous evidence to unchanged, safe, benign, or no-known-event.",
  },
  deltaOntology: [
    {
      deltaType: "repository_link_discontinuity",
      candidateEvidence: "Version-specific normalized repository descriptor from the selected release and its immediate retained predecessor.",
      minimumEligibility: [
        "Both opaque raw descriptors are retained in immutable raw inputs.",
        "A pre-registered normalization maps syntactic transport variants only; it must not follow redirects or query current repository ownership.",
        "The comparison record carries both version timestamps and source-response checksums.",
      ],
      permittedOutputIfEligible: "opaque equality-or-difference status plus canonicalization version and provenance references; never publish the repository URL in the benchmark feature table.",
      nonInterpretation: "A repository-link difference is a review-surface discontinuity, not evidence of a hostile transfer, compromise, or malicious payload.",
    },
    {
      deltaType: "source_revision_reference_discontinuity",
      candidateEvidence: "Version-specific git-head or equivalent source-revision reference from both retained release objects.",
      minimumEligibility: [
        "Both opaque revision references are retained and bound to their release-version objects.",
        "A registry-specific semantics record states whether the field is publisher-supplied, verified, or unknown.",
        "No current VCS branch, tag, commit availability, or repository ownership lookup is used to fill missing historical evidence.",
      ],
      permittedOutputIfEligible: "opaque equality-or-difference status only, with evidence-fidelity and semantics labels.",
      nonInterpretation: "A changed or absent revision reference is not a code-diff, provenance verdict, or compromise label.",
    },
    {
      deltaType: "release_manifest_publication_intent_discontinuity",
      candidateEvidence: "Version-specific publish configuration or provenance-intent fields preserved in the release manifest.",
      minimumEligibility: [
        "Both manifest fragments are retained in immutable raw inputs and parsed with a versioned schema.",
        "The pre-registered field allowlist distinguishes transport configuration from security claims.",
        "The comparison does not infer a publish workflow, actor identity, or build provenance from a missing field.",
      ],
      permittedOutputIfEligible: "pre-registered categorical presence/state transition, never the raw configuration value.",
      nonInterpretation: "A manifest change is neither an attestation nor evidence that a release was built or published by an unauthorized actor.",
    },
    {
      deltaType: "verifiable_provenance_attestation_state_transition",
      candidateEvidence: "Release-specific, signed provenance or publish attestation with immutable transparency-log reference and verification result at or after release publication.",
      minimumEligibility: [
        "The attestation is cryptographically verified against the release artifact and stored with a stable transparency-log reference.",
        "The source repository and build instructions are linked by the attestation rather than inferred from a registry repository field.",
        "The collection time, verification tool version, and verification policy are pre-registered.",
      ],
      permittedOutputIfEligible: "verified-attestation-state category with verification policy identifier; never an actor, credential, certificate, or workflow value.",
      nonInterpretation: "npm provenance does not guarantee that a package contains no malicious code and must not be converted into a benign label.",
    },
    {
      deltaType: "release_mediation_or_publisher_authority_transition",
      candidateEvidence: "Registry-native, version-specific, historically retained publication-authority or trusted-publishing evidence with documented semantics.",
      minimumEligibility: [
        "The field’s registry semantics and historical retention guarantee are independently documented.",
        "The comparison source is version-specific and not a current package maintainer list or account profile.",
        "Identifier pseudonymization, ambiguity handling, and source-access rules are pre-registered before reading outcomes.",
      ],
      permittedOutputIfEligible: "pseudonymous transition class with a documented evidence-fidelity label.",
      nonInterpretation: "A publisher or mediation transition is a review candidate only; it must not be called an account takeover or incident without independent adjudication.",
    },
    {
      deltaType: "release_workflow_authority_transition",
      candidateEvidence: "Release-specific, commit-bound CI/CD workflow evidence linked to the exact source revision by verified provenance or an equivalently time-valid release record.",
      minimumEligibility: [
        "The workflow commit is bound to the release source by a pre-registered, auditable evidence chain.",
        "Both predecessor and selected workflow states are retrieved at their exact historical revisions.",
        "Public workflow absence remains unknown unless the source/repository linkage and retrieval scope are documented.",
      ],
      permittedOutputIfEligible: "pre-registered categorical workflow-authority transition, with an unobservable category distinct from unchanged.",
      nonInterpretation: "Workflow configuration alone does not reveal secrets, cloud scope, runner isolation, or malicious intent.",
    },
  ],
  futureBenchmarkHandling: {
    missingness: "Keep field-level not_eligible and not_applicable states. Never impute them, merge them into unchanged, or use them as outcome labels.",
    outcomeSeparation: "Freeze delta extraction and quality checks before joining future labels; retain the independently adjudicated outcome manifest as a separate source object.",
    grouping: "Assign release observations to the pre-registered related-family validation unit; do not split related family observations across evaluation partitions.",
    reporting: "Report eligibility counts, evidence-fidelity states, and exclusion reasons before any score, rank, effect, calibration, or uncertainty result.",
  },
  currentDecision: {
    observedDeltaValuesExtracted: 0,
    observedDeltasClassified: 0,
    authorityScoresComputed: 0,
    controlsCreated: 0,
    modelsFitted: 0,
    rankingsComputed: 0,
    predictiveMetricsComputed: 0,
    status: "blocked_pending_primary_control_frame_and_pre_registered_raw_evidence_collection",
  },
  methodContext: [
    {
      source: "Santos-Grueiro, On Good Authority",
      url: "https://arxiv.org/abs/2606.22593",
      permittedUse: "Supports predecessor-aware authority comparison as a review surface; the reported study does not authorize reuse of its trigger set, controls, or outcomes for this benchmark.",
    },
    {
      source: "npm provenance documentation",
      url: "https://docs.npmjs.com/generating-provenance-statements",
      permittedUse: "Defines provenance and publish attestations and states that provenance does not guarantee absence of malicious code.",
    },
    {
      source: "Open Source Insights npm provenance overview",
      url: "https://blog.deps.dev/npm-provenance/",
      permittedUse: "Describes provenance as a link between a package artifact, build system, and source code; no provider provenance data was accessed for this protocol.",
    },
  ],
  prohibitedInterpretations: [
    "This protocol does not extract, compare, hash, classify, or publish any raw authority-field value or observed delta.",
    "This protocol does not create a control population, benign label, release-authority score, effect estimate, rank, model, confidence interval, or predictive metric.",
    "Do not treat a registry metadata difference, provenance transition, publisher transition, or workflow transition as evidence of compromise or malicious code.",
    "Do not use current registry, maintainer, repository, workflow, VCS, download, dependency, or account state as a substitute for release-time evidence.",
  ],
};

await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ outputPath, deltaTypes: output.deltaOntology.length, observedDeltasClassified: output.currentDecision.observedDeltasClassified, controlsCreated: output.currentDecision.controlsCreated, modelsFitted: output.currentDecision.modelsFitted }, null, 2));
