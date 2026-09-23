import { describe, expect, it } from "vitest";
import { getDocument, getDocuments, getExperiments, getIncidents, getLiterature, getQueueAudit, getSourceSnapshot } from "./researchSources";

describe("repository-backed research sources", () => {
  it("loads the required literature matrix from research/11_literature_matrix.csv", async () => {
    const studies = await getLiterature();
    expect(studies.length).toBeGreaterThanOrEqual(15);
    expect(studies.find((study) => study.study_id === "L15")?.study).toContain("Current project repository");
  });

  it("links candidate notes to assessments in the queue audit", async () => {
    const rows = await getQueueAudit();
    expect(rows.length).toBeGreaterThanOrEqual(20);
    expect(rows.find((row) => row.noteFile === "161_cloudplatform_search_may_2026_candidate_screen_notes.md")).toMatchObject({ assessmentFile: "178_cloudplatform_search_may_2026_candidate_assessment.json", disposition: "excluded", ledgerRecords: 0 });
    expect(rows.some((row) => row.disposition === "awaiting assessment")).toBe(false);
  });

  it("publishes Atomic Arch as contextual evidence without admitting it to the npm primary ledger", async () => {
    const documents = await getDocuments();
    expect(documents.find((document) => document.slug === "atomic-arch-case-study")?.sourceFile).toBe("172_atomic_arch_aur_cross_ecosystem_study.md");
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/173_atomic_arch_aur_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment.decision).toBe("retain_as_governed_cross_ecosystem_context_exclude_from_npm_primary_temporal_ledger");
    expect(assessment.currentDecision.primaryLedgerRecordsAdded).toBe(0);
    expect(assessment.strictEligibility.eligibleForFutureMultiregistryPropagationLayer).toBe(true);
  });

  it("excludes noblox.js-proxy-server when the exact malicious version lacks independent corroboration", async () => {
    const documents = await getDocuments();
    expect(documents.find((document) => document.slug === "noblox-js-proxy-server-screen")?.sourceFile).toBe("174_noblox_js_proxy_server_january_2024_candidate_screen_notes.md");
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/175_noblox_js_proxy_server_january_2024_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_independent_exact_version_corroboration",
      candidate: {
        packageName: "noblox.js-proxy-server",
        affectedVersionsReportedByPrimaryCandidateSource: ["4.15.4"],
        strictFeatureCutoffUtc: "2024-01-17T03:39:58.206Z",
        selectedPreEventVersion: "4.15.3",
        selectedPreEventVersionObjectRetained: true
      },
      strictEligibility: {
        finiteExactAffectedVersionsIndependentlyCorroborated: false,
        eligibleForGovernedReconstruction: false
      },
      currentDecision: { primaryLedgerRecordsAdded: 0, predictiveMetricsComputed: 0 }
    });
  });

  it("excludes cloudplatform-search when independent sources have no exact-version intersection", async () => {
    const documents = await getDocuments();
    expect(documents.find((document) => document.slug === "cloudplatform-search-screen")?.sourceFile).toBe("161_cloudplatform_search_may_2026_candidate_screen_notes.md");
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/178_cloudplatform_search_may_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_finite_exact_version_intersection",
      candidate: {
        packageName: "@cloudplatform-single-spa/search",
        sourceVersionClaims: { microsoft: ["100.100.100"], snyk: ["99.99.99"] }
      },
      strictEligibility: {
        independentlyCorroboratedPackageName: true,
        finiteExactAffectedVersionsIndependentlyCorroborated: false,
        sourceVersionIntersection: [],
        officialRegistryMetadataRequested: false,
        eligibleForGovernedReconstruction: false
      },
      currentDecision: { primaryLedgerRecordsAdded: 0, predictiveMetricsComputed: 0 }
    });
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
    expect(names).toContain("Bitwarden CLI 2026");
    expect(names).toContain("React Native country-select 2026");
    expect(names).toContain("rand-user-agent 2025");
    expect(names).toContain("AsyncAPI generator 2026");
    expect(names).toContain("dYdX v4 client 2026");
    expect(names).toContain("dYdX Solo 2022");
  });

  it("marks the graph-attention experiment as blocked until prerequisites are met", () => {
    const hgat = getExperiments().find((experiment) => experiment.id === "hgat");
    expect(hgat?.status).toBe("blocked");
  });

  it("reconciles the temporal-feasibility card with the forty-six-record no-fit ledger", () => {
    const temporal = getExperiments().find((experiment) => experiment.id === "temporal-feasibility");
    expect(temporal?.evaluation).toContain("Forty-seven package-event records");
    expect(temporal?.note).toContain("thirty-one campaign families");
    expect(temporal?.note).toContain("OpenSearch JavaScript client");
    expect(temporal?.note).toContain("bounded Qix-family members");
    expect(temporal?.note).toContain("simple-swizzle");
    expect(temporal?.note).toContain("OpenSearch JavaScript client");
    expect(temporal?.note).toContain("Nx S1ngularity");
    expect(temporal?.note).toContain("country-currency-map");
    expect(temporal?.note).toContain("html-to-gutenberg");
    expect(temporal?.note).toContain("@common-stack/generate-plugin");
    expect(temporal?.note).toContain("Bitwarden CLI");
    expect(temporal?.note).toContain("React Native country-select");
    expect(temporal?.note).toContain("rand-user-agent");
    expect(temporal?.note).toContain("AsyncAPI generator");
    expect(temporal?.note).toContain("dYdX v4 client");
    expect(temporal?.note).toContain("family-grouped only where sources explicitly name their Mini Shai-Hulud context");
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

  it("excludes the duplicate country-currency-map screening while retaining its exact timing provenance", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/131_country_currency_map_march_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_duplicate_existing_country_currency_map_event_record",
      candidate: {
        recordId: "country-currency-map-2025-03-26",
        packageName: "country-currency-map",
        eventFamilyCandidate: "country_currency_map_crypto_package_hijack_2025",
        affectedVersions: ["2.1.8"],
        earliestAffectedVersion: { version: "2.1.8", publishedUtc: "2025-03-25T09:03:00.518Z" },
        strictFeatureCutoffUtc: "2025-03-25T09:03:00.517Z",
        selectedPreEventVersion: "2.1.7",
        selectedPreEventVersionObjectRetained: true,
        distinctFromExistingLedgerFamilies: false,
        duplicateOfExistingLedgerRecord: "country-currency-map-2025-03-25",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: false, duplicateExistingLedgerRecord: true },
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

  it("admits the bounded Bitwarden CLI event only with independently corroborated exact release evidence, a retained strict predecessor, and no expansion of the documented Checkmarx context", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/140_bitwarden_cli_april_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "bitwarden-cli-2026-04-22",
        packageName: "@bitwarden/cli",
        eventFamilyCandidate: "bitwarden_cli_checkmarx_supply_chain_2026",
        affectedVersions: ["2026.4.0"],
        earliestAffectedVersion: { version: "2026.4.0", publishedUtc: "2026-04-22T21:22:59.021Z" },
        strictFeatureCutoffUtc: "2026-04-22T21:22:59.020Z",
        selectedPreEventVersion: "2026.3.0",
        selectedPreEventVersionObjectRetained: true,
        documentedIncidentContext: "related_to_the_broader_Checkmarx_supply_chain_incident",
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "2026.3.0", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The documented broader Checkmarx incident context does not authorize expansion into additional package records, assignment to an existing governed family, or a statistical-independence claim.");
  });

  it("admits the bounded React Native country-select event only with an independently corroborated exact version, a retained strict predecessor, and no expansion of same-day context", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/142_react_native_country_select_march_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "react-native-country-select-2026-03-16",
        packageName: "react-native-country-select",
        eventFamilyCandidate: "react_native_shared_publisher_glassworm_march_2026",
        affectedVersions: ["0.3.91"],
        affectedVersionScopeRule: "single_version_intersection_of_independently_reviewed_sources_only",
        earliestAffectedVersion: { version: "0.3.91", publishedUtc: "2026-03-16T10:54:18.512Z" },
        strictFeatureCutoffUtc: "2026-03-16T10:54:18.511Z",
        selectedPreEventVersion: "0.3.9",
        selectedPreEventVersionObjectRetained: true,
        documentedIncidentContext: "same_day_shared_publisher_context_with_an_unadmitted_package_not_expanded_here",
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "0.3.9", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The same-day shared-publisher context does not authorize expansion into another package record, assignment to an existing governed family, campaign completeness, or a statistical-independence claim.");
  });

  it("admits the bounded rand-user-agent event only with its independently corroborated three-version intersection, retained strict predecessor, and no-inference safeguards", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/144_rand_user_agent_may_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "rand-user-agent-2025-05-05",
        packageName: "rand-user-agent",
        eventFamilyCandidate: "rand_user_agent_unauthorized_npm_publications_2025",
        affectedVersions: ["2.0.83", "2.0.84", "1.0.110"],
        affectedVersionScopeRule: "strict_three_version_intersection_of_independently_reviewed_sources_only",
        earliestAffectedVersion: { version: "2.0.83", publishedUtc: "2025-04-26T15:25:00.992Z" },
        strictFeatureCutoffUtc: "2025-04-26T15:25:00.991Z",
        selectedPreEventVersion: "2.0.82",
        selectedPreEventVersionObjectRetained: true,
        documentedIncidentContext: "unauthorized_npm_publications_after_last_legitimate_project_release",
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "2.0.82", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The documented unauthorized-publication context does not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, or a statistical-independence claim.");
  });

  it("admits the bounded AsyncAPI generator event only with its independently corroborated exact version, retained strict predecessor, and no expansion of the documented AsyncAPI incident", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/148_asyncapi_generator_july_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "asyncapi-generator-2026-07-14",
        packageName: "@asyncapi/generator",
        eventFamilyCandidate: "asyncapi_github_actions_release_pipeline_compromise_2026",
        affectedVersions: ["3.3.1"],
        affectedVersionScopeRule: "single_version_intersection_of_independently_reviewed_sources_only",
        earliestAffectedVersion: { version: "3.3.1", publishedUtc: "2026-07-14T07:10:48.853Z" },
        strictFeatureCutoffUtc: "2026-07-14T07:10:48.852Z",
        selectedPreEventVersion: "3.3.0",
        selectedPreEventVersionObjectRetained: true,
        documentedIncidentContext: "github_actions_release_pipeline_compromise_with_unresolved_attribution",
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "3.3.0", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The documented unresolved attribution and reported tooling overlap do not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, or a statistical-independence claim.");
  });

  it("admits the bounded dYdX v4 client event only with its independently corroborated four-version intersection, retained strict predecessor, and no cross-ecosystem expansion", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/150_dydx_v4_client_february_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "dydx-v4-client-2026-02-06",
        packageName: "@dydxprotocol/v4-client-js",
        eventFamilyCandidate: "dydx_v4_client_npm_pypi_maintainer_compromise_2026",
        affectedVersions: ["3.4.1", "1.22.1", "1.15.2", "1.0.31"],
        affectedVersionScopeRule: "strict_four_version_intersection_of_independently_reviewed_sources_only",
        earliestAffectedVersion: { version: "1.0.31", publishedUtc: "2026-01-27T13:22:18.888Z" },
        strictFeatureCutoffUtc: "2026-01-27T13:22:18.887Z",
        selectedPreEventVersion: "3.4.0",
        selectedPreEventVersionObjectRetained: true,
        documentedIncidentContext: "npm_and_pypi_package_event_with_unconfirmed_maintainer_compromise_attribution",
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "3.4.0", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The unconfirmed maintainer-compromise attribution and cross-ecosystem context do not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, or a statistical-independence claim.");
  });

  it("admits the bounded dYdX Solo event only with its independently corroborated two-version intersection, retained strict predecessor, and no companion-package expansion", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/152_dydx_solo_september_2022_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction",
      candidate: {
        recordId: "dydx-solo-2022-09-23",
        packageName: "@dydxprotocol/solo",
        eventFamilyCandidate: "dydx_solo_september_2022_npm_account_compromise",
        affectedVersions: ["0.41.1", "0.41.2"],
        affectedVersionScopeRule: "strict_two_version_intersection_of_independently_reviewed_sources_only",
        earliestAffectedVersion: { version: "0.41.1", publishedUtc: "2022-09-23T10:39:42.987Z" },
        strictFeatureCutoffUtc: "2022-09-23T10:39:42.986Z",
        selectedPreEventVersion: "0.41.0",
        selectedPreEventVersionObjectRetained: true,
        documentedIncidentContext: "dydx_owned_npm_package_event_with_mend_reported_account_compromise",
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: "0.41.0", selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The documented dYdX package context and temporal difference from the governed 2026 dYdX record do not authorize expansion into additional package records, assignment to an existing governed family, campaign completeness, actor linkage, or a statistical-independence claim.");
  });

  it("excludes the bounded Joyfill lead as a new independent family when independent reporting documents PolinRider relatedness before registry access", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/146_joyfill_components_july_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_new_independent_primary_family_due_to_documented_polinrider_relatedness",
      candidate: {
        recordId: "joyfill-components-2026-07-28",
        packageName: "@joyfill/components",
        sourceOneAffectedVersions: ["4.0.0-rc24-2773-beta.4", "4.0.0-rc24-2773-beta.5", "4.0.0-rc24-2773-beta.6"],
        sourceTwoAffectedVersions: ["4.0.0-rc24-2773-beta.4"],
        affectedVersionIntersection: ["4.0.0-rc24-2773-beta.4"],
        documentedRelatedCampaign: "PolinRider",
        existingRelatedGovernedFamily: "common_stack_generate_plugin_polinrider_hijack_2026",
        distinctFromExistingLedgerFamilies: false,
      },
      registryBoundary: { officialRegistryRequestAttempted: false, strictFeatureCutoffUtc: null, selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: null },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.strictExclusionReason.consequence).toContain("Do not add @joyfill/components as a new independent primary-ledger family or future validation unit");
    expect(assessment.prohibitedInterpretations).toContain("The documented PolinRider relation does not establish campaign completeness, a complete related-package set, a current publisher state, or a statistical-independence claim.");
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
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("Joyfill July 2026 relatedness exclusion") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("AsyncAPI generator July 2026 GitHub Actions release-pipeline-compromise admission") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("dYdX v4 client January–February 2026 cross-ecosystem malicious-publication admission") });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("dYdX Solo September 2022 npm account-compromise admission") });
    await expect(getDocument("incident-labels")).resolves.toMatchObject({ markdown: expect.stringContaining("35 records in 28 families") });
  });

  it("admits TanStack History only as an explicitly documented Mini Shai-Hulud family member", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/155_tanstack_history_may_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
      candidate: { packageName: "@tanstack/history", affectedVersions: ["1.161.9", "1.161.12"], strictFeatureCutoffUtc: "2026-05-11T19:20:39.564Z", selectedPreEventVersion: "1.161.6", selectedPreEventVersionObjectRetained: true, existingFamily: "mini_shai_hulud_atool_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("excludes @ctrl/tinycolor before registry reconstruction when no finite exact version set is independently corroborated", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/157_ctrl_tinycolor_september_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_independently_corroborated_finite_exact_affected_version_set",
      candidate: { packageName: "@ctrl/tinycolor", affectedVersionIntersection: [], officialRegistryMetadataRequested: false, strictFeatureCutoffUtc: null, selectedPreEventVersion: null, familyTreatment: "unadjudicated_from_shared_campaign_name_alone" },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: false, eligibleForGovernedReconstruction: false },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Do not infer a package version, range, event cutoff, pre-event source object, or registry retention state from package-level reporting.");
  });

  it("preserves the generated direct-edge fidelity boundary and no-fit calibration result", async () => {
    const graph = await import("node:fs/promises").then((fs) => fs.readFile("research/67_cutoff_direct_dependency_graph_manifest.json", "utf8")).then(JSON.parse);
    const rangeResolution = await import("node:fs/promises").then((fs) => fs.readFile("research/70_cutoff_direct_dependency_range_resolution_manifest.json", "utf8")).then(JSON.parse);
    const rangeDiagnostic = await import("node:fs/promises").then((fs) => fs.readFile("research/71_direct_range_resolution_diagnostic.json", "utf8")).then(JSON.parse);
    const gate = await import("node:fs/promises").then((fs) => fs.readFile("research/66_temporal_baseline_and_calibration_gate.json", "utf8")).then(JSON.parse);
    expect(graph.summary).toMatchObject({ packageEventRecords: 47, exactSourceSnapshots: 45, unavailableSourceSnapshots: 2, declaredDirectEdges: 258, resolvedTargetVersions: 0, computedTransitiveReachValues: 0 });
    expect(graph.prohibitedInterpretations).toContain("This artifact is not a lockfile, a package-manager resolution, or a transitive dependency graph.");
    expect(rangeResolution.summary).toMatchObject({ inputDeclaredEdges: 258, resolvedIsolatedSemverRanges: 254, unresolvedTargetRanges: 4, computedTransitiveReachValues: 0 });
    expect(rangeResolution.prohibitedInterpretations).toContain("This artifact is not a package-lock, npm --before execution trace, or reproducible installation result.");
    expect(rangeDiagnostic).toMatchObject({ summary: { declaredDirectEdges: 258, isolatedCutoffSemverApproximations: 254, unresolvedDirectRanges: 4, computedTransitiveReachValues: 0 } });
    expect(gate).toMatchObject({ strictPackageEventRecords: 47, adjudicatedIncidentFamilyCount: 31, exactPreEventSnapshots: 45, exactSnapshotIncidentFamilyCount: 30, calibrationInference: "blocked" });
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
    expect(gate.adjudicatedIncidentFamilies).toContain("bitwarden_cli_checkmarx_supply_chain_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("react_native_shared_publisher_glassworm_march_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("rand_user_agent_unauthorized_npm_publications_2025");
    expect(gate.adjudicatedIncidentFamilies).toContain("asyncapi_github_actions_release_pipeline_compromise_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("dydx_v4_client_npm_pypi_maintainer_compromise_2026");
    expect(gate.adjudicatedIncidentFamilies).toContain("dydx_solo_september_2022_npm_account_compromise");
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
    expect(manifest.summary).toMatchObject({ exactRootSnapshots: 45, reconstructedEdges: 1848, unresolvedEdges: 7, maxObservedDepth: 3 });
    expect(manifest.prohibitedInterpretations).toContain("This graph is not a package-lock, npm install execution trace, or reproducible historical node_modules tree.");
    expect(diagnostic.summary).toMatchObject({ boundedEdges: 1848, directDepthOneEdges: 258, depthTwoEdges: 657, depthThreeEdges: 933, globalReachValuesComputed: 0, predictiveMetricsComputed: 0 });
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
    expect(overlap.summary).toMatchObject({ primaryRecordsChecked: 47, exactAffectedVersionMembership: 26, packagePresentVersionsUnspecified: 4, packagePresentNoExactVersionMatch: 1, packageNotPresent: 16, newPrimaryLabelsCreated: 0, controlsCreated: 0 });
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
      sourceInputs: { strictLedger: { recordCount: 47, familyCount: 31 } },
      validationUnits: { unitCount: 30 },
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
      input: { exactPreEventSourceSnapshots: 45 },
      summary: {
        exactPreEventSourceSnapshots: 45,
        predecessorAvailable: 44,
        repositoryDescriptorComparisonAvailable: 42,
        gitHeadComparisonAvailable: 34,
        publishConfigComparisonAvailable: 11,
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
      inputGate: { strictAvailabilityAudit: { observedAvailabilitySummary: { exactPreEventSourceSnapshots: 45, predecessorAvailable: 44, repositoryDescriptorComparisonAvailable: 42, gitHeadComparisonAvailable: 34, publishConfigComparisonAvailable: 11 } } },
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
      boundedAccessDecision: { strictPreEventVersionsEligibleForFutureScreen: 45, documentedMetadataOnlyVersionSpecificRetrievalPath: false, endpointGuessingPermitted: false, packagePayloadDownloadPermitted: false, installationPermitted: false, signatureVerificationRunPermitted: false },
      counts: { versionSpecificEndpointRequestsAttempted: 0, undocumentedEndpointsGuessed: 0, packagePayloadsDownloaded: 0, packagesInstalled: 0, attestationBundlesRetrieved: 0, signatureVerificationRuns: 0, attestationStatesClassified: 0, controlsCreated: 0, authorityScoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("Do not infer that any strict pre-event version lacks an attestation because no metadata-only access path was established.");
  });

  it("retains the full ledger source-object census as current retention rather than historical package evidence", async () => {
    const census = await import("node:fs/promises").then((fs) => fs.readFile("research/98_full_ledger_source_object_retention_census.json", "utf8")).then(JSON.parse);
    expect(census).toMatchObject({
      executionStatus: "current_registry_retention_census_only_no_package_feature_or_outcome_analysis",
      summary: { incidentRecords: 47, incidentFamilies: 31, currentRegistryResponsesWithProvenance: 47, strictPreEventSourceObjectsRetained: 45, labelOnlyExceptions: 2, currentRetentionIsNotHistoricalEvidence: true },
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
      protocolInputs: { relatednessProtocol: { futureValidationUnitCount: 30 } },
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
      policyInputs: { groupedInferenceProtocol: { futureValidationUnitCount: 30 } },
      currentDecision: { releasePlansCreated: 0, releaseLedgerEntriesCreated: 0, sourceObjectsInspectedForRelease: 0, outcomeRowsReleased: 0, controlRowsReleased: 0, authorityValuesReleased: 0, aggregateCellsComputed: 0, aggregateCellsReleased: 0, smallCellReviewsPerformed: 0, differencingReviewsPerformed: 0, modelResultsReleased: 0, rankingsReleased: 0, uncertaintyIntervalsReleased: 0, predictiveMetricsReleased: 0 },
    });
    expect(policy.releaseClasses).toHaveLength(4);
    expect(policy.releaseClasses.find((releaseClass: { releaseClass: string }) => releaseClass.releaseClass === "P3_aggregate_benchmark_results")?.futureEligibility).toContain("Not enabled");
    expect(policy.disclosureSafeguards.smallCellAndCompositionControls).toContain("Treat any aggregate based on the current 47 positive records, 31 families, or 30 future validation units as non-releasable under P2 unless a later independent disclosure review establishes a valid broader eligible frame.");
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

  it("admits got-fetch as a bounded existing eslint-config-prettier-family member after relatedness adjudication", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/154_got_fetch_july_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "eligible_for_governed_primary_temporal_ledger_reconstruction_as_existing_family_member",
      candidate: { recordId: "got-fetch-2025-07-17", packageName: "got-fetch", eventFamilyCandidate: "eslint_config_prettier_compromise_2025", affectedVersions: ["5.1.11", "5.1.12"], earliestAffectedVersion: { version: "5.1.11", publishedUtc: "2025-07-17T17:28:28.289Z" }, strictFeatureCutoffUtc: "2025-07-17T17:28:28.288Z", selectedPreEventVersion: "6.0.2", selectedPreEventVersionObjectRetained: true },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, relatednessAdjudicated: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.sourceProvenance).toMatchObject({ bleepingComputer: "https://www.bleepingcomputer.com/news/security/popular-npm-linter-packages-hijacked-via-phishing-to-drop-malware/", stepSecurity: "https://www.stepsecurity.io/blog/supply-chain-security-alert-eslint-config-prettier-package-shows-signs-of-compromise" });
    expect(assessment.prohibitedInterpretations).toContain("No cutoff-valid control population, benign label, score, model, rank, interval, calibration result, or predictive metric is created.");
  });

  it("excludes the independently corroborated sbx-mask candidate when the strict cutoff has no retained pre-event source object", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/138_sbx_mask_march_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
      candidate: {
        recordId: "sbx-mask-2026-03-18",
        packageName: "sbx-mask",
        eventFamilyCandidate: "sbx_mask_march_2026_maintainer_compromise",
        affectedVersions: ["1.0.0", "1.0.1", "1.0.2"],
        earliestAffectedVersion: { version: "1.0.0", publishedUtc: "2026-03-19T14:46:00.636Z" },
        strictFeatureCutoffUtc: "2026-03-19T14:46:00.635Z",
        selectedPreEventVersion: null,
        selectedPreEventVersionObjectRetained: false,
        distinctFromExistingLedgerFamilies: "not_asserted_related_to_any_governed_family",
      },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: false, eligibleForGovernedReconstruction: false },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, isolatedSemverApproximationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, benignLabelsCreated: 0, historicalInstallTracesCreated: 0, reachOrBlastRadiusValuesCreated: 0, scoresComputed: 0, modelsFitted: 0, rankingsComputed: 0, uncertaintyIntervalsComputed: 0, calibrationResultsCreated: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.corroboration.officialRegistry.retainedVersionObjectKeys).toEqual(["0.0.1-security"]);
    expect(assessment.nextDecisionBoundary).toContain("cannot enter the strict ledger");
  });

  it("admits the bounded Red Hat Chrome record only with exact corroboration, retained cutoff source, and existing-family treatment", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/163_redhat_cloud_services_chrome_june_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
      candidate: { recordId: "redhat-cloud-services-chrome-2026-06-01", packageName: "@redhat-cloud-services/chrome", affectedVersions: ["2.3.1", "2.3.2"], earliestAffectedVersion: { version: "2.3.1", publishedUtc: "2026-06-01T10:54:42.121Z" }, strictFeatureCutoffUtc: "2026-06-01T10:54:42.120Z", selectedPreEventVersion: "2.3.0", selectedPreEventVersionObjectRetained: true, existingFamily: "mini_shai_hulud_atool_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("excludes the corroborated t-in-one candidate when no strict pre-event source object is retained", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/164_t_in_one_add_application_may_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
      candidate: { recordId: "t-in-one-add-application-2026-05-29", packageName: "@t-in-one/add_application", affectedVersions: ["5.7.1"], earliestAffectedVersion: { version: "5.7.1", publishedUtc: "2026-05-29T09:01:56.660Z" }, strictFeatureCutoffUtc: "2026-05-29T09:01:56.659Z", selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: false, documentedRelatedFamily: "moika_dependency_confusion_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: false, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: false },
      zeroOutputs: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The missing strict pre-event source object does not convert the candidate into a benign, safe, unchanged, no-known-event, or control row.");
  });

  it("admits the bounded Mastra Core record only with exact corroboration, a retained cutoff source, and distinct-family treatment", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/165_mastra_core_june_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_record_in_a_distinct_mastra_scope_compromise_family",
      candidate: { recordId: "mastra-core-2026-06-17", packageName: "@mastra/core", affectedVersions: ["1.42.1"], earliestAffectedVersion: { version: "1.42.1", publishedUtc: "2026-06-17T01:15:13.011Z" }, strictFeatureCutoffUtc: "2026-06-17T01:15:13.010Z", selectedPreEventVersion: "0.0.0-caleb-channels-on-lease-20260616160652", selectedPreEventVersionObjectRetained: true, eventFamily: "mastra_scope_easy_day_js_compromise_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("admits bounded easy-day-js only as a documented Mastra-family member without an additional validation unit", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/166_easy_day_js_june_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_row_in_existing_mastra_scope_compromise_family_without_creating_an_independent_validation_unit",
      candidate: { recordId: "easy-day-js-2026-06-17", packageName: "easy-day-js", affectedVersions: ["1.11.22"], earliestAffectedVersion: { version: "1.11.22", publishedUtc: "2026-06-17T01:01:33.087Z" }, strictFeatureCutoffUtc: "2026-06-17T01:01:33.086Z", selectedPreEventVersion: "1.11.21", selectedPreEventVersionObjectRetained: true, existingFamily: "mastra_scope_easy_day_js_compromise_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("excludes echarts-for-react before registry reconstruction when independent finite exact versions disagree", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/167_echarts_for_react_may_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_independently_corroborated_finite_exact_affected_version_intersection",
      candidate: { recordId: "echarts-for-react-2026-05-19", packageName: "echarts-for-react", stepSecurityObservedVersion: "3.0.7", gitLabAdvisoryAffectedVersions: ["3.1.7", "3.2.7"], exactAffectedVersionIntersection: [], officialRegistryMetadataRequested: false, strictFeatureCutoffUtc: null, selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: false, campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      evidenceGate: { independentlyCorroboratedPackageSpecificIncidentSource: true, independentlyCorroboratedFiniteExactAffectedVersionIntersection: false, officialRegistryMetadataInspected: false, eligibleForGovernedReconstruction: false },
      zeroOutputs: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
    expect(assessment.prohibitedInterpretations).toContain("The Mini Shai-Hulud event context cannot be used to substitute an affected version set from another package or source.");
  });

  it("admits the bounded node-ipc May 2026 record only with exact corroboration, retained cutoff source, and distinct-family treatment", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/168_node_ipc_may_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_record_in_a_distinct_node_ipc_may_2026_maintainer_account_compromise_family",
      candidate: { recordId: "node-ipc-2026-05-14", packageName: "node-ipc", affectedVersions: ["9.1.6", "9.2.3", "12.0.1"], earliestAffectedVersion: { version: "12.0.1", publishedUtc: "2026-05-14T14:25:30.311Z" }, strictFeatureCutoffUtc: "2026-05-14T14:25:30.310Z", selectedPreEventVersion: "12.0.0", selectedPreEventVersionObjectRetained: true, eventFamily: "node_ipc_may_2026_maintainer_account_compromise", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("admits bounded Red Hat Compliance Client only as a documented Mini Shai-Hulud-family member without an additional validation unit", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/169_redhat_compliance_client_june_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
      candidate: { recordId: "redhat-cloud-services-compliance-client-2026-06-01", packageName: "@redhat-cloud-services/compliance-client", affectedVersions: ["4.0.3", "4.0.4"], earliestAffectedVersion: { version: "4.0.3", publishedUtc: "2026-06-01T10:55:21.357Z" }, strictFeatureCutoffUtc: "2026-06-01T10:55:21.356Z", selectedPreEventVersion: "4.0.2", selectedPreEventVersionObjectRetained: true, existingFamily: "mini_shai_hulud_atool_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("admits bounded Red Hat Config Manager Client only as a documented Mini Shai-Hulud-family member without an additional validation unit", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/170_redhat_config_manager_client_june_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
      candidate: { recordId: "redhat-cloud-services-config-manager-client-2026-06-01", packageName: "@redhat-cloud-services/config-manager-client", affectedVersions: ["5.0.4", "5.0.5"], earliestAffectedVersion: { version: "5.0.4", publishedUtc: "2026-06-01T10:54:25.934Z" }, strictFeatureCutoffUtc: "2026-06-01T10:54:25.933Z", selectedPreEventVersion: "5.0.3", selectedPreEventVersionObjectRetained: true, existingFamily: "mini_shai_hulud_atool_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("excludes peacenotwar when the advisory is all-versions scoped and no strict predecessor exists", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/106_peacenotwar_protestware_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_strict_pre_event_source_object_and_no_exact_version_specific_advisory_target",
      candidate: { recordId: "peacenotwar-2022-03-08", packageName: "peacenotwar", advisoryAffectedVersionScope: "all_versions", registryFirstVersion: "9.1.1", registryFirstVersionPublishedUtc: "2022-03-08T16:38:45.767Z", strictFeatureCutoffUtc: "2022-03-08T16:38:45.766Z", timeMapSelectedPreEventVersion: null },
      strictExclusionReason: { observedState: "The advisory scope is all peacenotwar versions and the incident report supplies a March 8 publication context, but no inspected independent source identifies a finite event-specific peacenotwar version. The official registry's first retained publication is 9.1.1, so no strictly earlier source version exists to reconstruct an exact pre-event snapshot." },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
  });

  it("excludes flatmap-stream when no official affected timestamp or retained strict pre-event object exists", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/104_flatmap_stream_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_official_affected_release_timestamp_or_retained_pre_event_source_object",
      candidate: { recordId: "flatmap-stream-2018-10-05", packageName: "flatmap-stream", independentlyReportedAffectedVersion: "0.1.1", relatedExistingFamily: "event_stream_2018", officialAffectedVersionTimeUtc: null, strictFeatureCutoffUtc: null },
      strictExclusionReason: { observedState: "The bounded current registry response lacks a 0.1.1 time-map entry, lacks all 0.1.x time-map entries, and retains no historically relevant 0.1.x version object. A later security-holder object does not supply event-time or pre-event source evidence. Therefore no official exact cutoff or pre-event source-object selection can be reconstructed." },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, primaryLedgerValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
  });

  it("excludes crossenv when the selected strict pre-event version object is not retained", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/103_crossenv_typosquatting_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_retained_pre_event_source_object",
      candidate: { recordId: "crossenv-2017-07-19", packageName: "crossenv", independentlyReportedAffectedVersion: "6.1.1", affectedVersionPublishedUtc: "2017-07-19T06:49:52.698Z", strictFeatureCutoffUtc: "2017-07-19T06:49:52.697Z", timeMapSelectedPreEventVersion: "6.0.7" },
      strictExclusionReason: { observedState: "The official registry time map selects crossenv@6.0.7 immediately before the independently reported crossenv@6.1.1 timestamp, but the current bounded response retains only 1.0.0 and 1.0.1 version objects; the selected 6.0.7 object is absent." },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
  });

  it("excludes sbx-mask when no strict pre-event source object is retained", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/138_sbx_mask_march_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object",
      candidate: { recordId: "sbx-mask-2026-03-18", packageName: "sbx-mask", affectedVersions: ["1.0.0", "1.0.1", "1.0.2"], earliestAffectedVersion: { version: "1.0.0", publishedUtc: "2026-03-19T14:46:00.636Z" }, strictFeatureCutoffUtc: "2026-03-19T14:46:00.635Z", selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: false, eligibleForGovernedReconstruction: false },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
  });

  it("admits bounded Red Hat Entitlements Client only as a documented Mini Shai-Hulud-family member without an additional validation unit", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/171_redhat_entitlements_client_june_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "admit_as_one_bounded_row_in_existing_mini_shai_hulud_family_without_creating_an_independent_validation_unit",
      candidate: { recordId: "redhat-cloud-services-entitlements-client-2026-06-01", packageName: "@redhat-cloud-services/entitlements-client", affectedVersions: ["4.0.11", "4.0.12"], earliestAffectedVersion: { version: "4.0.11", publishedUtc: "2026-06-01T10:54:20.421Z" }, strictFeatureCutoffUtc: "2026-06-01T10:54:20.420Z", selectedPreEventVersion: "4.0.10", selectedPreEventVersionObjectRetained: true, existingFamily: "mini_shai_hulud_atool_2026", campaignCompletenessClaim: false, statisticalIndependenceClaim: false },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, familyTreatmentExplicitlyDocumented: true, eligibleForGovernedReconstruction: true },
    });
    expect(assessment.prohibitedInterpretations).toContain("No controls, benign labels, scores, models, rankings, intervals, calibration results, or predictive metrics are created.");
  });

  it("excludes Joyfill from a new independent family when PolinRider relatedness is documented", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/146_joyfill_components_july_2026_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_new_independent_primary_family_due_to_documented_polinrider_relatedness",
      candidate: { recordId: "joyfill-components-2026-07-28", packageName: "@joyfill/components", affectedVersionIntersection: ["4.0.0-rc24-2773-beta.4"], existingRelatedGovernedFamily: "common_stack_generate_plugin_polinrider_hijack_2026", distinctFromExistingLedgerFamilies: false },
      registryBoundary: { officialRegistryRequestAttempted: false, strictFeatureCutoffUtc: null, selectedPreEventVersion: null, selectedPreEventVersionObjectRetained: null },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
  });

  it("excludes duplicate country-currency-map event screening without adding a second ledger record", async () => {
    const assessment = await import("node:fs/promises").then((fs) => fs.readFile("research/131_country_currency_map_march_2025_candidate_assessment.json", "utf8")).then(JSON.parse);
    expect(assessment).toMatchObject({
      decision: "exclude_from_primary_temporal_ledger_due_to_duplicate_existing_country_currency_map_event_record",
      candidate: { recordId: "country-currency-map-2025-03-26", packageName: "country-currency-map", affectedVersions: ["2.1.8"], strictFeatureCutoffUtc: "2025-03-25T09:03:00.517Z", selectedPreEventVersion: "2.1.7", selectedPreEventVersionObjectRetained: true, distinctFromExistingLedgerFamilies: false, duplicateOfExistingLedgerRecord: "country-currency-map-2025-03-25" },
      strictEligibility: { finiteExactAffectedVersionsIndependentlyCorroborated: true, officialAffectedVersionTimestampsRetained: true, selectedPreEventVersionObjectRetained: true, eligibleForGovernedReconstruction: false, duplicateExistingLedgerRecord: true },
      currentDecision: { primaryLedgerRecordsAdded: 0, primaryLedgerFamiliesAdded: 0, futureValidationUnitsAdded: 0, exactPreEventSourceSnapshotsCreated: 0, dependencyDeclarationsCreated: 0, recursiveGraphEdgesCreated: 0, controlsCreated: 0, modelsFitted: 0, predictiveMetricsComputed: 0 },
    });
  });
});
