import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const repositoryCommit = {
  sha: "6de6e895805a8415f4cc6093f870587a768c67cd",
  committedAtUtc: "2026-08-24T09:05:46Z",
};
const manifestUrl = `https://raw.githubusercontent.com/DataDog/malicious-software-packages-dataset/${repositoryCommit.sha}/samples/npm/manifest.json`;

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

const ledger = parseCsv(await readFile(path.join(researchDir, "64_temporal_package_event_ledger.csv"), "utf8"));
const manifestResponse = await fetch(manifestUrl, { headers: { Accept: "application/json", "User-Agent": "supply-chain-research-datadog-overlap/1.0" } });
if (!manifestResponse.ok) throw new Error(`DataDog manifest request failed (${manifestResponse.status}).`);
const manifestText = await manifestResponse.text();
const manifest = JSON.parse(manifestText);
const overlap = ledger.map(row => {
  const affected = row.affected_versions.split("|");
  const entry = Object.prototype.hasOwnProperty.call(manifest, row.package_name) ? manifest[row.package_name] : undefined;
  const listed = Array.isArray(entry) ? entry : [];
  const matchingVersions = affected.filter(version => listed.includes(version));
  const membership = entry === undefined
    ? "package_not_present_in_current_positive_manifest"
    : entry === null
      ? "package_present_versions_unspecified"
      : matchingVersions.length
        ? "exact_affected_version_membership"
        : "package_present_no_exact_affected_version_match";
  return {
    record_id: row.record_id,
    package_name: row.package_name,
    primary_affected_versions: affected,
    event_family: row.event_family,
    primary_event_start_utc: row.event_start_utc,
    positive_membership_status: membership,
    matching_versions: matchingVersions,
    manifest_listed_versions: listed,
    permitted_use: "candidate_positive_membership_corroboration_only",
    prohibited_use: "not a primary label time, evidence source, incident-family assignment, benign label, or control observation",
  };
});
const output = {
  study: "datadog-positive-membership-overlap",
  generatedAtUtc: new Date().toISOString(),
  source: {
    manifestUrl,
    manifestSha256: createHash("sha256").update(manifestText).digest("hex"),
    repositoryCommitSha: repositoryCommit.sha,
    repositoryCommitUtc: repositoryCommit.committedAtUtc,
  },
  summary: {
    primaryRecordsChecked: overlap.length,
    exactAffectedVersionMembership: overlap.filter(item => item.positive_membership_status === "exact_affected_version_membership").length,
    packagePresentVersionsUnspecified: overlap.filter(item => item.positive_membership_status === "package_present_versions_unspecified").length,
    packagePresentNoExactVersionMatch: overlap.filter(item => item.positive_membership_status === "package_present_no_exact_affected_version_match").length,
    packageNotPresent: overlap.filter(item => item.positive_membership_status === "package_not_present_in_current_positive_manifest").length,
    newPrimaryLabelsCreated: 0,
    controlsCreated: 0,
  },
  interpretation: "The current positive-only manifest can corroborate listed package/version membership but supplies no event time, primary evidence URL, campaign grouping, or negative/control population. The pre-registered ledger remains authoritative for all primary temporal labels.",
  records: overlap,
};
await writeFile(path.join(researchDir, "80_datadog_positive_membership_overlap.json"), JSON.stringify(output, null, 2) + "\n");
console.log(JSON.stringify(output.summary, null, 2));
