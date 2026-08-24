import { createHash } from "node:crypto";
import { createInflateRaw } from "node:zlib";
import { createWriteStream } from "node:fs";
import { readFile, writeFile } from "node:fs/promises";
import { once } from "node:events";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { StringDecoder } from "node:string_decoder";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const allowIncomplete = process.argv.includes("--allow-incomplete");

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

const snapshots = parseCsv(await readFile(path.join(researchDir, "65_package_temporal_companion_snapshots.csv"), "utf8"));
const targets = new Map(snapshots.filter(row => row.snapshot_status === "registry_reconstructed_exact").map(row => [
  `${row.package_name}@${row.pre_event_latest_version}`,
  {
    recordId: row.record_id,
    packageName: row.package_name,
    sourceVersion: row.pre_event_latest_version,
    cutoffUtc: row.feature_cutoff_utc,
    cutoffSql: row.feature_cutoff_utc.replace("T", " ").replace(/\.\d{3}Z$/, ""),
  },
]));

const outputPath = path.join(researchDir, "73_chrono_resolution_candidate_interval_rows.jsonl");
const output = createWriteStream(outputPath);
const compressedHash = createHash("sha256");
const inflater = createInflateRaw();
const decoder = new StringDecoder("utf8");
let remainder = "";
let compressedBytes = 0;
let decompressedBytes = 0;
let matchedRows = 0;
let copiedRows = 0;
let inputEnded = false;
let inflaterError = null;

function coversCutoff(start, end, cutoffSql) {
  const afterStart = start <= cutoffSql;
  const beforeEnd = end === "\\N" || end === "" || end.toLowerCase() === "infinity" || cutoffSql < end;
  return afterStart && beforeEnd;
}

function processLine(line) {
  if (!line.startsWith("npm\t")) return;
  const columns = line.split("\t");
  if (columns.length < 9) return;
  const target = targets.get(`${columns[1]}@${columns[2]}`);
  if (!target) return;
  matchedRows += 1;
  if (!coversCutoff(columns[7], columns[8], target.cutoffSql)) return;
  const row = {
    record_id: target.recordId,
    source_package: target.packageName,
    source_version: target.sourceVersion,
    feature_cutoff_utc: target.cutoffUtc,
    ecosystem: columns[0],
    dependency: columns[3],
    dependency_constraint: columns[4],
    dependency_version: columns[5],
    dependency_highest_version: columns[6],
    interval_start_raw: columns[7],
    interval_end_raw: columns[8],
    source_fidelity: "chrono_resolution_interval_row_timezone_unverified",
    interpretation_limit: "The CHRONO-RESOLUTION schema uses timestamp without time zone. This row is a candidate interval match under lexical UTC-normalized comparison pending explicit upstream timezone confirmation; it is not a transitive edge or install trace.",
  };
  output.write(JSON.stringify(row) + "\n");
  copiedRows += 1;
}

inflater.on("data", chunk => {
  decompressedBytes += chunk.length;
  const text = remainder + decoder.write(chunk);
  const lines = text.split("\n");
  remainder = lines.pop() ?? "";
  for (const line of lines) processLine(line);
});
inflater.on("error", error => { inflaterError = error; });
process.stdin.on("data", chunk => { compressedBytes += chunk.length; compressedHash.update(chunk); });
process.stdin.pipe(inflater);
await once(process.stdin, "end");
inputEnded = true;
await new Promise(resolve => setTimeout(resolve, 20));
if (!inflaterError && remainder) processLine(remainder + decoder.end());
if (inflaterError && !allowIncomplete) throw inflaterError;
await new Promise(resolve => output.end(resolve));

const diagnostics = {
  study: "chrono-resolution-streamed-candidate-interval-extraction",
  generatedAtUtc: new Date().toISOString(),
  input: {
    archive: "https://zenodo.org/records/17576373/files/chrono-resolution.zip?download=1",
    compression: "raw deflate member data-relations.sql",
    completeStream: !inflaterError && inputEnded,
    compressedBytes,
    compressedSha256: compressedHash.digest("hex"),
    decompressedBytes,
  },
  eligiblePilotSources: [...targets.values()].map(target => ({ recordId: target.recordId, package: target.packageName, version: target.sourceVersion, cutoffUtc: target.cutoffUtc })),
  rowsWithMatchingPackageVersion: matchedRows,
  candidateRowsCoveringCutoff: copiedRows,
  timestampSemantics: "Schema declares timestamp without time zone. Candidate interval matching normalizes the frozen UTC cutoff to YYYY-MM-DD HH:MM:SS for lexical comparison; this fidelity remains timezone_unverified until source documentation or author confirmation supplies a timezone convention.",
  prohibitedInterpretations: [
    "Candidate interval rows are not a complete relation table unless the entire compressed stream was processed successfully.",
    "No transitive traversal, downstream reach, centrality, blast-radius, model ranking, or calibration is computed.",
    "No candidate row is an observed npm installation or package-lock trace.",
  ],
  streamError: inflaterError ? { name: inflaterError.name, message: inflaterError.message } : null,
};
await writeFile(path.join(researchDir, "73_chrono_resolution_candidate_interval_diagnostics.json"), JSON.stringify(diagnostics, null, 2) + "\n");
console.log(JSON.stringify({ completeStream: diagnostics.input.completeStream, compressedBytes, decompressedBytes, matchedRows, copiedRows, streamError: diagnostics.streamError }, null, 2));
