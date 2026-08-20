import { createHash } from "node:crypto";
import { mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import AdmZip from "adm-zip";

const [archivePath, outputDirectory] = process.argv.slice(2);

if (!archivePath || !outputDirectory) {
  throw new Error("Usage: node scripts/analyze-structural-leverage.mjs <metrics_summary.csv.zip> <output-directory>");
}

const numericFields = [
  "wormability_max",
  "wormability_sum",
  "blast_radius",
  "direct_dependents",
  "direct_dependents_with_workflows",
  "transitive_dependents",
  "attacker_roi",
];

function parseCsv(text) {
  const [headerLine, ...dataLines] = text.trim().split(/\r?\n/);
  const headers = headerLine.split(",");

  return dataLines.map((line) => {
    const cells = line.split(",");
    const row = Object.fromEntries(headers.map((header, index) => [header, cells[index] ?? ""]));
    for (const field of numericFields) row[field] = Number(row[field]);
    return row;
  });
}

function quantile(values, probability) {
  const sorted = [...values].sort((a, b) => a - b);
  const position = (sorted.length - 1) * probability;
  const lower = Math.floor(position);
  const upper = Math.ceil(position);
  if (lower === upper) return sorted[lower];
  return sorted[lower] + (sorted[upper] - sorted[lower]) * (position - lower);
}

function describe(rows, field) {
  const values = rows.map((row) => row[field]);
  const total = values.reduce((sum, value) => sum + value, 0);
  return {
    min: Math.min(...values),
    p50: quantile(values, 0.5),
    p90: quantile(values, 0.9),
    p99: quantile(values, 0.99),
    max: Math.max(...values),
    mean: total / values.length,
    nonzeroCount: values.filter((value) => value > 0).length,
  };
}

function rank(values) {
  const indexed = values.map((value, index) => ({ value, index })).sort((a, b) => a.value - b.value);
  const output = Array(values.length);
  let start = 0;
  while (start < indexed.length) {
    let end = start;
    while (end + 1 < indexed.length && indexed[end + 1].value === indexed[start].value) end += 1;
    const averageRank = (start + 1 + end + 1) / 2;
    for (let cursor = start; cursor <= end; cursor += 1) output[indexed[cursor].index] = averageRank;
    start = end + 1;
  }
  return output;
}

function pearson(left, right) {
  const leftMean = left.reduce((sum, value) => sum + value, 0) / left.length;
  const rightMean = right.reduce((sum, value) => sum + value, 0) / right.length;
  let covariance = 0;
  let leftVariance = 0;
  let rightVariance = 0;
  for (let index = 0; index < left.length; index += 1) {
    const leftDelta = left[index] - leftMean;
    const rightDelta = right[index] - rightMean;
    covariance += leftDelta * rightDelta;
    leftVariance += leftDelta ** 2;
    rightVariance += rightDelta ** 2;
  }
  return covariance / Math.sqrt(leftVariance * rightVariance);
}

function spearman(rows, leftField, rightField) {
  return pearson(rank(rows.map((row) => row[leftField])), rank(rows.map((row) => row[rightField])));
}

function topRows(rows, field, count) {
  return [...rows]
    .sort((left, right) => right[field] - left[field] || left.package_name.localeCompare(right.package_name))
    .slice(0, count);
}

function csvEscape(value) {
  const text = String(value ?? "");
  return /[",\n]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

const archiveBytes = await readFile(archivePath);
const sourceSha256 = createHash("sha256").update(archiveBytes).digest("hex");
const zip = new AdmZip(archiveBytes);
const csvEntry = zip.getEntries().find((entry) => entry.entryName.endsWith(".csv"));

if (!csvEntry) throw new Error("The archive does not contain a CSV metrics file.");

const rows = parseCsv(zip.readAsText(csvEntry));
const reviewBudget = Math.ceil(rows.length * 0.01);
const topRoi = topRows(rows, "attacker_roi", reviewBudget);
const topReach = topRows(rows, "transitive_dependents", reviewBudget);
const topWorkflowReach = topRows(rows, "direct_dependents_with_workflows", reviewBudget);
const asSet = (items) => new Set(items.map((item) => item.package_name));
const roiSet = asSet(topRoi);
const reachSet = asSet(topReach);
const workflowSet = asSet(topWorkflowReach);
const intersection = (left, right) => [...left].filter((value) => right.has(value)).length;

const fieldSummary = Object.fromEntries(numericFields.map((field) => [field, describe(rows, field)]));
const summary = {
  analysisName: "current_snapshot_structural_leverage_audit",
  sourceArchive: path.basename(archivePath),
  sourceCsv: csvEntry.entryName,
  sourceSha256,
  recordCount: rows.length,
  generatedAt: new Date().toISOString(),
  scope: "Cross-sectional descriptive analysis only; it is not a pre-incident prediction evaluation.",
  fieldSummary,
  correlations: {
    spearman_attacker_roi_vs_transitive_dependents: spearman(rows, "attacker_roi", "transitive_dependents"),
    spearman_attacker_roi_vs_direct_dependents: spearman(rows, "attacker_roi", "direct_dependents"),
    spearman_attacker_roi_vs_workflow_bearing_direct_dependents: spearman(rows, "attacker_roi", "direct_dependents_with_workflows"),
    spearman_wormability_max_vs_transitive_dependents: spearman(rows, "wormability_max", "transitive_dependents"),
  },
  topOnePercentReviewBudget: reviewBudget,
  queueOverlap: {
    roi_and_reach: intersection(roiSet, reachSet),
    roi_and_workflow_reach: intersection(roiSet, workflowSet),
    reach_and_workflow_reach: intersection(reachSet, workflowSet),
    all_three: [...roiSet].filter((name) => reachSet.has(name) && workflowSet.has(name)).length,
  },
  caveats: [
    "The archive is a repository snapshot, not a complete npm census.",
    "The workflow-bearing dependent field is derived from public workflow-directory observations and is not a privilege or compromise measurement.",
    "Current cross-sectional metrics must not be used as historical features without dated reconstruction.",
    "The weighted attacker_roi field is retained only to audit the existing implementation; it is reported as a legacy structural score, not attacker utility.",
  ],
};

const topTable = topRows(rows, "attacker_roi", 50).map((row, index) => ({
  rank: index + 1,
  package_name: row.package_name,
  attacker_roi: row.attacker_roi,
  wormability_max: row.wormability_max,
  blast_radius: row.blast_radius,
  direct_dependents: row.direct_dependents,
  direct_dependents_with_workflows: row.direct_dependents_with_workflows,
  transitive_dependents: row.transitive_dependents,
}));

await mkdir(outputDirectory, { recursive: true });
await writeFile(path.join(outputDirectory, "51_current_snapshot_structural_analysis.json"), `${JSON.stringify(summary, null, 2)}\n`);
await writeFile(
  path.join(outputDirectory, "51_current_snapshot_top_legacy_structural_scores.csv"),
  [Object.keys(topTable[0]).join(","), ...topTable.map((row) => Object.values(row).map(csvEscape).join(","))].join("\n") + "\n",
);

console.log(JSON.stringify({ recordCount: rows.length, sourceSha256, reviewBudget, queueOverlap: summary.queueOverlap }, null, 2));
