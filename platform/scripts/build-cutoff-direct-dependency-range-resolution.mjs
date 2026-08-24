import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import semver from "semver";

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

async function getRegistry(packageName) {
  const response = await fetch(`https://registry.npmjs.org/${encodeURIComponent(packageName)}`, {
    headers: { Accept: "application/json", "User-Agent": "supply-chain-research-range-resolution/1.0" },
  });
  const body = await response.text();
  if (!response.ok) throw new Error(`Registry request for ${packageName} failed (${response.status}).`);
  return { metadata: JSON.parse(body), sha256: createHash("sha256").update(body).digest("hex") };
}

function eligibleVersions(metadata, cutoffMs) {
  return Object.entries(metadata.time ?? {})
    .filter(([version, timestamp]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(timestamp)))
    .filter(([version, timestamp]) => metadata.versions?.[version] && Date.parse(timestamp) <= cutoffMs && semver.valid(version))
    .map(([version, timestamp]) => ({ version, timestamp: new Date(Date.parse(timestamp)).toISOString() }));
}

const inputText = await readFile(path.join(researchDir, "67_cutoff_direct_dependency_graph_edges.csv"), "utf8");
const edges = parseCsv(inputText);
const targetCache = new Map();
const output = [];

for (const edge of edges) {
  const cutoffMs = Date.parse(edge.feature_cutoff_utc);
  let target;
  try {
    target = targetCache.get(edge.target_package);
    if (!target) {
      target = await getRegistry(edge.target_package);
      targetCache.set(edge.target_package, target);
    }
  } catch (error) {
    output.push({
      ...edge,
      target_resolution_status: "target_registry_unavailable",
      target_version: "",
      target_version_published_utc: "",
      eligible_target_version_count: 0,
      target_registry_response_sha256: "",
      target_version_fidelity: "not_available",
      resolution_note: String(error.message),
    });
    continue;
  }
  const candidates = eligibleVersions(target.metadata, cutoffMs);
  const matching = semver.validRange(edge.declared_range) ? semver.maxSatisfying(candidates.map(candidate => candidate.version), edge.declared_range, { includePrerelease: false }) : null;
  const selected = candidates.find(candidate => candidate.version === matching);
  output.push({
    ...edge,
    target_resolution_status: matching ? "resolved_isolated_semver_range" : semver.validRange(edge.declared_range) ? "no_cutoff_valid_satisfying_version" : "unsupported_or_invalid_semver_range",
    target_version: matching ?? "",
    target_version_published_utc: selected?.timestamp ?? "",
    eligible_target_version_count: candidates.length,
    target_registry_response_sha256: target.sha256,
    target_version_fidelity: matching ? "registry_reconstructed_cutoff_semver_approximation" : "not_available",
    resolution_note: matching
      ? "Highest valid SemVer target satisfying the declared range among versions retained by the current registry response and published at or before the cutoff; isolated direct-range calculation only."
      : "No target version was selected; this record remains unsuitable for a resolved direct edge.",
  });
}

const header = Object.keys(output[0] ?? { record_id: "" });
const csv = [header.join(","), ...output.map(row => header.map(key => escapeCsv(row[key])).join(","))].join("\n") + "\n";
const summary = {
  inputDeclaredEdges: edges.length,
  attemptedTargetResolutions: output.length,
  resolvedIsolatedSemverRanges: output.filter(row => row.target_resolution_status === "resolved_isolated_semver_range").length,
  unresolvedTargetRanges: output.filter(row => row.target_resolution_status !== "resolved_isolated_semver_range").length,
  distinctTargetPackages: targetCache.size,
  computedTransitiveReachValues: 0,
};
const manifest = {
  study: "cutoff-valid-isolated-direct-range-resolution",
  schemaVersion: "1.0",
  generatedAtUtc: new Date().toISOString(),
  inputArtifact: "67_cutoff_direct_dependency_graph_edges.csv",
  inputSha256: createHash("sha256").update(inputText).digest("hex"),
  resolver: { implementation: "npm semver", version: semver.SemVer ? "7.x" : "unknown", includePrerelease: false },
  summary,
  fidelityVocabulary: {
    registry_reconstructed_exact_direct_declaration: "Exact source package declaration reconstructed from a cutoff-selected registry version object.",
    registry_reconstructed_cutoff_semver_approximation: "Highest target version satisfying one declared range among current-registry versions timestamped at or before the cutoff. It is an isolated range calculation, not a recorded install result.",
    not_available: "The target range could not be resolved from registry metadata under the stated method.",
  },
  prohibitedInterpretations: [
    "This artifact is not a package-lock, npm --before execution trace, or reproducible installation result.",
    "Peer, optional, bundled, workspace, override, and nested dependency behavior is not resolved here.",
    "No transitive dependency graph, downstream reach, centrality, blast radius, or attack-return metric is computed.",
  ],
};

await writeFile(path.join(researchDir, "70_cutoff_direct_dependency_range_resolution.csv"), csv);
await writeFile(path.join(researchDir, "70_cutoff_direct_dependency_range_resolution_manifest.json"), JSON.stringify(manifest, null, 2) + "\n");
console.log(JSON.stringify(summary, null, 2));
