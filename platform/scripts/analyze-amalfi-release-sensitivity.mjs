import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

function parseCsv(text) {
  const records = [];
  let row = [];
  let value = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    if (character === '"') {
      if (quoted && text[index + 1] === '"') { value += '"'; index += 1; } else quoted = !quoted;
    } else if (character === "," && !quoted) { row.push(value); value = ""; }
    else if ((character === "\n" || character === "\r") && !quoted) {
      if (character === "\r" && text[index + 1] === "\n") index += 1;
      row.push(value); value = "";
      if (row.length) records.push(row);
      row = [];
    } else value += character;
  }
  if (value || row.length) { row.push(value); records.push(row); }
  const [header, ...rows] = records;
  return rows.filter(row => row.length === header.length).map(row => Object.fromEntries(header.map((column, index) => [column, row[index] ?? ""])));
}

const ledger = parseCsv(await readFile(path.join(researchDir, "77_amalfi_release_sensitivity_ledger.csv"), "utf8"));
const labels = ["malicious", "benign"];
const byLabel = Object.fromEntries(labels.map(label => {
  const rows = ledger.filter(row => row.corpus_analysis_label === label);
  return [label, {
    explicitLabelRows: rows.length,
    retainedRegistryVersionObjects: rows.filter(row => row.registry_snapshot_status === "registry_reconstructed").length,
    versionNotRetained: rows.filter(row => row.registry_snapshot_status === "version_not_retained").length,
    otherUnavailable: rows.filter(row => !["registry_reconstructed", "version_not_retained"].includes(row.registry_snapshot_status)).length,
    distinctPackages: new Set(rows.map(row => row.package_name)).size,
  }];
}));
const mixedLabelPackages = new Set(labels.flatMap(label => ledger.filter(row => row.corpus_analysis_label === label).map(row => row.package_name))).size;
const diagnostics = {
  study: "amalfi-release-sensitivity-control-frame-decision",
  generatedAtUtc: new Date().toISOString(),
  summary: {
    explicitLabelRows: ledger.length,
    labelCounts: byLabel,
    retainedRegistryVersionObjects: ledger.filter(row => row.registry_snapshot_status === "registry_reconstructed").length,
    unavailableOrMissingVersions: ledger.filter(row => row.registry_snapshot_status !== "registry_reconstructed").length,
    distinctPackagesAcrossLabels: mixedLabelPackages,
  },
  decision: {
    primaryFutureCompromiseControlFrame: "blocked",
    rationale: [
      "The artifact provides release-classification labels, not per-row future-outcome or review-horizon timestamps.",
      "The basic corpus is a case-centred detection corpus, not an explicitly sampled at-risk npm population for the independently adjudicated incident families.",
      "688 of 1,790 corpus versions are not retained as current registry version objects, producing outcome-linked availability attrition that must not be imputed.",
    ],
    allowedSensitivityUse: "The 1,102 retained version objects may support separately labelled retrospective release-classification provenance/descriptive work only, with package-grouped separation and no transfer of any metric to the primary future-compromise benchmark.",
  },
  prohibitedInterpretations: [
    "Do not call the benign rows generic no-known-event controls.",
    "Do not merge these labels with the independently adjudicated incident ledger or treat package/version rows as independent incident families.",
    "Do not report PR-AUC, recall, calibration, blast radius, attack return, or compromise-ranking results for the primary benchmark from this corpus.",
  ],
};
await writeFile(path.join(researchDir, "78_amalfi_release_sensitivity_gate.json"), JSON.stringify(diagnostics, null, 2) + "\n");
console.log(JSON.stringify(diagnostics, null, 2));
