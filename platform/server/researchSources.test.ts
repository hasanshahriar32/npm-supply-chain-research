import { describe, expect, it } from "vitest";
import { getDocument, getDocuments, getExperiments, getIncidents, getLiterature, getSourceSnapshot } from "./researchSources";

describe("repository-backed research sources", () => {
  it("loads the required literature matrix from research/11_literature_matrix.csv", async () => {
    const studies = await getLiterature();
    expect(studies.length).toBeGreaterThanOrEqual(15);
    expect(studies.find((study) => study.study_id === "L15")?.study).toContain("Current project repository");
  });

  it("loads current benchmark snapshot values from the source manifest", async () => {
    const snapshot = await getSourceSnapshot();
    expect(snapshot.packages).toBe(25228);
    expect(snapshot.dependencyEdges).toBe(121885);
    expect(snapshot.maintainers).toBe(12217);
    expect(snapshot.workflowChecks).toBe(21523);
  });

  it("includes the documented Shai-Hulud and Axios incident anchors", () => {
    const names = getIncidents().map((incident) => incident.name);
    expect(names).toContain("Shai-Hulud");
    expect(names).toContain("Axios");
    expect(names).toContain("node-ipc 2026");
    expect(names).toContain("@emcd-vue/auth 2026");
    expect(names).toContain("Mini Shai-Hulud atool 2026");
    expect(names).toContain("is 2025");
    expect(names).toContain("keyv 2026");
  });

  it("marks the graph-attention experiment as blocked until prerequisites are met", () => {
    const hgat = getExperiments().find((experiment) => experiment.id === "hgat");
    expect(hgat?.status).toBe("blocked");
  });

  it("reconciles the temporal-feasibility card with the fourteen-record no-fit ledger", () => {
    const temporal = getExperiments().find((experiment) => experiment.id === "temporal-feasibility");
    expect(temporal?.evaluation).toContain("Fourteen package-event records");
    expect(temporal?.note).toContain("ten campaign families");
    expect(temporal?.note).toContain("not asserted statistically independent");
    expect(temporal?.note).toContain("no cutoff-valid controls exist");
  });

  it("serves the completed temporal reconstruction and adjudication artifacts in governed workspace sections", async () => {
    const documents = await getDocuments();
    expect(documents.find((document) => document.slug === "gap-analysis")?.sourceFile).toBe("68_temporal_reconstruction_and_baseline_results.md");
    expect(documents.find((document) => document.slug === "methodology")?.sourceFile).toBe("50_gap_resolution_study_protocol.md");
    expect(documents.find((document) => document.slug === "incident-labels")?.sourceFile).toBe("69_temporal_incident_label_adjudication.md");
    expect(documents.find((document) => document.slug === "experiment-results")?.sourceFile).toBe("68_temporal_reconstruction_and_baseline_results.md");
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ title: "Gap Analysis" });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("no predictive model has been fitted") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("Provider-backed control-frame assessment") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("Control-frame contract and public snapshot access assessment") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("Figshare replication package") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("GitHub’s public malware-advisory path") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("npm-follower archive") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("SupplyTGN supplies a useful") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("Original Sin of npm") });
    await expect(getDocument("incident-labels")).resolves.toMatchObject({ markdown: expect.stringContaining("fourteen package-event records") });
  });

  it("preserves the generated direct-edge fidelity boundary and no-fit calibration result", async () => {
    const graph = await import("node:fs/promises").then((fs) => fs.readFile("research/67_cutoff_direct_dependency_graph_manifest.json", "utf8")).then(JSON.parse);
    const rangeResolution = await import("node:fs/promises").then((fs) => fs.readFile("research/70_cutoff_direct_dependency_range_resolution_manifest.json", "utf8")).then(JSON.parse);
    const rangeDiagnostic = await import("node:fs/promises").then((fs) => fs.readFile("research/71_direct_range_resolution_diagnostic.json", "utf8")).then(JSON.parse);
    const gate = await import("node:fs/promises").then((fs) => fs.readFile("research/66_temporal_baseline_and_calibration_gate.json", "utf8")).then(JSON.parse);
    expect(graph.summary).toMatchObject({ packageEventRecords: 14, exactSourceSnapshots: 12, unavailableSourceSnapshots: 2, declaredDirectEdges: 29, resolvedTargetVersions: 0, computedTransitiveReachValues: 0 });
    expect(graph.prohibitedInterpretations).toContain("This artifact is not a lockfile, a package-manager resolution, or a transitive dependency graph.");
    expect(rangeResolution.summary).toMatchObject({ inputDeclaredEdges: 29, resolvedIsolatedSemverRanges: 29, unresolvedTargetRanges: 0, computedTransitiveReachValues: 0 });
    expect(rangeResolution.prohibitedInterpretations).toContain("This artifact is not a package-lock, npm --before execution trace, or reproducible installation result.");
    expect(rangeDiagnostic).toMatchObject({ summary: { declaredDirectEdges: 29, isolatedCutoffSemverApproximations: 29, computedTransitiveReachValues: 0 } });
    expect(gate).toMatchObject({ strictPackageEventRecords: 14, adjudicatedIncidentFamilyCount: 10, exactPreEventSnapshots: 12, exactSnapshotIncidentFamilyCount: 9, calibrationInference: "blocked" });
    expect(gate.adjudicatedIncidentFamilies).toContain("node_ipc_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("moika_dependency_confusion_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("shai_hulud_second_coming_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("mini_shai_hulud_atool_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("is_maintainer_compromise_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("keyv_cacheable_august_2026");
    expect(gate.blockingConditions).toContain("No cutoff-valid, independently adjudicated control population is available.");
  });

  it("records the selectively inspected resolver archive without treating its monolithic relation payload as ingested graph data", async () => {
    const fs = await import("node:fs/promises");
    const inventory = JSON.parse(await fs.readFile("research/72_chrono_resolution_archive_inventory.json", "utf8"));
    const schema = await fs.readFile("research/72_chrono_resolution_schema_relations.sql", "utf8");
    expect(inventory.zip64).toMatchObject({ totalEntries: "4" });
    expect(inventory.entries.find((entry: { name: string }) => entry.name === "data-relations.sql")).toMatchObject({ compressedSize: "10228591413", uncompressedSize: "138731381476" });
    expect(inventory.conclusion).toBe("Central-directory metadata only. No archive member payload was downloaded or executed.");
    expect(schema).toContain("dependency_version public.semver");
    expect(schema).toContain("interval_start timestamp without time zone");
  });

  it("retains no partial relation rows after the bounded monolithic-stream timeout", async () => {
    const fs = await import("node:fs/promises");
    const attempt = JSON.parse(await fs.readFile("research/73_chrono_resolution_streaming_attempt.json", "utf8"));
    expect(attempt).toMatchObject({
      result: "incomplete_timeout_no_valid_candidate_artifact",
      memberCompressedBytes: 10228591413,
      compressedBytesReceivedBeforeTimeout: 783198932,
      percentOfCompressedMemberReceived: 7.6569,
      candidateRowsRetained: 0,
    });
    expect(attempt.nextDataGate).toContain("bulk-compute environment");
  });

  it("preserves the bounded recursive registry graph as a sensitivity artifact rather than a reach or predictive result", async () => {
    const fs = await import("node:fs/promises");
    const manifest = JSON.parse(await fs.readFile("research/74_bounded_recursive_registry_semver_graph_manifest.json", "utf8"));
    const diagnostic = JSON.parse(await fs.readFile("research/75_bounded_recursive_registry_graph_diagnostic.json", "utf8"));
    expect(manifest.summary).toMatchObject({ exactRootSnapshots: 12, reconstructedEdges: 64, unresolvedEdges: 0, maxObservedDepth: 3 });
    expect(manifest.prohibitedInterpretations).toContain("This graph is not a package-lock, npm install execution trace, or reproducible historical node_modules tree.");
    expect(diagnostic.summary).toMatchObject({ boundedEdges: 64, directDepthOneEdges: 29, depthTwoEdges: 18, depthThreeEdges: 17, globalReachValuesComputed: 0, predictiveMetricsComputed: 0 });
    expect(diagnostic.interpretation).toContain("not historical installed-tree size");
  });

  it("keeps the explicit-label release corpus separate from a primary future-compromise control frame", async () => {
    const fs = await import("node:fs/promises");
    const provenance = JSON.parse(await fs.readFile("research/77_amalfi_release_sensitivity_diagnostics.json", "utf8"));
    const gate = JSON.parse(await fs.readFile("research/78_amalfi_release_sensitivity_gate.json", "utf8"));
    expect(provenance.corpus).toMatchObject({ explicitLabelRows: 1790, maliciousRows: 643, benignRows: 1147, distinctPackages: 444 });
    expect(gate.summary.labelCounts).toMatchObject({ malicious: { retainedRegistryVersionObjects: 9, versionNotRetained: 634 }, benign: { retainedRegistryVersionObjects: 1093, versionNotRetained: 54 } });
    expect(gate.decision.primaryFutureCompromiseControlFrame).toBe("blocked");
    expect(gate.prohibitedInterpretations).toContain("Do not call the benign rows generic no-known-event controls.");
  });

  it("uses the DataDog manifest only as positive-membership corroboration", async () => {
    const fs = await import("node:fs/promises");
    const overlap = JSON.parse(await fs.readFile("research/80_datadog_positive_membership_overlap.json", "utf8"));
    expect(overlap.summary).toMatchObject({ primaryRecordsChecked: 14, exactAffectedVersionMembership: 5, packagePresentVersionsUnspecified: 2, packageNotPresent: 7, newPrimaryLabelsCreated: 0, controlsCreated: 0 });
    expect(overlap.interpretation).toContain("no event time");
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "axios-2026-03-31")).toMatchObject({ positive_membership_status: "exact_affected_version_membership" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "node-ipc-2026-05-14")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "wenk-2025-11-24")).toMatchObject({ positive_membership_status: "package_present_versions_unspecified", permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "amapcn-2026-05-19")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["0.2.2", "0.3.2"], permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "is-2025-07-19")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["3.3.1", "5.0.0"], permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "keyv-2026-08-04")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["6.0.0"], permitted_use: "candidate_positive_membership_corroboration_only" });
  });

  it("retains the provider-backed control-frame assessment as an exclusion rather than creating inferred controls", async () => {
    const probe = await import("node:fs/promises").then((fs) => fs.readFile("research/81_provider_control_frame_probe.json", "utf8")).then(JSON.parse);
    expect(probe).toMatchObject({
      candidate: { provider: "Google Open Source Insights / deps.dev", dataset: "bigquery-public-data.deps_dev_v1" },
      accessProbe: { credentialsUsed: false, httpStatus: 401 },
      controlFrameDecision: "excluded",
      controlsCreated: 0,
    });
    expect(probe.blockingConditions).toContain("The documented advisory relation covers disclosed vulnerabilities rather than a closed-world malicious-publication or compromise event target.");
  });

  it("records a required temporal control-frame contract and excludes unmatched public population sources", async () => {
    const contract = await import("node:fs/promises").then((fs) => fs.readFile("research/83_control_frame_contract_and_access_assessment.md", "utf8"));
    expect(contract).toContain("zero control observations created");
    expect(contract).toContain("NPM Registry Dataset 2025 (GitHub Only)");
    expect(contract).toContain("22.3 GB compressed");
    expect(contract).toContain("No companion closed-world malicious-publication or compromise coverage source");
    expect(contract).toContain("redirected to Google sign-in");
    expect(contract).toContain("Libraries.io public metadata");
    expect(contract).toContain("zero valid controls");
  });

  it("retains the bounded Figshare detector benchmark as a release-classification lead rather than temporal controls", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/85_figshare_npm_benchmark_control_frame_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      controlFrameDecision: "excluded",
      controlsCreated: 0,
      boundedMetadataObservations: {
        malwareTimeCsv: { rows: 6420, timestampsNonblankAfterNormalization: 6149, timestampsBlankAfterNormalization: 271 },
        selectedBenignPackages: { rows: 1000, perRowTimestampProvided: false, observationHorizonProvided: false },
      },
    });
    expect(assessment.blockingConditions).toContain("The inspected selected-benign list has package/version identifiers but no per-row timestamp, collection cutoff, or observation horizon.");
    expect(assessment.prohibitedInterpretations).toContain("Do not call the selected benign strings cutoff-valid temporal controls.");
  });

  it("retains the GitHub malware-advisory path as positive provenance rather than temporal controls", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/86_github_advisory_database_malware_path_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({ controlFrameDecision: "excluded", controlsCreated: 0, primaryTemporalLabelsCreated: 0, candidate: { format: "OSV advisory records", supportedEcosystem: "npm" } });
    expect(assessment.blockingConditions).toContain("Absence from an advisory record cannot be interpreted as benign, uncompromised, or no-known-event.");
    expect(assessment.prohibitedInterpretations).toContain("Do not derive benign controls from advisory absence.");
  });

  it("retains npm-follower as a historical-population lead rather than an accessible temporal control source", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/87_npm_follower_population_access_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      controlFrameDecision: "excluded",
      controlsCreated: 0,
      boundedAccessScreen: { compactDataReleaseFound: false, filteredExportFound: false, queryApiFound: false, rowAddressableHistoricalPackageVersionSnapshotFound: false, dataRowsRetrieved: 0 },
    });
    expect(assessment.blockingConditions).toContain("No compact, reproducible filtered export, query API, or row-addressable historical package-version snapshot was documented on the public access path.");
    expect(assessment.prohibitedInterpretations).toContain("Do not treat npm-follower’s existence as current access to a control population.");
  });

  it("retains SupplyTGN as a PyPI/OSV methodology reference rather than npm control data", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/88_supplytgn_methodology_transfer_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({ npmControlFrameDecision: "excluded", npmRowsCreated: 0, controlsCreated: 0, candidate: { documentedEcosystem: "PyPI/OSV" } });
    expect(assessment.blockingConditions).toContain("The disclosed benchmark population is PyPI/OSV component-cutoff instances, not npm package versions.");
    expect(assessment.prohibitedInterpretations).toContain("Do not transfer reported PyPI/OSV performance results to npm.");
  });

  it("retains Original Sin of npm as vulnerability-lifecycle context rather than a temporal compromise-control frame", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/89_original_sin_npm_control_frame_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      controlFrameDecision: "excluded",
      controlsCreated: 0,
      npmRowsCreated: 0,
      candidate: { documentedOutcome: "Disclosed OSV/NVD vulnerability propagation and lifecycle information." },
    });
    expect(assessment.blockingConditions).toContain("The documented target is vulnerability propagation, not closed-world malicious-publication or maintainer-compromise coverage.");
    expect(assessment.prohibitedInterpretations).toContain("Do not treat vulnerability absence as a benign or uncompromised npm control label.");
  });

  it("retains the authorized provider-access specification as a non-executed future contract rather than control data", async () => {
    const specification = await import("node:fs/promises").then((fs) => fs.readFile("research/90_authorized_npm_control_frame_access_specification.json", "utf8")).then(JSON.parse);
    expect(specification).toMatchObject({
      executionStatus: "not_executed_no_authorized_provider_access_or_target_matched_outcome_manifest",
      currentDecision: { controlFrameStatus: "blocked", controlsCreated: 0, packageVersionRowsRetrieved: 0, positiveOutcomeRowsJoined: 0, modelMetricsCreated: 0 },
      sourceContext: { populationProvider: "Google Open Source Insights deps.dev BigQuery public dataset" },
    });
    expect(specification.independentOutcomeJoinSpecification.nonEventRule).toContain("unknown rather than benign");
    expect(specification.prohibitedActions).toContain("Do not derive controls from advisory absence, registry survival, source omission, current package state, or no-known-event assertions.");
  });

  it("retains campaign-relatedness rules as a non-executed grouped-inference safeguard", async () => {
    const protocol = await import("node:fs/promises").then((fs) => fs.readFile("research/94_campaign_relatedness_and_grouped_inference_protocol.json", "utf8")).then(JSON.parse);
    expect(protocol).toMatchObject({
      executionStatus: "protocol_only_no_control_frame_or_model_eligible_dataset",
      sourceInputs: { strictLedger: { recordCount: 14, familyCount: 10 } },
      validationUnits: { unitCount: 9 },
      currentDecision: { controlsCreated: 0, modelsFitted: 0, temporalSplitsGenerated: 0, uncertaintyIntervalsComputed: 0, rankingsComputed: 0, predictiveMetricsComputed: 0, status: "blocked_pending_control_frame_and_model_eligibility" },
    });
    expect(protocol.documentedCrossFamilyRelatedness).toContainEqual(expect.objectContaining({
      sourceFamilyId: "mini_shai_hulud_atool_2026",
      relatedFamilyId: "keyv_cacheable_august_2026",
      requiredValidationClusterId: "mini_shai_hulud_payload_lineage_cluster",
    }));
    expect(protocol.futureEligibleOnlyRules.resamplingRules).toContain("If uncertainty is eligible, resample validation units rather than individual package-event rows.");
    expect(protocol.prohibitedInterpretations).toContain("This protocol is not a model, a model evaluation, a confidence interval, or a predictive result.");
  });

  it("retains strict release-authority metadata as an availability audit rather than a feature or scoring result", async () => {
    const audit = await import("node:fs/promises").then((fs) => fs.readFile("research/95_release_authority_metadata_availability_audit.json", "utf8")).then(JSON.parse);
    expect(audit).toMatchObject({
      executionStatus: "availability_audit_only_no_feature_values_deltas_scores_or_models",
      input: { exactPreEventSourceSnapshots: 12 },
      summary: {
        exactPreEventSourceSnapshots: 12,
        predecessorAvailable: 12,
        repositoryDescriptorComparisonAvailable: 11,
        gitHeadComparisonAvailable: 9,
        publishConfigComparisonAvailable: 0,
        featureValuesExtracted: 0,
        deltasClassified: 0,
        releaseAuthorityScoresComputed: 0,
        controlsCreated: 0,
        modelsFitted: 0,
        predictiveMetricsComputed: 0,
      },
    });
    expect(audit.scope.nonUseOfCurrentState).toContain("current dist-tags");
    expect(audit.prohibitedInterpretations).toContain("Do not use repository, gitHead, publishConfig, dist, or embedded-maintainer availability as a release-authority score.");
  });

  it("retains future release-authority delta semantics as a non-executed eligibility contract", async () => {
    const protocol = await import("node:fs/promises").then((fs) => fs.readFile("research/96_release_authority_delta_semantics_protocol.json", "utf8")).then(JSON.parse);
    expect(protocol).toMatchObject({
      executionStatus: "protocol_only_no_metadata_values_compared_or_deltas_classified",
      inputGate: { strictAvailabilityAudit: { observedAvailabilitySummary: { exactPreEventSourceSnapshots: 12, predecessorAvailable: 12, repositoryDescriptorComparisonAvailable: 11, gitHeadComparisonAvailable: 9, publishConfigComparisonAvailable: 0 } } },
      currentDecision: { observedDeltaValuesExtracted: 0, observedDeltasClassified: 0, authorityScoresComputed: 0, controlsCreated: 0, modelsFitted: 0, rankingsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(protocol.deltaOntology).toHaveLength(6);
    expect(protocol.eligibilityDecisionVocabulary.prohibitedFallback).toContain("unchanged, safe, benign, or no-known-event");
    expect(protocol.prohibitedInterpretations).toContain("This protocol does not create a control population, benign label, release-authority score, effect estimate, rank, model, confidence interval, or predictive metric.");
  });

  it("retains official npm provenance access as a metadata-only access exclusion rather than an attestation-state result", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/97_official_npm_provenance_attestation_access_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "metadata_only_version_specific_attestation_access_not_established",
      boundedAccessDecision: { strictPreEventVersionsEligibleForFutureScreen: 12, documentedMetadataOnlyVersionSpecificRetrievalPath: false, endpointGuessingPermitted: false, packagePayloadDownloadPermitted: false, installationPermitted: false, signatureVerificationRunPermitted: false },
      counts: { versionSpecificEndpointRequestsAttempted: 0, undocumentedEndpointsGuessed: 0, packagePayloadsDownloaded: 0, packagesInstalled: 0, attestationBundlesRetrieved: 0, signatureVerificationRuns: 0, attestationStatesClassified: 0, controlsCreated: 0, authorityScoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Do not infer that any strict pre-event version lacks an attestation because no metadata-only access path was established.");
  });

  it("retains the full ledger source-object census as current retention rather than historical package evidence", async () => {
    const census = await import("node:fs/promises").then((fs) => fs.readFile("research/98_full_ledger_source_object_retention_census.json", "utf8")).then(JSON.parse);
    expect(census).toMatchObject({
      executionStatus: "current_registry_retention_census_only_no_package_feature_or_outcome_analysis",
      summary: { incidentRecords: 14, incidentFamilies: 10, currentRegistryResponsesWithProvenance: 14, strictPreEventSourceObjectsRetained: 12, labelOnlyExceptions: 2, currentRetentionIsNotHistoricalEvidence: true },
      exceptionCategories: { timeMapSelectionButStrictObjectRetentionFailure: ["plain-crypto-js-2026-03-31"], noPreCutoffVersionSelectionInCurrentResponse: ["emcd-vue-auth-2026-06-01"] },
      currentDecision: { packageMetadataValuesExtracted: 0, maintainerOrPublisherValuesExtracted: 0, repositoryOrWorkflowValuesExtracted: 0, provenanceOrAttestationStatesClassified: 0, packageFeaturesDerived: 0, controlsCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(census.prohibitedInterpretations).toContain("Do not treat a current registry retention state as a historical package, maintainer, repository, provenance, workflow, or dependency-state observation.");
  });

  it("retains the release-authority raw-evidence capture contract as future-only and opaque", async () => {
    const contract = await import("node:fs/promises").then((fs) => fs.readFile("research/99_release_authority_raw_evidence_capture_contract.json", "utf8")).then(JSON.parse);
    expect(contract).toMatchObject({
      executionStatus: "future_only_contract_no_raw_evidence_retrieved_stored_canonicalized_or_compared",
      protocolInput: { deltaTypes: ["repository_link_discontinuity", "source_revision_reference_discontinuity", "release_manifest_publication_intent_discontinuity", "verifiable_provenance_attestation_state_transition", "release_mediation_or_publisher_authority_transition", "release_workflow_authority_transition"] },
      currentDecision: { rawEvidenceObjectsRetrieved: 0, rawAuthorityValuesStored: 0, rawAuthorityValuesPublished: 0, sourceEndpointsContacted: 0, packagePayloadsDownloaded: 0, packageInstallationsRun: 0, canonicalizationRunsExecuted: 0, opaqueCommitmentsRecorded: 0, sourceTimeValidityDecisionsMade: 0, observedDeltasClassified: 0, controlsCreated: 0, authorityScoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(contract.fieldCollectionSchemas).toHaveLength(6);
    expect(contract.captureManifestSchema.forbiddenFields).toContain("Outcome labels, incident labels, control labels, model scores, ranks, or metric values in the collection manifest.");
    expect(contract.prohibitedInterpretations).toContain("This contract is not a raw-evidence collection, a current-state audit, a delta comparison, or an authority assessment.");
  });

  it("admits only the bounded and independently corroborated is maintainer-compromise record", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/91_is_package_compromise_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_one_bounded_package_event_record",
      candidateRecord: { recordId: "is-2025-07-19", packageName: "is", affectedVersions: ["3.3.1", "5.0.0"], eventFamily: "is_maintainer_compromise_2025", eventStartUtc: "2025-07-19T11:40:30.778Z" },
      corroboration: { openssfRecordId: "MAL-2025-6020", preEventLatestVersion: "3.3.0" },
    });
    expect(assessment.prohibitedInterpretations).toContain("This artifact does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, or blast-radius estimate.");
  });

  it("admits only the bounded keyv campaign-family record without claiming cross-campaign independence", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/92_keyv_compromise_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_one_bounded_campaign_family_record_without_cross_campaign_independence_claim",
      candidateRecord: { recordId: "keyv-2026-08-04", packageName: "keyv", affectedVersions: ["6.0.0"], eventFamily: "keyv_cacheable_august_2026", eventStartUtc: "2026-08-04T09:35:00.763Z" },
      corroboration: { openssfRecordId: "MAL-2026-11524", preEventLatestVersion: "6.0.0-rc.1" },
    });
    expect(assessment.familyRelationship.crossCampaign).toContain("no statistical independence");
    expect(assessment.prohibitedInterpretations).toContain("This artifact does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, or blast-radius estimate.");
  });

  it("admits only the bounded and cross-source corroborated wenk Shai-Hulud record", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/82_shai_hulud_second_coming_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_one_bounded_package_event_record",
      candidateRecord: { recordId: "wenk-2025-11-24", packageName: "wenk", affectedVersions: ["1.0.9", "1.0.10"], eventFamily: "shai_hulud_second_coming_2025", eventStartUtc: "2025-11-24T10:06:12.376Z" },
      corroboration: { frozenWizIocRow: "wenk,= 1.0.10 || = 1.0.9", preEventLatestVersion: "1.0.8" },
    });
    expect(assessment.prohibitedInterpretations).toContain("This artifact does not create a control population or benign labels.");
  });

  it("admits only the bounded and cross-source corroborated amapcn Mini Shai-Hulud record", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/84_mini_shai_hulud_atool_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_one_bounded_package_event_record",
      candidateRecord: { recordId: "amapcn-2026-05-19", packageName: "amapcn", affectedVersions: ["0.2.2", "0.3.2"], eventFamily: "mini_shai_hulud_atool_2026", eventStartUtc: "2026-05-19T01:56:40.925Z" },
      corroboration: { openssfRecordId: "MAL-2026-4127", preEventLatestVersion: "0.1.2" },
    });
    expect(assessment.prohibitedInterpretations).toContain("This artifact does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, or blast-radius estimate.");
  });
});
