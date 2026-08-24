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
  });

  it("marks the graph-attention experiment as blocked until prerequisites are met", () => {
    const hgat = getExperiments().find((experiment) => experiment.id === "hgat");
    expect(hgat?.status).toBe("blocked");
  });

  it("serves the completed temporal reconstruction and adjudication artifacts in governed workspace sections", async () => {
    const documents = await getDocuments();
    expect(documents.find((document) => document.slug === "gap-analysis")?.sourceFile).toBe("68_temporal_reconstruction_and_baseline_results.md");
    expect(documents.find((document) => document.slug === "methodology")?.sourceFile).toBe("50_gap_resolution_study_protocol.md");
    expect(documents.find((document) => document.slug === "incident-labels")?.sourceFile).toBe("69_temporal_incident_label_adjudication.md");
    expect(documents.find((document) => document.slug === "experiment-results")?.sourceFile).toBe("68_temporal_reconstruction_and_baseline_results.md");
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ title: "Gap Analysis" });
    await expect(getDocument("gap-analysis")).resolves.toMatchObject({ markdown: expect.stringContaining("no predictive model has been fitted") });
    await expect(getDocument("incident-labels")).resolves.toMatchObject({ markdown: expect.stringContaining("nine package-event records") });
  });

  it("preserves the generated direct-edge fidelity boundary and no-fit calibration result", async () => {
    const graph = await import("node:fs/promises").then((fs) => fs.readFile("research/67_cutoff_direct_dependency_graph_manifest.json", "utf8")).then(JSON.parse);
    const rangeResolution = await import("node:fs/promises").then((fs) => fs.readFile("research/70_cutoff_direct_dependency_range_resolution_manifest.json", "utf8")).then(JSON.parse);
    const rangeDiagnostic = await import("node:fs/promises").then((fs) => fs.readFile("research/71_direct_range_resolution_diagnostic.json", "utf8")).then(JSON.parse);
    const gate = await import("node:fs/promises").then((fs) => fs.readFile("research/66_temporal_baseline_and_calibration_gate.json", "utf8")).then(JSON.parse);
    expect(graph.summary).toMatchObject({ packageEventRecords: 9, exactSourceSnapshots: 8, declaredDirectEdges: 24, resolvedTargetVersions: 0, computedTransitiveReachValues: 0 });
    expect(graph.prohibitedInterpretations).toContain("This artifact is not a lockfile, a package-manager resolution, or a transitive dependency graph.");
    expect(rangeResolution.summary).toMatchObject({ inputDeclaredEdges: 24, resolvedIsolatedSemverRanges: 24, unresolvedTargetRanges: 0, computedTransitiveReachValues: 0 });
    expect(rangeResolution.prohibitedInterpretations).toContain("This artifact is not a package-lock, npm --before execution trace, or reproducible installation result.");
    expect(rangeDiagnostic).toMatchObject({ summary: { declaredDirectEdges: 24, isolatedCutoffSemverApproximations: 24, computedTransitiveReachValues: 0 } });
    expect(gate).toMatchObject({ exactPreEventSnapshots: 8, calibrationInference: "blocked" });
    expect(gate.distinctIncidentFamilies).toContain("node_ipc_2026");
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
    expect(manifest.summary).toMatchObject({ exactRootSnapshots: 8, reconstructedEdges: 59, unresolvedEdges: 0, maxObservedDepth: 3 });
    expect(manifest.prohibitedInterpretations).toContain("This graph is not a package-lock, npm install execution trace, or reproducible historical node_modules tree.");
    expect(diagnostic.summary).toMatchObject({ boundedEdges: 59, directDepthOneEdges: 24, depthTwoEdges: 18, depthThreeEdges: 17, globalReachValuesComputed: 0, predictiveMetricsComputed: 0 });
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
    expect(overlap.summary).toMatchObject({ primaryRecordsChecked: 9, exactAffectedVersionMembership: 2, packagePresentVersionsUnspecified: 1, packageNotPresent: 6, newPrimaryLabelsCreated: 0, controlsCreated: 0 });
    expect(overlap.interpretation).toContain("no event time");
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "axios-2026-03-31")).toMatchObject({ positive_membership_status: "exact_affected_version_membership" });
    expect(overlap.records.find((record: { record_id: string }) => record.record_id === "node-ipc-2026-05-14")).toMatchObject({ positive_membership_status: "exact_affected_version_membership", permitted_use: "candidate_positive_membership_corroboration_only" });
  });
});
