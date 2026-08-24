import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/);
  const columns = header.split(",");
  return lines.map(line => {
    const values = [];
    let current = "";
    let quoted = false;
    for (let i = 0; i < line.length; i += 1) {
      const character = line[i];
      if (character === '"') {
        if (quoted && line[i + 1] === '"') { current += '"'; i += 1; } else quoted = !quoted;
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

async function getRegistry(packageName) {
  const response = await fetch(`https://registry.npmjs.org/${encodeURIComponent(packageName)}`, {
    headers: { Accept: "application/json", "User-Agent": "supply-chain-research-temporal-companion/1.0" },
  });
  const body = await response.text();
  if (!response.ok) throw new Error(`Registry request for ${packageName} failed (${response.status}).`);
  return { metadata: JSON.parse(body), sha256: createHash("sha256").update(body).digest("hex") };
}

const ledger = parseCsv(await readFile(path.join(researchDir, "64_temporal_package_event_ledger.csv"), "utf8"));
const output = [];
const edges = [];
const provenance = [];

for (const record of ledger) {
  const { metadata, sha256 } = await getRegistry(record.package_name);
  const cutoffMs = Date.parse(record.event_start_utc) - 1;
  const timeline = Object.entries(metadata.time ?? {})
    .filter(([version, timestamp]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(timestamp)))
    .map(([version, timestamp]) => ({ version, timestamp, ms: Date.parse(timestamp) }))
    .sort((a, b) => a.ms - b.ms);
  const latest = timeline.filter(entry => entry.ms <= cutoffMs).at(-1);
  const selected = latest ? metadata.versions?.[latest.version] : null;
  const dependencies = selected?.dependencies ?? {};
  const scripts = selected?.scripts ?? {};
  const first = timeline.at(0);
  const priorCount = timeline.filter(entry => entry.ms <= cutoffMs).length;
  output.push({
    record_id: record.record_id,
    package_name: record.package_name,
    event_family: record.event_family,
    event_start_utc: record.event_start_utc,
    label_class: record.label_class,
    feature_cutoff_utc: new Date(cutoffMs).toISOString(),
    pre_event_latest_version: latest?.version ?? "",
    pre_event_latest_published_utc: latest?.timestamp ? new Date(latest.ms).toISOString() : "",
    package_age_days: first ? Math.floor((cutoffMs - first.ms) / 86_400_000) : "",
    prior_version_count: priorCount,
    direct_dependency_count: Object.keys(dependencies).length,
    has_install_script: Boolean(selected?.hasInstallScript ?? scripts.preinstall ?? scripts.install ?? scripts.postinstall),
    integrity_present: Boolean(selected?.dist?.integrity),
    snapshot_status: selected ? "registry_reconstructed_exact" : "not_available",
    target_status: "event_label_only_not_model_target",
    registry_response_sha256: sha256,
  });
  for (const [targetPackage, declaredRange] of Object.entries(dependencies)) {
    edges.push({
      record_id: record.record_id,
      source_package: record.package_name,
      source_version: latest?.version ?? "",
      target_package: targetPackage,
      declared_range: declaredRange,
      feature_cutoff_utc: new Date(cutoffMs).toISOString(),
      edge_type: "runtime_direct_dependency",
      historical_fidelity: "registry_reconstructed_direct_declaration",
      resolution_status: "not_version_resolved",
    });
  }
  provenance.push({ packageName: record.package_name, responseSha256: sha256, retrievedAt: new Date().toISOString() });
}

const families = [...new Set(output.map(row => row.event_family))];
const header = Object.keys(output[0] ?? { record_id: "" });
const csv = [header.join(","), ...output.map(row => header.map(key => escapeCsv(row[key])).join(","))].join("\n") + "\n";
const edgeHeader = Object.keys(edges[0] ?? { record_id: "" });
const edgeCsv = [edgeHeader.join(","), ...edges.map(row => edgeHeader.map(key => escapeCsv(row[key])).join(","))].join("\n") + "\n";
const diagnostics = {
  study: "package-level-temporal-companion",
  observations: output.length,
  incidentFamilies: families,
  incidentFamilyCount: families.length,
  exactSnapshotCount: output.filter(row => row.snapshot_status === "registry_reconstructed_exact").length,
  directDeclaredEdgeCount: edges.length,
  graphFidelity: "cutoff-valid direct dependency declarations only; no package-version or transitive resolution",
  controls: "not constructed; no defensible negative population was pre-registered",
  calibrationInference: "blocked",
  blockedReason: [
    output.length < 10 ? `Only ${output.length} strict pre-registered package-event records are available; the minimum gate is ten.` : null,
    families.length < 5 ? `Only ${families.length} independent incident families are available; the minimum gate is five.` : null,
    "No cutoff-valid, independently adjudicated negative/control design is available.",
  ].filter(Boolean).join(" "),
  provenance,
};

await mkdir(researchDir, { recursive: true });
await writeFile(path.join(researchDir, "65_package_temporal_companion_snapshots.csv"), csv);
await writeFile(path.join(researchDir, "65_package_temporal_companion_declared_edges.csv"), edgeCsv);
await writeFile(path.join(researchDir, "65_package_temporal_companion_diagnostics.json"), JSON.stringify(diagnostics, null, 2) + "\n");
console.log(JSON.stringify({ observations: diagnostics.observations, incidentFamilyCount: diagnostics.incidentFamilyCount, calibrationInference: diagnostics.calibrationInference }, null, 2));
