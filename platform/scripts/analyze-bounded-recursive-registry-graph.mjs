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
      } else if (character === "," && !quoted) { values.push(current); current = ""; } else current += character;
    }
    values.push(current);
    return Object.fromEntries(columns.map((column, index) => [column, values[index] ?? ""]));
  });
}

const inputText = await readFile(path.join(researchDir, "74_bounded_recursive_registry_semver_graph_edges.csv"), "utf8");
const edges = parseCsv(inputText);
const perRoot = Object.entries(Object.groupBy(edges, edge => edge.record_id)).map(([recordId, rows]) => {
  const nodes = new Set(rows.flatMap(row => [row.parent_node, row.target_version ? `${row.target_package}@${row.target_version}` : ""]).filter(Boolean));
  const depthCounts = Object.fromEntries([1, 2, 3].map(depth => [String(depth), rows.filter(row => Number(row.depth) === depth).length]));
  return {
    recordId,
    rootNode: rows[0].root_node,
    boundedEdges: rows.length,
    boundedNodesIncludingRoot: nodes.size,
    depthCounts,
    unresolvedEdges: rows.filter(row => row.target_resolution_status !== "resolved_cutoff_semver_range").length,
    includedEdges: rows.filter(row => row.traversal_status === "included_within_depth_bound").length,
  };
});

const diagnostic = {
  study: "bounded-recursive-registry-semver-graph-descriptive-diagnostic",
  generatedAtUtc: new Date().toISOString(),
  inputArtifact: "74_bounded_recursive_registry_semver_graph_edges.csv",
  summary: {
    rootRecordsWithEdges: perRoot.length,
    boundedEdges: edges.length,
    boundedNodesAcrossRootGraphs: perRoot.reduce((sum, item) => sum + item.boundedNodesIncludingRoot, 0),
    directDepthOneEdges: edges.filter(edge => Number(edge.depth) === 1).length,
    depthTwoEdges: edges.filter(edge => Number(edge.depth) === 2).length,
    depthThreeEdges: edges.filter(edge => Number(edge.depth) === 3).length,
    unresolvedEdges: edges.filter(edge => edge.target_resolution_status !== "resolved_cutoff_semver_range").length,
    globalReachValuesComputed: 0,
    centralityValuesComputed: 0,
    predictiveMetricsComputed: 0,
  },
  perRoot,
  interpretation: "Counts describe only the depth-three, runtime-dependency, registry-range reconstruction bound. They are not historical installed-tree size, transitive dependency reach, downstream blast radius, or a predictive feature.",
  prohibitedInterpretations: [
    "Do not treat any bounded node count as an npm installation result or package-lock reconstruction.",
    "Do not compare counts across roots as security scores or use them for ranking, calibration, recall, PR-AUC, or attack-return claims.",
  ],
};
await writeFile(path.join(researchDir, "75_bounded_recursive_registry_graph_diagnostic.json"), JSON.stringify(diagnostic, null, 2) + "\n");
console.log(JSON.stringify(diagnostic.summary, null, 2));
