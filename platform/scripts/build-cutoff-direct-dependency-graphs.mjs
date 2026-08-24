import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/);
  const columns = header.split(",");
  return lines.filter(Boolean).map(line => {
    const values = [];
    let current = "";
    let quoted = false;
    for (let index = 0; index < line.length; index += 1) {
      const character = line[index];
      if (character === '"') {
        if (quoted && line[index + 1] === '"') { current += '"'; index += 1; } else quoted = !quoted;
      } else if (character === "," && !quoted) {
        values.push(current);
        current = "";
      } else current += character;
    }
    values.push(current);
    return Object.fromEntries(columns.map((column, index) => [column, values[index] ?? ""]));
  });
}

function escapeCsv(value) {
  const text = value == null ? "" : String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

const [snapshotText, companionEdgeText] = await Promise.all([
  readFile(path.join(researchDir, "65_package_temporal_companion_snapshots.csv"), "utf8"),
  readFile(path.join(researchDir, "65_package_temporal_companion_declared_edges.csv"), "utf8"),
]);
const snapshots = parseCsv(snapshotText);
const companionEdges = parseCsv(companionEdgeText);
const sourceByRecord = new Map(snapshots.map(snapshot => [snapshot.record_id, snapshot]));

const graphEdges = companionEdges.map(edge => ({
  record_id: edge.record_id,
  source_node: `${edge.source_package}@${edge.source_version}`,
  source_package: edge.source_package,
  source_version: edge.source_version,
  target_node: `npm:${edge.target_package}`,
  target_package: edge.target_package,
  declared_range: edge.declared_range,
  feature_cutoff_utc: edge.feature_cutoff_utc,
  edge_type: edge.edge_type,
  source_snapshot_fidelity: "registry_reconstructed_exact_direct_declaration",
  target_version_fidelity: "unresolved_not_attempted",
  transitive_reach_fidelity: "not_computed",
  registry_response_sha256: sourceByRecord.get(edge.record_id)?.registry_response_sha256 ?? "",
}));

const perRecord = snapshots.map(snapshot => {
  const recordEdges = graphEdges.filter(edge => edge.record_id === snapshot.record_id);
  const exact = snapshot.snapshot_status === "registry_reconstructed_exact";
  return {
    recordId: snapshot.record_id,
    incidentFamily: snapshot.event_family,
    sourcePackage: snapshot.package_name,
    cutoffUtc: snapshot.feature_cutoff_utc,
    sourceVersion: snapshot.pre_event_latest_version || null,
    sourceSnapshotFidelity: exact ? "registry_reconstructed_exact_direct_declaration" : "not_available",
    declaredDirectEdgeCount: recordEdges.length,
    targetVersionResolution: exact ? "unresolved_not_attempted" : "not_applicable",
    transitiveReach: "not_computed",
    registryResponseSha256: snapshot.registry_response_sha256,
  };
});

const manifest = {
  study: "cutoff-valid-direct-dependency-graph-reconstruction",
  schemaVersion: "1.0",
  generatedAtUtc: new Date().toISOString(),
  inputArtifacts: {
    snapshots: "65_package_temporal_companion_snapshots.csv",
    declaredEdges: "65_package_temporal_companion_declared_edges.csv",
    inputSha256: {
      snapshots: createHash("sha256").update(snapshotText).digest("hex"),
      declaredEdges: createHash("sha256").update(companionEdgeText).digest("hex"),
    },
  },
  scope: "Eight pre-registered package-event records in the temporal companion ledger; source versions were selected strictly before each event cutoff from official npm registry version timestamps.",
  fidelityVocabulary: {
    registry_reconstructed_exact_direct_declaration: "Exact source package version selected at or before the cutoff and its declared runtime dependency range read from that version's registry metadata.",
    unresolved_not_attempted: "A dependency package was named and its declared SemVer range retained, but no target version was selected or resolved.",
    not_available: "No source version object was available from the registry reconstruction for this record.",
    not_computed: "No multi-hop or graph-reachability quantity was computed.",
  },
  prohibitedInterpretations: [
    "This artifact is not a lockfile, a package-manager resolution, or a transitive dependency graph.",
    "It cannot support historical centrality, dependency reach, blast-radius, or attack-return estimates.",
    "Current maintainer, repository, workflow, download, and popularity information is not used as historical graph evidence.",
  ],
  summary: {
    packageEventRecords: perRecord.length,
    exactSourceSnapshots: perRecord.filter(record => record.sourceSnapshotFidelity === "registry_reconstructed_exact_direct_declaration").length,
    unavailableSourceSnapshots: perRecord.filter(record => record.sourceSnapshotFidelity === "not_available").length,
    declaredDirectEdges: graphEdges.length,
    resolvedTargetVersions: 0,
    computedTransitiveReachValues: 0,
  },
  records: perRecord,
};

const edgeHeader = Object.keys(graphEdges[0] ?? { record_id: "" });
const edgeCsv = [edgeHeader.join(","), ...graphEdges.map(row => edgeHeader.map(key => escapeCsv(row[key])).join(","))].join("\n") + "\n";
await writeFile(path.join(researchDir, "67_cutoff_direct_dependency_graph_edges.csv"), edgeCsv);
await writeFile(path.join(researchDir, "67_cutoff_direct_dependency_graph_manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
console.log(JSON.stringify(manifest.summary, null, 2));
