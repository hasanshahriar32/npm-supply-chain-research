import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import semver from "semver";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const MAX_DEPTH = 3;
const MAX_NODES_PER_ROOT = 250;
const USER_AGENT = "supply-chain-research-bounded-recursive-graph/1.0";

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
      } else if (character === "," && !quoted) { values.push(current); current = ""; } else current += character;
    }
    values.push(current);
    return Object.fromEntries(columns.map((column, index) => [column, values[index] ?? ""]));
  });
}

function escapeCsv(value) {
  const text = value == null ? "" : String(value);
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

async function getRegistry(packageName, cache) {
  if (cache.has(packageName)) return cache.get(packageName);
  const response = await fetch(`https://registry.npmjs.org/${encodeURIComponent(packageName)}`, { headers: { Accept: "application/json", "User-Agent": USER_AGENT } });
  const body = await response.text();
  if (!response.ok) throw new Error(`Registry request for ${packageName} failed (${response.status}).`);
  const entry = { metadata: JSON.parse(body), sha256: createHash("sha256").update(body).digest("hex") };
  cache.set(packageName, entry);
  return entry;
}

function selectVersion(metadata, declaredRange, cutoffMs) {
  if (!semver.validRange(declaredRange)) return { status: "unsupported_or_invalid_semver_range" };
  const candidates = Object.entries(metadata.time ?? {})
    .filter(([version, timestamp]) => version !== "created" && version !== "modified" && metadata.versions?.[version] && semver.valid(version) && Date.parse(timestamp) <= cutoffMs)
    .map(([version, timestamp]) => ({ version, publishedUtc: new Date(Date.parse(timestamp)).toISOString() }));
  const selectedVersion = semver.maxSatisfying(candidates.map(candidate => candidate.version), declaredRange, { includePrerelease: false });
  const selected = candidates.find(candidate => candidate.version === selectedVersion);
  return selected ? { status: "resolved_cutoff_semver_range", selected, eligibleVersionCount: candidates.length } : { status: "no_cutoff_valid_satisfying_version", eligibleVersionCount: candidates.length };
}

const inputText = await readFile(path.join(researchDir, "65_package_temporal_companion_snapshots.csv"), "utf8");
const roots = parseCsv(inputText).filter(row => row.snapshot_status === "registry_reconstructed_exact");
const registryCache = new Map();
const edges = [];
const perRoot = [];

for (const source of roots) {
  const cutoffMs = Date.parse(source.feature_cutoff_utc);
  const rootNode = `${source.package_name}@${source.pre_event_latest_version}`;
  const queue = [{ packageName: source.package_name, version: source.pre_event_latest_version, node: rootNode, depth: 0, nodeFidelity: "registry_reconstructed_exact_source_snapshot" }];
  const visitedNodes = new Set([rootNode]);
  let rootEdges = 0;
  let unresolvedEdges = 0;
  let nodeCapReached = false;

  while (queue.length) {
    const parent = queue.shift();
    if (parent.depth >= MAX_DEPTH || nodeCapReached) continue;
    let parentRegistry;
    try { parentRegistry = await getRegistry(parent.packageName, registryCache); } catch (error) {
      edges.push({ record_id: source.record_id, root_node: rootNode, feature_cutoff_utc: source.feature_cutoff_utc, depth: parent.depth + 1, parent_node: parent.node, parent_node_fidelity: parent.nodeFidelity, dependency_type: "dependencies", target_package: "", declared_range: "", target_version: "", target_version_published_utc: "", target_resolution_status: "parent_registry_unavailable", target_node_fidelity: "not_available", parent_registry_response_sha256: "", target_registry_response_sha256: "", traversal_status: "stopped", note: String(error.message) });
      unresolvedEdges += 1;
      continue;
    }
    const parentManifest = parentRegistry.metadata.versions?.[parent.version];
    if (!parentManifest) {
      edges.push({ record_id: source.record_id, root_node: rootNode, feature_cutoff_utc: source.feature_cutoff_utc, depth: parent.depth + 1, parent_node: parent.node, parent_node_fidelity: parent.nodeFidelity, dependency_type: "dependencies", target_package: "", declared_range: "", target_version: "", target_version_published_utc: "", target_resolution_status: "parent_version_unavailable", target_node_fidelity: "not_available", parent_registry_response_sha256: parentRegistry.sha256, target_registry_response_sha256: "", traversal_status: "stopped", note: "The parent version object is not retained in the current registry response." });
      unresolvedEdges += 1;
      continue;
    }
    for (const [targetPackage, declaredRange] of Object.entries(parentManifest.dependencies ?? {})) {
      let targetRegistry;
      let selection;
      try {
        targetRegistry = await getRegistry(targetPackage, registryCache);
        selection = selectVersion(targetRegistry.metadata, declaredRange, cutoffMs);
      } catch (error) {
        selection = { status: "target_registry_unavailable", error: String(error.message) };
      }
      const selected = selection.selected;
      const targetNode = selected ? `${targetPackage}@${selected.version}` : "";
      const edge = {
        record_id: source.record_id,
        root_node: rootNode,
        feature_cutoff_utc: source.feature_cutoff_utc,
        depth: parent.depth + 1,
        parent_node: parent.node,
        parent_node_fidelity: parent.nodeFidelity,
        dependency_type: "dependencies",
        target_package: targetPackage,
        declared_range: declaredRange,
        target_version: selected?.version ?? "",
        target_version_published_utc: selected?.publishedUtc ?? "",
        target_resolution_status: selection.status,
        target_node_fidelity: selected ? "registry_reconstructed_cutoff_semver_approximation" : "not_available",
        parent_registry_response_sha256: parentRegistry.sha256,
        target_registry_response_sha256: targetRegistry?.sha256 ?? "",
        traversal_status: selected ? "included_within_depth_bound" : "stopped",
        note: selected
          ? "Target is the highest non-prerelease SemVer version satisfying the declared runtime dependency range among retained registry versions published by the root cutoff. It is not a package-manager installation result."
          : selection.error ?? "No cutoff-valid target was selected for this declared range.",
      };
      edges.push(edge);
      rootEdges += 1;
      if (!selected) { unresolvedEdges += 1; continue; }
      if (visitedNodes.has(targetNode)) continue;
      if (visitedNodes.size >= MAX_NODES_PER_ROOT) { nodeCapReached = true; edge.traversal_status = "node_cap_reached"; continue; }
      visitedNodes.add(targetNode);
      queue.push({ packageName: targetPackage, version: selected.version, node: targetNode, depth: parent.depth + 1, nodeFidelity: "registry_reconstructed_cutoff_semver_approximation" });
    }
  }
  perRoot.push({ recordId: source.record_id, rootNode, cutoffUtc: source.feature_cutoff_utc, rootEdges, reconstructedNodes: visitedNodes.size, unresolvedEdges, nodeCapReached });
}

const header = Object.keys(edges[0] ?? { record_id: "" });
await writeFile(path.join(researchDir, "74_bounded_recursive_registry_semver_graph_edges.csv"), [header.join(","), ...edges.map(row => header.map(key => escapeCsv(row[key])).join(","))].join("\n") + "\n");
const manifest = {
  study: "bounded-recursive-registry-semver-dependency-approximation",
  schemaVersion: "1.0",
  generatedAtUtc: new Date().toISOString(),
  inputArtifact: "65_package_temporal_companion_snapshots.csv",
  inputSha256: createHash("sha256").update(inputText).digest("hex"),
  resolver: { implementation: "npm semver", includePrerelease: false, strategy: "highest retained cutoff-valid satisfying version" },
  bounds: { maxDepth: MAX_DEPTH, maxNodesPerRoot: MAX_NODES_PER_ROOT, relationsIncluded: ["dependencies"], relationsExcluded: ["devDependencies", "peerDependencies", "optionalDependencies", "bundledDependencies", "overrides", "workspace", "link", "git", "tarball"] },
  summary: { exactRootSnapshots: roots.length, reconstructedEdges: edges.length, reconstructedNodesAcrossRoots: perRoot.reduce((sum, item) => sum + item.reconstructedNodes, 0), unresolvedEdges: edges.filter(edge => edge.target_resolution_status !== "resolved_cutoff_semver_range").length, maxObservedDepth: Math.max(0, ...edges.map(edge => Number(edge.depth))), perRoot },
  fidelityVocabulary: {
    registry_reconstructed_exact_source_snapshot: "A pre-event root package-version object retained by the current registry and selected using its official version timestamp.",
    registry_reconstructed_cutoff_semver_approximation: "A non-root package version selected by cutoff-valid highest-satisfying SemVer range logic from currently retained registry version objects.",
    not_available: "No cutoff-valid range-selected target could be reconstructed.",
  },
  prohibitedInterpretations: [
    "This graph is not a package-lock, npm install execution trace, or reproducible historical node_modules tree.",
    "The graph does not resolve peer, optional, bundled, workspace, override, link, git, tarball, nested-hoisting, cache, registry-configuration, or package-manager-version behavior.",
    "The bounded graph is not a full transitive dependency graph and must not be used for global reach, centrality, blast-radius, ranking, calibration, or attack-return claims.",
  ],
};
await writeFile(path.join(researchDir, "74_bounded_recursive_registry_semver_graph_manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
console.log(JSON.stringify(manifest.summary, null, 2));
