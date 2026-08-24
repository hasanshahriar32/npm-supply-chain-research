import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

function parseCsv(text) {
  const [header, ...lines] = text.trim().split(/\r?\n/);
  const columns = header.split(",");
  return lines.map(line => Object.fromEntries(line.split(",").map((value, index) => [columns[index], value])));
}

function numeric(values) {
  const valid = values.map(Number).filter(Number.isFinite);
  if (!valid.length) return { count: 0, min: null, median: null, max: null, mean: null };
  const sorted = [...valid].sort((a, b) => a - b);
  const median = sorted.length % 2 ? sorted[(sorted.length - 1) / 2] : (sorted[sorted.length / 2 - 1] + sorted[sorted.length / 2]) / 2;
  return { count: valid.length, min: sorted[0], median, max: sorted.at(-1), mean: valid.reduce((sum, value) => sum + value, 0) / valid.length };
}

const rows = parseCsv(await readFile(path.join(researchDir, "65_package_temporal_companion_snapshots.csv"), "utf8"));
const diagnostics = JSON.parse(await readFile(path.join(researchDir, "65_package_temporal_companion_diagnostics.json"), "utf8"));
const exact = rows.filter(row => row.snapshot_status === "registry_reconstructed_exact");
const distinctFamilies = [...new Set(exact.map(row => row.event_family))];
const report = {
  study: "temporal-baseline-and-calibration-gate",
  exactPreEventSnapshots: exact.length,
  distinctIncidentFamilies: distinctFamilies,
  featureSummaries: {
    package_age_days: numeric(exact.map(row => row.package_age_days)),
    prior_version_count: numeric(exact.map(row => row.prior_version_count)),
    direct_dependency_count: numeric(exact.map(row => row.direct_dependency_count)),
    install_script_true_count: exact.filter(row => row.has_install_script === "true").length,
    integrity_present_count: exact.filter(row => row.integrity_present === "true").length,
  },
  baselineEvaluation: {
    direct_dependency_ranking: "not_evaluable_without_cutoff-valid controls",
    package_age_ranking: "not_evaluable_without_cutoff-valid controls",
    multivariate_logistic_regression: "blocked: all retained snapshots are event records, not labeled negatives",
    probability_calibration: "blocked: no evaluation population or independent positive-family count",
    pr_auc_and_recall_at_k: "blocked: requires positives and a defensible non-event population",
  },
  calibrationInference: "blocked",
  blockingConditions: [
    `Only ${exact.length} exact pre-event snapshots are available.`,
    `Only ${distinctFamilies.length} independent incident families are represented.`,
    "No cutoff-valid, independently adjudicated control population is available.",
    "Current structural and workflow metrics cannot be joined as historical features.",
  ],
  nextDataGate: "Acquire at least ten strict future positives from five or more incident families and pre-register a cutoff-valid control design before fitting or calibrating any ranking model.",
  provenance: diagnostics.provenance,
};

await writeFile(path.join(researchDir, "66_temporal_baseline_and_calibration_gate.json"), JSON.stringify(report, null, 2) + "\n");
console.log(JSON.stringify({ exactPreEventSnapshots: report.exactPreEventSnapshots, distinctIncidentFamilies: distinctFamilies.length, calibrationInference: report.calibrationInference }, null, 2));
