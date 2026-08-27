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
    expect(names).toContain("node-ipc 2022");
    expect(names).toContain("@emcd-vue/auth 2026");
    expect(names).toContain("Mini Shai-Hulud atool 2026");
    expect(names).toContain("is 2025");
    expect(names).toContain("keyv 2026");
    expect(names).toContain("Lottie Player 2024");
    expect(names).toContain("Nx S1ngularity 2025");
    expect(names).toContain("country-currency-map 2025");
    expect(names).toContain("html-to-gutenberg 2026");
    expect(names).toContain("common-stack generate-plugin 2026");
  });

  it("marks the graph-attention experiment as blocked until prerequisites are met", () => {
    const hgat = getExperiments().find((experiment) => experiment.id === "hgat");
    expect(hgat?.status).toBe("blocked");
  });

  it("reconciles the temporal-feasibility card with the twenty-eight-record no-fit ledger", () => {
    const temporal = getExperiments().find((experiment) => experiment.id === "temporal-feasibility");
    expect(temporal?.evaluation).toContain("Twenty-eight package-event records");
    expect(temporal?.note).toContain("twenty-two campaign families");
    expect(temporal?.note).toContain("March 2022 node-ipc");
    expect(temporal?.note).toContain("shared Qix-related family");
    expect(temporal?.note).toContain("Debug/chalk");
    expect(temporal?.note).toContain("Lottie Player");
    expect(temporal?.note).toContain("Nx S1ngularity");
    expect(temporal?.note).toContain("country-currency-map");
    expect(temporal?.note).toContain("html-to-gutenberg");
    expect(temporal?.note).toContain("@common-stack/generate-plugin");
    expect(temporal?.note).toContain("remains non-independent");
    expect(temporal?.note).toContain("no cutoff-valid controls exist");
  });

  it("admits the separately bounded March 2022 node-ipc event only with its exact strict registry predecessor and no-inference safeguards", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/123_node_ipc_march_2022_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        packageName: "node-ipc",
        affectedVersions: ["10.1.1", "10.1.2"],
        earliestAffectedVersion: { version: "10.1.1", publishedUtc: "2022-03-07T11:03:59.179Z" },
        strictFeatureCutoffUtc: "2022-03-07T11:03:59.178Z",
        selectedPreEventVersion: "10.1.0",
        selectedPreEventVersionObjectRetained: true,
        proposedFamilyId: "node_ipc_march_2022_maintainer_protestware",
        distinctFromExistingNodeIpc2026Record: true,
      },
      zeroOutputsUntilReconstruction: { ledgerRows: 0, families: 0, validationUnits: 0, snapshots: 0, controls: 0, models: 0, predictiveMetrics: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("No historical installation, dependency reach, blast-radius, score, model, ranking, interval, calibration, or predictive metric is created.");
  });

  it("admits the bounded Nx S1ngularity event only with exact versions, the strict all-stream predecessor, and no-inference safeguards", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/129_nx_august_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "nx-2025-08-26",
        packageName: "nx",
        eventFamilyCandidate: "nx_s1ngularity_publish_token_compromise_2025",
        affectedVersions: ["21.5.0", "20.9.0", "20.10.0", "21.6.0", "20.11.0", "21.7.0", "21.8.0", "20.12.0"],
        earliestAffectedVersion: { version: "21.5.0", publishedUtc: "2025-08-26T22:32:25.482Z" },
        strictFeatureCutoffUtc: "2025-08-26T22:32:25.481Z",
        selectedPreEventVersion: "21.5.0-canary.20250826-af44608",
        selectedPreEventVersionObjectRetained: true,
        distinctFromExistingLedgerFamilies: true,
      },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Registry metadata establishes publication-time selection and retained-object availability only; it does not establish historical installations, downstream reach, blast radius, current maintainer state, or a causal effect.");
  });

  it("admits the bounded country-currency-map hijack only with its exact version, strict predecessor, and no-inference safeguards", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/131_country_currency_map_march_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "country-currency-map-2025-03-26",
        packageName: "country-currency-map",
        eventFamilyCandidate: "country_currency_map_crypto_package_hijack_2025",
        affectedVersions: ["2.1.8"],
        earliestAffectedVersion: { version: "2.1.8", publishedUtc: "2025-03-25T09:03:00.518Z" },
        strictFeatureCutoffUtc: "2025-03-25T09:03:00.517Z",
        selectedPreEventVersion: "2.1.7",
        selectedPreEventVersionObjectRetained: true,
        distinctFromExistingLedgerFamilies: true,
      },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Registry metadata establishes publication-time selection and retained-object availability only; it does not establish historical installations, downstream reach, blast radius, current maintainer state, or a causal effect.");
  });

  it("admits the bounded html-to-gutenberg hijack only with independently corroborated exact versions, a retained strict predecessor, and no-inference safeguards", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/133_html_to_gutenberg_may_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "html-to-gutenberg-2026-05-25",
        packageName: "html-to-gutenberg",
        eventFamilyCandidate: "html_to_gutenberg_vscode_task_hijack_2026",
        affectedVersions: ["4.2.11", "4.2.14"],
        earliestAffectedVersion: { version: "4.2.11", publishedUtc: "2026-05-25T19:19:47.408Z" },
        strictFeatureCutoffUtc: "2026-05-25T19:19:47.407Z",
        selectedPreEventVersion: "4.2.10",
        selectedPreEventVersionObjectRetained: true,
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "4.2.10", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Registry metadata establishes publication-time selection and retained-object availability only; it does not establish historical installations, downstream reach, blast radius, current maintainer state, or a causal effect.");
  });

  it("admits the bounded common-stack generate-plugin hijack only with the strict two-version source intersection, retained predecessor, and no-inference safeguards", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/136_common_stack_generate_plugin_may_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "common-stack-generate-plugin-2026-05-21",
        packageName: "@common-stack/generate-plugin",
        eventFamilyCandidate: "common_stack_generate_plugin_polinrider_hijack_2026",
        affectedVersions: ["9.0.2-alpha.21", "9.0.2-alpha.22"],
        affectedVersionScopeRule: "strict_two_version_intersection_of_independently_reviewed_sources_only",
        earliestAffectedVersion: { version: "9.0.2-alpha.21", publishedUtc: "2026-05-21T15:54:08.581Z" },
        strictFeatureCutoffUtc: "2026-05-21T15:54:08.580Z",
        selectedPreEventVersion: "9.0.2-alpha.18",
        selectedPreEventVersionObjectRetained: true,
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "9.0.2-alpha.18", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Registry metadata establishes publication-time selection and retained-object availability only; it does not establish historical installations, downstream reach, blast radius, current maintainer state, or a causal effect.");
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
    await expect(getDocument("incident-labels")).resolves.toMatchObject({ markdown: expect.stringContaining("28 package-event records in 22 incident families") });
  });

  it("preserves the generated direct-edge fidelity boundary and no-fit calibration result", async () => {
    const graph = await import("node:fs/promises").then((fs) => fs.readFile("research/67_cutoff_direct_dependency_graph_manifest.json", "utf8")).then(JSON.parse);
    const rangeResolution = await import("node:fs/promises").then((fs) => fs.readFile("research/70_cutoff_direct_dependency_range_resolution_manifest.json", "utf8")).then(JSON.parse);
    const rangeDiagnostic = await import("node:fs/promises").then((fs) => fs.readFile("research/71_direct_range_resolution_diagnostic.json", "utf8")).then(JSON.parse);
    const gate = await import("node:fs/promises").then((fs) => fs.readFile("research/66_temporal_baseline_and_calibration_gate.json", "utf8")).then(JSON.parse);
    expect(graph.summary).toMatchObject({ packageEventRecords: 28, exactSourceSnapshots: 26, unavailableSourceSnapshots: 2, declaredDirectEdges: 126, resolvedTargetVersions: 0, computedTransitiveReachValues: 0 });
    expect(graph.prohibitedInterpretations).toContain("This artifact is not a lockfile, a package-manager resolution, or a transitive dependency graph.");
    expect(rangeResolution.summary).toMatchObject({ inputDeclaredEdges: 126, resolvedIsolatedSemverRanges: 126, unresolvedTargetRanges: 0, computedTransitiveReachValues: 0 });
    expect(rangeResolution.prohibitedInterpretations).toContain("This artifact is not a package-lock, npm --before execution trace, or reproducible installation result.");
    expect(rangeDiagnostic).toMatchObject({ summary: { declaredDirectEdges: 126, isolatedCutoffSemverApproximations: 126, computedTransitiveReachValues: 0 } });
    expect(gate).toMatchObject({ strictPackageEventRecords: 28, adjudicatedIncidentFamilyCount: 22, exactPreEventSnapshots: 26, exactSnapshotIncidentFamilyCount: 21, calibrationInference: "blocked" });
    expect(gate.adjudicatedIncidentFamilies).toContain("colors_faker_protestware_2022");
    expect(gate.adjudicatedIncidentFamilies).toContain("node_ipc_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("node_ipc_march_2022_maintainer_protestware");
    expect(gate.adjudicatedIncidentFamilies).toContain("moika_dependency_confusion_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("shai_hulud_second_coming_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("mini_shai_hulud_atool_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("is_maintainer_compromise_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("keyv_cacheable_august_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("qix_npm_phishing_september_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("solana_web3_js_publish_access_compromise_2024");
    expect(gate.adjudicatedIncidentFamilies).toContain("lottie_player_npm_account_takeover_2024");
    expect(gate.adjudicatedIncidentFamilies).toContain("nx_s1ngularity_publish_token_compromise_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("country_currency_map_crypto_package_hijack_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("html_to_gutenberg_vscode_task_hijack_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("common_stack_generate_plugin_polinrider_hijack_2026");
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
    expect(manifest.summary).toMatchObject({ exactRootSnapshots: 26, reconstructedEdges: 760, unresolvedEdges: 0, maxObservedDepth: 3 });
    expect(manifest.prohibitedInterpretations).toContain("This graph is not a package-lock, npm install execution trace, or reproducible historical node_modules tree.");
    expect(diagnostic.summary).toMatchObject({ boundedEdges: 760, directDepthOneEdges: 126, depthTwoEdges: 281, depthThreeEdges: 353, globalReachValuesComputed: 0, predictiveMetricsComputed: 0 });
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
    expect(overlap.summary).toMatchObject({ primaryRecordsChecked: 28, exactAffectedVersionMembership: 11, packagePresentVersionsUnspecified: 3, packagePresentNoExactVersionMatch: 1, packageNotPresent: 13, newPrimaryLabelsCreated: 0, controlsCreated: 0 });
    expect(overlap.interpretation).toContain("no event time");
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "axios-2026-03-31")).toMatchObject({ positive_membership_status: "exact_affected_version_membership" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "node-ipc-2026-05-14")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "node-ipc-2022-03-07")).toMatchObject({ positive_membership_status: "package_present_no_exact_affected_version_match", permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "wenk-2025-11-24")).toMatchObject({ positive_membership_status: "package_present_versions_unspecified", permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "amapcn-2026-05-19")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["0.2.2", "0.3.2"], permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "is-2025-07-19")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["3.3.1", "5.0.0"], permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "keyv-2026-08-04")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["6.0.0"], permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "debug-2025-09-08")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["4.4.2"], permitted_use: "candidate_positive_membership_corroboration_only" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "solana-web3-js-2024-12-03")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", matching_versions: ["1.95.7"], permitted_use: "candidate_positive_membership_corroboration_only" });
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
      sourceInputs: { strictLedger: { recordCount: 28, familyCount: 22 } },
      validationUnits: { unitCount: 21 },
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
      input: { exactPreEventSourceSnapshots: 26 },
      summary: {
        exactPreEventSourceSnapshots: 26,
        predecessorAvailable: 26,
        repositoryDescriptorComparisonAvailable: 24,
        gitHeadComparisonAvailable: 18,
        publishConfigComparisonAvailable: 5,
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
      inputGate: { strictAvailabilityAudit: { observedAvailabilitySummary: { exactPreEventSourceSnapshots: 26, predecessorAvailable: 26, repositoryDescriptorComparisonAvailable: 24, gitHeadComparisonAvailable: 18, publishConfigComparisonAvailable: 5 } } },
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
      boundedAccessDecision: { strictPreEventVersionsEligibleForFutureScreen: 26, documentedMetadataOnlyVersionSpecificRetrievalPath: false, endpointGuessingPermitted: false, packagePayloadDownloadPermitted: false, installationPermitted: false, signatureVerificationRunPermitted: false },
      counts: { versionSpecificEndpointRequestsAttempted: 0, undocumentedEndpointsGuessed: 0, packagePayloadsDownloaded: 0, packagesInstalled: 0, attestationBundlesRetrieved: 0, signatureVerificationRuns: 0, attestationStatesClassified: 0, controlsCreated: 0, authorityScoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Do not infer that any strict pre-event version lacks an attestation because no metadata-only access path was established.");
  });

  it("retains the full ledger source-object census as current retention rather than historical package evidence", async () => {
    const census = await import("node:fs/promises").then((fs) => fs.readFile("research/98_full_ledger_source_object_retention_census.json", "utf8")).then(JSON.parse);
    expect(census).toMatchObject({
      executionStatus: "current_registry_retention_census_only_no_package_feature_or_outcome_analysis",
      summary: { incidentRecords: 28, incidentFamilies: 22, currentRegistryResponsesWithProvenance: 28, strictPreEventSourceObjectsRetained: 26, labelOnlyExceptions: 2, currentRetentionIsNotHistoricalEvidence: true },
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

  it("retains the future outcome-manifest sealing protocol as blinded and without outcomes or controls", async () => {
    const protocol = await import("node:fs/promises").then((fs) => fs.readFile("research/100_future_outcome_manifest_sealing_protocol.json", "utf8")).then(JSON.parse);
    expect(protocol).toMatchObject({
      executionStatus: "future_only_protocol_no_outcome_sources_contacted_rows_labels_controls_or_joins_created",
      protocolInputs: { relatednessProtocol: { futureValidationUnitCount: 21 } },
      currentDecision: { outcomeSourcesContacted: 0, sourceInventoryRecordsCreated: 0, candidateDocketsCreated: 0, adjudicatorDecisionsRecorded: 0, outcomeRowsCreated: 0, positiveOutcomeRowsCreated: 0, eligibleNonEventRowsCreated: 0, unknownOutcomeRowsCreated: 0, controlsCreated: 0, coverageRecordsCreated: 0, manifestRevisionsSealed: 0, featureOutcomeJoinsCreated: 0, temporalSplitsGenerated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(protocol.targetAndHorizonContract.targetVocabulary.unknown_outcome).toContain("not benign");
    expect(protocol.sealingAndBlindingWorkflow.blindingRules).toContain("Outcome adjudicators must not receive feature values, authority commitments, graph measures, workflow evidence, review-queue membership, controls, scores, ranks, or performance metrics.");
    expect(protocol.prohibitedInterpretations).toContain("Existing strict incident records remain independently adjudicated positive evidence only; they are not a closed-world outcome population or proof of horizon completeness.");
  });

  it("retains the public-safe aggregate-release policy as future-only and without released cells or results", async () => {
    const policy = await import("node:fs/promises").then((fs) => fs.readFile("research/101_future_public_safe_aggregate_release_policy.json", "utf8")).then(JSON.parse);
    expect(policy).toMatchObject({
      executionStatus: "future_only_policy_no_release_rows_labels_controls_aggregates_or_model_results_created",
      policyInputs: { groupedInferenceProtocol: { futureValidationUnitCount: 21 } },
      currentDecision: { releasePlansCreated: 0, releaseLedgerEntriesCreated: 0, sourceObjectsInspectedForRelease: 0, outcomeRowsReleased: 0, controlRowsReleased: 0, authorityValuesReleased: 0, aggregateCellsComputed: 0, aggregateCellsReleased: 0, smallCellReviewsPerformed: 0, differencingReviewsPerformed: 0, modelResultsReleased: 0, rankingsReleased: 0, uncertaintyIntervalsReleased: 0, predictiveMetricsReleased: 0 },
    });
    expect(policy.releaseClasses).toHaveLength(4);
    expect(policy.releaseClasses.find((releaseClass: { releaseClass: string }) => releaseClass.releaseClass === "P3_aggregate_benchmark_results")?.futureEligibility).toContain("Not enabled");
    expect(policy.disclosureSafeguards.smallCellAndCompositionControls).toContain("Treat any aggregate based on the current 28 positive records, 22 families, or 21 future validation units as non-releasable under P2 unless a later independent disclosure review establishes a valid broader eligible frame.");
    expect(policy.prohibitedInterpretations).toContain("The current policy version permits no P3 model-result release and no public row-level outcome, control, authority, feature, family, validation-unit, split, score, rank, interval, calibration, or metric disclosure.");
  });

  it("retains the future aggregate-plan parameter contract without thresholds, data access, or releases", async () => {
    const contract = await import("node:fs/promises").then((fs) => fs.readFile("research/102_future_aggregate_plan_parameter_sealing_contract.json", "utf8")).then(JSON.parse);
    expect(contract).toMatchObject({
      executionStatus: "future_only_contract_no_parameter_values_records_commitments_aggregates_or_releases_created",
      currentDecision: { secureParameterRecordsCreated: 0, parameterValuesSet: 0, parameterCommitmentManifestsCreated: 0, preInspectionAttestationsRecorded: 0, accessControlReviewsPerformed: 0, independentVerificationsPerformed: 0, amendmentsCreated: 0, protectedDataObjectsInspected: 0, aggregatePlansCreated: 0, aggregateCellsComputed: 0, aggregateCellsReleased: 0, outcomeRowsCreated: 0, controlsCreated: 0, authorityValuesCreated: 0, modelResultsCreated: 0, rankingsCreated: 0, uncertaintyIntervalsCreated: 0, predictiveMetricsCreated: 0 },
    });
    expect(contract.secureParameterRecordSchema.parameterFieldsSecureOnly).toHaveLength(12);
    expect(contract.publicSafeCommitmentManifestSchema.permittedFields).toHaveLength(14);
    expect(contract.activationGate.prohibitedActivationFallbacks).toContain("Do not choose or tune a parameter after inspecting an aggregate, cell, suppression outcome, class prevalence, review queue, score, rank, interval, calibration, or model result.");
    expect(contract.prohibitedInterpretations).toContain("No current policy permits a P3 model-result release, and no current artifact creates or reveals a threshold, plan, aggregate, row, label, control, authority value, score, rank, interval, calibration, or predictive metric.");
  });

  it("excludes the corroborated crossenv candidate when the strict pre-event source object is not retained", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/103_crossenv_typosquatting_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_retained_pre_event_source_object",
      candidate: { recordId: "crossenv-2017-07-19", packageName: "crossenv", independentlyReportedAffectedVersion: "6.1.1", affectedVersionPublishedUtc: "2017-07-19T06:49:52.698Z", strictFeatureCutoffUtc: "2017-07-19T06:49:52.697Z", timeMapSelectedPreEventVersion: "6.0.7" },
      corroboration: { officialRegistry: { affectedVersionObjectRetained: false, selectedPreEventVersionObjectRetained: false } },
      currentDecision: { primaryLedgerRecordsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.corroboration.officialRegistry.retainedVersionObjectKeys).toEqual(["0.0.1-security", "0.0.2-security", "1.0.0", "1.0.1"]);
    expect(assessment.strictExclusionReason.consequence).toContain("Do not add crossenv to the current primary ledger");
    expect(assessment.prohibitedInterpretations).toContain("This exclusion does not dispute the independently corroborated crossenv incident evidence or convert the candidate into a benign, safe, unchanged, no-known-event, or control row.");
  });

  it("excludes the related flatmap-stream candidate without creating a new family or validation unit", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/104_flatmap_stream_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_official_affected_release_timestamp_or_retained_pre_event_source_object",
      candidate: { recordId: "flatmap-stream-2018-10-05", packageName: "flatmap-stream", independentlyReportedAffectedVersion: "0.1.1", relatedExistingFamily: "event_stream_2018", officialAffectedVersionTimeUtc: null, strictFeatureCutoffUtc: null },
      corroboration: { officialRegistry: { affectedVersionTimeUtc: null, blockedVersionTimeRetention: { "0.1.0": null, "0.1.1": null, "0.1.2": null }, blockedVersionObjectRetention: { "0.1.0": false, "0.1.1": false, "0.1.2": false }, retainedVersionObjectKeys: ["0.0.1-security"] } },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, primaryLedgerValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.strictExclusionReason.consequence).toContain("Do not add flatmap-stream to the current primary ledger");
    expect(assessment.prohibitedInterpretations).toContain("The documented relationship to event-stream is relatedness evidence only; it does not establish a new independent campaign family, validation unit, causal pathway, or campaign-complete census.");
  });

  it("excludes peacenotwar when the advisory is all-version scoped and no strict pre-event source object exists", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/106_peacenotwar_protestware_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_strict_pre_event_source_object_and_no_exact_version_specific_advisory_target",
      candidate: { recordId: "peacenotwar-2022-03-08", packageName: "peacenotwar", advisoryAffectedVersionScope: "all_versions", registryFirstVersion: "9.1.1", registryFirstVersionPublishedUtc: "2022-03-08T16:38:45.767Z", timeMapSelectedPreEventVersion: null },
      corroboration: { snykAdvisory: { advisoryId: "SNYK-JS-PEACENOTWAR-2426724" }, officialRegistry: { firstRegistryVersion: "9.1.1", selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: false } },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.strictExclusionReason.consequence).toContain("Do not add peacenotwar to the primary ledger");
    expect(assessment.prohibitedInterpretations).toContain("The all-versions advisory scope cannot be collapsed into a finite exact release target without a source that explicitly identifies the candidate version set.");
  });

  it("excludes the independently corroborated Noblox 2021 package-name screen when no finite exact affected version is documented", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/125_noblox_js_proxy_october_2021_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_independently_corroborated_finite_exact_affected_version_target",
      candidate: { recordId: "noblox-js-proxy-2021-10-26", packageName: "noblox.js-proxy", independentlyCorroboratedPackageName: true, independentlyCorroboratedAffectedVersions: null },
      corroboration: { officialRegistry: { boundedMetadataOnly: true, httpStatus: 200, retainedVersionObjectKeys: ["0.0.1-security"], inspectedForSourceObjectSelection: false } },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, calibrationResultsCreated: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.strictExclusionReason.consequence).toContain("Do not add a primary ledger record");
    expect(assessment.prohibitedInterpretations).toContain("The official registry response is used only to document bounded metadata availability; it cannot infer a finite affected version, historical installation, source snapshot, dependency graph, reach, or blast radius.");
  });

  it("admits the bounded Debug record only with independent finite-version corroboration and a retained strict predecessor", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/108_debug_september_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: { recordId: "debug-2025-09-08", packageName: "debug", affectedVersions: ["4.4.2"], eventFamilyCandidate: "qix_npm_phishing_september_2025", affectedVersionPublishedUtc: "2025-09-08T13:12:39.973Z", strictFeatureCutoffUtc: "2025-09-08T13:12:39.972Z", timeMapSelectedPreEventVersion: "4.4.1" },
      strictEligibility: { finiteExactAffectedVersionIndependentlyCorroborated: true, officialAffectedVersionTimestampRetained: true, selectedPreEventVersion: "4.4.1", selectedPreEventVersionObjectRetained: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.nextDecisionBoundary).toContain("all ledger-dependent artifacts are updated atomically");
    expect(assessment.prohibitedInterpretations).toContain("An eligible source-object screen alone does not create a cutoff-valid control population, benign labels, historical installation trace, dependency reach, blast-radius estimate, score, model, ranking, interval, calibration result, or predictive metric.");
  });

  it("admits the bounded Solana web3.js record only with independent finite-version corroboration and the all-stream retained source object", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/110_solana_web3_js_december_2024_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: { recordId: "solana-web3-js-2024-12-03", packageName: "@solana/web3.js", affectedVersions: ["1.95.6", "1.95.7"], eventFamilyCandidate: "solana_web3_js_publish_access_compromise_2024", eventStartUtc: "2024-12-03T15:10:07.122Z", strictFeatureCutoffUtc: "2024-12-03T15:10:07.121Z", timeMapSelectedPreEventVersion: "2.1.0-canary-20241203100809" },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "2.1.0-canary-20241203100809", selectedPreEventVersionObjectRetained: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.corroboration.officialRegistry.affectedVersionObjectsRetained).toEqual({ "1.95.6": false, "1.95.7": false });
    expect(assessment.nextDecisionBoundary).toContain("all ledger-dependent artifacts are updated atomically");
    expect(assessment.prohibitedInterpretations).toContain("No later package, repository, maintainer, workflow, lockfile, download, payload, installation, or dependency-reach state may be substituted for the selected strict pre-event source object.");
  });

  it("admits the bounded Lottie Player account-takeover record only with exact independent versions and a retained strict predecessor", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/127_lottie_player_october_2024_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: { recordId: "lottie-player-2024-10-30", packageName: "@lottiefiles/lottie-player", eventFamilyCandidate: "lottie_player_npm_account_takeover_2024", affectedVersions: ["2.0.5", "2.0.6", "2.0.7"], earliestAffectedVersion: { version: "2.0.5", publishedUtc: "2024-10-30T20:12:15.375Z" }, strictFeatureCutoffUtc: "2024-10-30T20:12:15.374Z", selectedPreEventVersion: "2.0.4", selectedPreEventVersionObjectRetained: true, distinctFromExistingLedgerFamilies: true },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "2.0.4", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, calibrationResultsCreated: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.corroboration.officialRegistry.retainedAffectedVersionObjects).toEqual({ "2.0.5": false, "2.0.6": false, "2.0.7": false });
    expect(assessment.nextDecisionBoundary).toContain("atomically update the strict ledger and every dependent artifact");
    expect(assessment.prohibitedInterpretations).toContain("Registry metadata establishes publication-time selection and retained-object availability only; it does not establish historical installations, downstream reach, blast radius, current maintainer state, or a causal effect.");
  });

  it("admits the two related colors and faker records with strict registry cutoffs but no controls or model outputs", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/105_colors_faker_protestware_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_two_related_records_to_existing_primary_temporal_ledger_under_single_new_related_family",
      eventFamily: "colors_faker_protestware_2022",
      labelClass: "confirmed_malicious_publication",
      candidates: [
        { recordId: "colors-2022-01-08", packageName: "colors", affectedVersions: ["1.4.44-liberty-2", "1.4.1", "1.4.2"], eventStartUtc: "2022-01-08T04:24:16.448Z", sourceSelection: { selectedVersion: "1.4.0", exactSourceObjectRetained: true } },
        { recordId: "faker-2022-01-05", packageName: "faker", affectedVersions: ["6.6.6"], eventStartUtc: "2022-01-05T01:38:36.409Z", sourceSelection: { selectedVersion: "5.5.3", exactSourceObjectRetained: true } },
      ],
      currentDecision: { primaryLedgerRecordsAdded: 2, primaryLedgerFamiliesAdded: 1, primaryLedgerValidationUnitsAdded: 1, exactPreEventSourceSnapshotsExpected: 2, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.relatednessRule).toContain("cannot create two independent validation units");
    expect(assessment.prohibitedInterpretations).toContain("The two records are related and count as one future validation unit, not two independent observations.");
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

  it("excludes eslint-plugin-prettier despite a retained predecessor when package-specific independent corroboration is absent", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/119_eslint_plugin_prettier_july_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_independently_corroborated_package_specific_incident_source",
      candidate: { packageName: "eslint-plugin-prettier", affectedVersions: ["4.2.2", "4.2.3"], selectedPreEventVersion: "5.5.1", selectedPreEventVersionObjectRetained: true, requiredFamilyId: "eslint_config_prettier_compromise_2025" },
      evidenceGate: { independentlyCorroboratedPackageSpecificIncidentSource: false },
      zeroOutputs: { ledgerRows: 0, families: 0, validationUnits: 0, snapshots: 0, controls: 0, models: 0, predictiveMetrics: 0 },
    });
  });
});
