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

const edges = parseCsv(await readFile(path.join(researchDir, "70_cutoff_direct_dependency_range_resolution.csv"), "utf8"));
const byRecord = Object.values(Object.groupBy(edges, edge => edge.record_id)).map(rows => ({
  recordId: rows[0].record_id,
  sourceNode: rows[0].source_node,
  declaredEdgeCount: rows.length,
  isolatedRangeResolutions: rows.filter(row => row.target_resolution_status === "resolved_isolated_semver_range").length,
  unresolvedRanges: rows.filter(row => row.target_resolution_status !== "resolved_isolated_semver_range").length,
}));
const diagnostic = {
  study: "direct-range-resolution-descriptive-diagnostic",
  generatedAtUtc: new Date().toISOString(),
  inputArtifact: "70_cutoff_direct_dependency_range_resolution.csv",
  summary: {
    declaredDirectEdges: edges.length,
    isolatedCutoffSemverApproximations: edges.filter(row => row.target_resolution_status === "resolved_isolated_semver_range").length,
    unresolvedDirectRanges: edges.filter(row => row.target_resolution_status !== "resolved_isolated_semver_range").length,
    sourceRecordsWithDirectEdges: byRecord.length,
    computedTransitiveReachValues: 0,
  },
  perRecord: byRecord,
  fidelityBoundary: "Target selection is an isolated highest-satisfying SemVer calculation over currently retained registry versions published at or before the cutoff. It is not evidence of the package-manager result that any historical installation actually obtained.",
  inferenceGate: {
    temporalRanking: "blocked: no cutoff-valid control population",
    probabilityCalibration: "blocked: no cutoff-valid evaluation population; positive-count and family-count floors alone do not permit calibration",
    blastRadius: "blocked: no transitive traversal or downstream dependency population has been reconstructed",
  },
};
await writeFile(path.join(researchDir, "71_direct_range_resolution_diagnostic.json"), JSON.stringify(diagnostic, null, 2) + "\n");
console.log(JSON.stringify(diagnostic.summary, null, 2));
