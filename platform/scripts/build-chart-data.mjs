import { execFileSync } from "node:child_process";
import fs from "node:fs/promises";
import path from "node:path";

const projectRoot = path.resolve(import.meta.dirname, "..");
const archivePath = path.resolve(projectRoot, "..", "repo-inspection", "repo", "data", "metrics_summary.csv.zip");
const outputPath = path.join(projectRoot, "research", "benchmark_chart_data.json");

function parseCsvLine(line) {
  const values = [];
  let value = "";
  let quoted = false;
  for (const char of line) {
    if (char === '"') quoted = !quoted;
    else if (char === "," && !quoted) { values.push(value); value = ""; }
    else value += char;
  }
  values.push(value);
  return values.map((item) => item.replace(/^"|"$/g, "").trim());
}

const raw = execFileSync("unzip", ["-p", archivePath], { encoding: "utf8", maxBuffer: 32 * 1024 * 1024 });
const [header, ...lines] = raw.trim().split(/\r?\n/);
const fields = parseCsvLine(header);
const records = lines.map((line) => Object.fromEntries(fields.map((field, index) => [field, parseCsvLine(line)[index] ?? ""])));

const bucketDefinitions = [
  { label: "0", min: 0, max: 0 },
  { label: "1", min: 1, max: 1 },
  { label: "2", min: 2, max: 2 },
  { label: "3–5", min: 3, max: 5 },
  { label: "6+", min: 6, max: Number.POSITIVE_INFINITY },
];

const blastRadiusDistribution = bucketDefinitions.map((bucket) => ({
  bucket: bucket.label,
  packages: records.filter((record) => {
    const value = Number(record.blast_radius);
    return value >= bucket.min && value <= bucket.max;
  }).length,
}));

const topBlastRadius = [...records]
  .sort((a, b) => Number(b.blast_radius) - Number(a.blast_radius) || Number(b.transitive_dependents) - Number(a.transitive_dependents))
  .slice(0, 10)
  .map((record) => ({ packageName: record.package_name, blastRadius: Number(record.blast_radius), transitiveDependents: Number(record.transitive_dependents) }));

const topAttackerRoi = [...records]
  .sort((a, b) => Number(b.attacker_roi) - Number(a.attacker_roi))
  .slice(0, 10)
  .map((record) => ({ packageName: record.package_name, attackerRoi: Number(Number(record.attacker_roi).toFixed(3)), blastRadius: Number(record.blast_radius) }));

await fs.writeFile(outputPath, `${JSON.stringify({
  source: "data/metrics_summary.csv.zip",
  generatedAt: new Date().toISOString(),
  recordCount: records.length,
  blastRadiusDistribution,
  topBlastRadius,
  topAttackerRoi,
}, null, 2)}\n`);

console.log(`Wrote ${outputPath} from ${records.length} real metric records.`);
