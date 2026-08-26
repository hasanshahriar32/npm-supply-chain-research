import { createHash } from "node:crypto";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const outputPath = path.join(researchDir, "125_noblox_js_proxy_october_2021_candidate_assessment.json");

const sources = {
  sonatypeIncidentReport: "https://www.sonatype.com/blog/fake-npm-roblox-api-package-installs-ransomware-spooky-surprise",
  bleepingComputerReport: "https://www.bleepingcomputer.com/news/security/malicious-npm-libraries-install-ransomware-password-stealer/",
  npmRegistry: "https://registry.npmjs.org/noblox.js-proxy",
};

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

async function fetchText(url, accept) {
  const response = await fetch(url, {
    headers: {
      Accept: accept,
      "User-Agent": "supply-chain-research-noblox-js-proxy-candidate-assessment/1.0",
    },
  });
  const text = await response.text();
  return { ok: response.ok, status: response.status, text };
}

const [sonatype, bleepingComputer, registryResponse] = await Promise.all([
  fetchText(sources.sonatypeIncidentReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.bleepingComputerReport, "text/html, text/plain;q=0.9"),
  fetchText(sources.npmRegistry, "application/json"),
]);

if (!sonatype.ok || !sonatype.text.includes("noblox.js-proxy")) {
  throw new Error("The bounded Sonatype response does not retain the named noblox.js-proxy incident context.");
}
if (!bleepingComputer.ok || !bleepingComputer.text.includes("noblox.js-proxy")) {
  throw new Error("The bounded BleepingComputer response does not retain the named noblox.js-proxy incident context.");
}

const registry = registryResponse.ok ? JSON.parse(registryResponse.text) : null;
const retainedVersionTimes = registry
  ? Object.entries(registry.time ?? {})
      .filter(([version, publishedAt]) => version !== "created" && version !== "modified" && Number.isFinite(Date.parse(publishedAt)))
      .sort((left, right) => Date.parse(left[1]) - Date.parse(right[1]))
  : [];

const artifact = {
  study: "noblox-js-proxy-october-2021-bounded-package-event-candidate-assessment",
  artifactVersion: 1,
  artifactDate: new Date().toISOString().slice(0, 10),
  decision: "exclude_from_primary_temporal_ledger_due_to_no_independently_corroborated_finite_exact_affected_version_target",
  candidate: {
    recordId: "noblox-js-proxy-2021-10-26",
    packageName: "noblox.js-proxy",
    eventFamilyCandidate: "noblox_js_roblox_typosquatting_october_2021",
    relatednessStatus: "candidate is distinct from existing ledger families but creates no family or validation unit because the strict target gate fails",
    independentlyCorroboratedPackageName: true,
    independentlyCorroboratedAffectedVersions: null,
    eventPublicationContext: "Sonatype reported the second named package discovery on 2021-10-26; BleepingComputer independently reported the named malicious libraries on 2021-10-27.",
  },
  corroboration: {
    sonatypeIncidentReport: {
      publishedDate: "2021-10-27",
      statement: "Identifies noblox.js-proxy and noblox.js-proxies as malicious typosquatting packages, but the inspected text does not enumerate an exact affected version or finite version set.",
    },
    bleepingComputerReport: {
      publishedDate: "2021-10-27",
      statement: "Independently identifies noblox.js-proxy and noblox.js-proxies as malicious packages, but the inspected text does not enumerate an exact affected version or finite version set.",
    },
    officialRegistry: {
      boundedMetadataOnly: true,
      httpStatus: registryResponse.status,
      retainedVersionTimes,
      retainedVersionObjectKeys: Object.keys(registry?.versions ?? {}).sort(),
      inspectedForSourceObjectSelection: false,
      reason: "Registry metadata cannot create the missing event-specific exact target or substitute for a source’s finite affected-version assertion.",
    },
  },
  sourceProvenance: {
    sonatypeIncidentReport: { url: sources.sonatypeIncidentReport, httpStatus: sonatype.status, responseSha256: sha256(sonatype.text) },
    bleepingComputerReport: { url: sources.bleepingComputerReport, httpStatus: bleepingComputer.status, responseSha256: sha256(bleepingComputer.text) },
    npmRegistry: { url: sources.npmRegistry, httpStatus: registryResponse.status, responseSha256: sha256(registryResponse.text) },
  },
  strictExclusionReason: {
    requiredRule: "A primary ledger record requires independently corroborated exact affected release(s) or a finite exact version set before official registry time selection and strict pre-event source-object reconstruction.",
    observedState: "The independently corroborated source texts name the packages but do not specify a version-specific affected target. The official registry metadata response is not permitted to infer an affected release from package history or retention state.",
    consequence: "Do not add a primary ledger record, event cutoff, source snapshot, declaration, range selection, graph edge, incident family, validation unit, control, or outcome label for this candidate.",
  },
  currentDecision: {
    primaryLedgerRecordsAdded: 0,
    primaryLedgerFamiliesAdded: 0,
    futureValidationUnitsAdded: 0,
    exactPreEventSourceSnapshotsCreated: 0,
    dependencyDeclarationsCreated: 0,
    isolatedSemverApproximationsCreated: 0,
    recursiveGraphEdgesCreated: 0,
    controlsCreated: 0,
    benignLabelsCreated: 0,
    historicalInstallTracesCreated: 0,
    reachOrBlastRadiusValuesCreated: 0,
    scoresComputed: 0,
    modelsFitted: 0,
    rankingsComputed: 0,
    uncertaintyIntervalsComputed: 0,
    calibrationResultsCreated: 0,
    predictiveMetricsComputed: 0,
  },
  prohibitedInterpretations: [
    "This exclusion does not dispute the independently corroborated reports or turn noblox.js-proxy into a benign, safe, unchanged, no-known-event, or control row.",
    "The official registry response is used only to document bounded metadata availability; it cannot infer a finite affected version, historical installation, source snapshot, dependency graph, reach, or blast radius.",
    "This artifact creates no control frame, model, ranking, interval, calibration output, PR-AUC, Recall@K, or predictive result.",
  ],
};

await mkdir(researchDir, { recursive: true });
await writeFile(outputPath, `${JSON.stringify(artifact, null, 2)}\n`);
console.log(JSON.stringify({ decision: artifact.decision, registryHttpStatus: registryResponse.status, primaryLedgerRecordsAdded: artifact.currentDecision.primaryLedgerRecordsAdded }, null, 2));
