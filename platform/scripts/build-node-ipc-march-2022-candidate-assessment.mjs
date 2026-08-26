import { writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const packageName = "node-ipc";
const affectedVersions = ["10.1.1", "10.1.2"];
const registryUrl = `https://registry.npmjs.org/${packageName}`;
const response = await fetch(registryUrl, {
  headers: {
    Accept: "application/json",
    "User-Agent": "supply-chain-research-node-ipc-march-2022/1.0",
  },
});
if (!response.ok) throw new Error(`Registry request failed: ${response.status}`);

const registry = await response.json();
const affected = affectedVersions.map((version) => ({
  version,
  publishedUtc: registry.time?.[version] ?? null,
}));
if (affected.some(({ publishedUtc }) => !publishedUtc)) {
  throw new Error("Missing affected-version timestamp.");
}

const earliestAffectedVersion = [...affected].sort(
  (a, b) => Date.parse(a.publishedUtc) - Date.parse(b.publishedUtc),
)[0];
const strictFeatureCutoffUtc = new Date(
  Date.parse(earliestAffectedVersion.publishedUtc) - 1,
).toISOString();
const selectedPreEventVersion = Object.entries(registry.time)
  .filter(
    ([version, timestamp]) =>
      !["created", "modified"].includes(version) &&
      Date.parse(timestamp) <= Date.parse(strictFeatureCutoffUtc),
  )
  .sort((a, b) => Date.parse(a[1]) - Date.parse(b[1]))
  .at(-1)?.[0] ?? null;
const selectedPreEventVersionObjectRetained = Boolean(
  selectedPreEventVersion && registry.versions?.[selectedPreEventVersion],
);
const decision = selectedPreEventVersionObjectRetained
  ? "eligible_for_governed_primary_temporal_ledger_reconstruction"
  : "exclude_from_primary_temporal_ledger_due_to_no_retained_strict_pre_event_source_object";

const output = {
  study: "node-ipc-march-2022-bounded-package-event-candidate-assessment",
  decision,
  candidate: {
    packageName,
    affectedVersions,
    earliestAffectedVersion,
    strictFeatureCutoffUtc,
    selectedPreEventVersion,
    selectedPreEventVersionObjectRetained,
    proposedFamilyId: "node_ipc_march_2022_maintainer_protestware",
    distinctFromExistingNodeIpc2026Record: true,
  },
  corroboration: {
    reviewedGithubAdvisory: "https://github.com/advisories/GHSA-97m3-w2cp-4xx6",
    independentSnykReport: "https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/",
    independentNvdRecord: "https://nvd.nist.gov/vuln/detail/CVE-2022-23812",
    officialRegistry: registryUrl,
  },
  zeroOutputsUntilReconstruction: {
    ledgerRows: 0,
    families: 0,
    validationUnits: 0,
    snapshots: 0,
    controls: 0,
    models: 0,
    predictiveMetrics: 0,
  },
  prohibitedInterpretations: [
    "No registry survival, advisory absence, or current state is a benign control.",
    "No historical installation, dependency reach, blast-radius, score, model, ranking, interval, calibration, or predictive metric is created.",
  ],
};

await writeFile(
  path.join(root, "research", "123_node_ipc_march_2022_candidate_assessment.json"),
  `${JSON.stringify(output, null, 2)}\n`,
);
console.log(
  JSON.stringify(
    { decision, earliestAffectedVersion, selectedPreEventVersion, selectedPreEventVersionObjectRetained },
    null,
    2,
  ),
);
