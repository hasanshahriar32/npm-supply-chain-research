import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");

function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const character = text[index];
    const next = text[index + 1];
    if (character === '"' && quoted && next === '"') {
      field += '"';
      index += 1;
    } else if (character === '"') {
      quoted = !quoted;
    } else if (character === "," && !quoted) {
      row.push(field);
      field = "";
    } else if ((character === "\n" || character === "\r") && !quoted) {
      if (character === "\r" && next === "\n") index += 1;
      row.push(field);
      if (row.some((value) => value.length > 0)) rows.push(row);
      row = [];
      field = "";
    } else {
      field += character;
    }
  }
  if (field.length > 0 || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  const [header, ...dataRows] = rows;
  return dataRows.map((dataRow) => Object.fromEntries(header.map((column, index) => [column, dataRow[index] ?? ""])));
}

function canonicalRepository(value) {
  if (typeof value !== "string" || value.length === 0) return null;
  const normalized = value.trim().replace(/^git\+/, "").replace(/\.git$/, "");
  return normalized.length > 0 ? normalized : null;
}

function repositoryDescriptor(version) {
  if (typeof version?.repository === "string") return canonicalRepository(version.repository);
  if (version?.repository && typeof version.repository === "object") return canonicalRepository(version.repository.url);
  return null;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

async function getRegistry(packageName) {
  const response = await fetch(`https://registry.npmjs.org/${encodeURIComponent(packageName)}`, {
    headers: { Accept: "application/json", "User-Agent": "supply-chain-research-release-authority-audit/1.0" },
  });
  const body = await response.text();
  if (!response.ok) throw new Error(`Registry request for ${packageName} failed (${response.status}).`);
  return { metadata: JSON.parse(body), sha256: sha256(body) };
}

const snapshots = parseCsv(await readFile(path.join(researchDir, "65_package_temporal_companion_snapshots.csv"), "utf8"));
const exactSnapshots = snapshots.filter((snapshot) => snapshot.snapshot_status === "registry_reconstructed_exact");
if (exactSnapshots.length !== 12) {
  throw new Error(`Expected 12 exact snapshots, found ${exactSnapshots.length}.`);
}

const records = [];
for (const snapshot of exactSnapshots) {
  const { metadata, sha256: registryResponseSha256 } = await getRegistry(snapshot.package_name);
  const selectedVersion = snapshot.pre_event_latest_version;
  const selectedTime = Date.parse(snapshot.pre_event_latest_published_utc);
  const selected = metadata.versions?.[selectedVersion];
  if (!selected || !Number.isFinite(selectedTime)) {
    throw new Error(`Selected retained source version is unavailable for ${snapshot.record_id}.`);
  }
  const predecessorTimeline = Object.entries(metadata.time ?? {})
    .filter(([version, timestamp]) => version !== "created" && version !== "modified" && version !== selectedVersion && Number.isFinite(Date.parse(timestamp)) && Date.parse(timestamp) < selectedTime && metadata.versions?.[version])
    .map(([version, timestamp]) => ({ version, timestamp, ms: Date.parse(timestamp) }))
    .sort((left, right) => left.ms - right.ms);
  const predecessor = predecessorTimeline.at(-1);
  const predecessorObject = predecessor ? metadata.versions?.[predecessor.version] : null;
  const selectedRepository = repositoryDescriptor(selected);
  const predecessorRepository = predecessorObject ? repositoryDescriptor(predecessorObject) : null;
  const selectedDist = selected.dist ?? {};
  const predecessorDist = predecessorObject?.dist ?? {};

  records.push({
    record_id: snapshot.record_id,
    package_name: snapshot.package_name,
    event_family: snapshot.event_family,
    feature_cutoff_utc: snapshot.feature_cutoff_utc,
    selected_pre_event_version: selectedVersion,
    selected_pre_event_published_utc: snapshot.pre_event_latest_published_utc,
    immediate_prior_retained_version: predecessor?.version ?? null,
    immediate_prior_retained_published_utc: predecessor ? new Date(predecessor.ms).toISOString() : null,
    predecessor_available: Boolean(predecessorObject),
    selected_repository_descriptor_present: Boolean(selectedRepository),
    predecessor_repository_descriptor_present: Boolean(predecessorRepository),
    repository_descriptor_comparison_available: Boolean(selectedRepository && predecessorRepository),
    selected_git_head_present: Boolean(selected.gitHead),
    predecessor_git_head_present: Boolean(predecessorObject?.gitHead),
    git_head_comparison_available: Boolean(selected.gitHead && predecessorObject?.gitHead),
    selected_publish_config_present: Boolean(selected.publishConfig),
    predecessor_publish_config_present: Boolean(predecessorObject?.publishConfig),
    publish_config_comparison_available: Boolean(selected.publishConfig && predecessorObject?.publishConfig),
    selected_dist_integrity_present: Boolean(selectedDist.integrity),
    predecessor_dist_integrity_present: Boolean(predecessorDist.integrity),
    selected_dist_shasum_present: Boolean(selectedDist.shasum),
    predecessor_dist_shasum_present: Boolean(predecessorDist.shasum),
    selected_maintainers_embedded: Array.isArray(selected.maintainers) && selected.maintainers.length > 0,
    predecessor_maintainers_embedded: Array.isArray(predecessorObject?.maintainers) && predecessorObject.maintainers.length > 0,
    retained_metadata_interpretation: "availability_only_no_values_or_deltas_extracted",
    registry_response_sha256: registryResponseSha256,
  });
}

const count = (field) => records.filter((record) => record[field]).length;
const output = {
  study: "strict-pre-event-release-authority-metadata-availability-audit",
  artifactVersion: 1,
  executionStatus: "availability_audit_only_no_feature_values_deltas_scores_or_models",
  generatedAtUtc: new Date().toISOString(),
  input: {
    strictSnapshotArtifact: "research/65_package_temporal_companion_snapshots.csv",
    exactPreEventSourceSnapshots: exactSnapshots.length,
    excludedSnapshotStatuses: snapshots.filter((snapshot) => snapshot.snapshot_status !== "registry_reconstructed_exact").map((snapshot) => ({ recordId: snapshot.record_id, status: snapshot.snapshot_status })),
  },
  scope: {
    retainedMetadataObject: "The selected version object from the official npm registry response, plus only the immediate earlier retained version object by publication time.",
    strictTemporalBoundary: "All selected versions precede their incident event cutoff. The audit never reads a malicious release as a feature object.",
    nonUseOfCurrentState: "Package root metadata, current dist-tags, current maintainers, current repository state, GitHub workflow state, download counts, and dependency graphs are excluded.",
    noValueExtraction: "Only boolean availability fields and version identifiers are retained. Repository URLs, git heads, publisher names, maintainer identities, tarball URLs, hashes, config values, and any equality or change delta are not emitted.",
  },
  records,
  summary: {
    exactPreEventSourceSnapshots: records.length,
    predecessorAvailable: count("predecessor_available"),
    repositoryDescriptorComparisonAvailable: count("repository_descriptor_comparison_available"),
    gitHeadComparisonAvailable: count("git_head_comparison_available"),
    publishConfigComparisonAvailable: count("publish_config_comparison_available"),
    selectedDistIntegrityPresent: count("selected_dist_integrity_present"),
    selectedEmbeddedMaintainersPresent: count("selected_maintainers_embedded"),
    featureValuesExtracted: 0,
    deltasClassified: 0,
    releaseAuthorityScoresComputed: 0,
    controlsCreated: 0,
    modelsFitted: 0,
    predictiveMetricsComputed: 0,
  },
  permittedInterpretations: [
    "This artifact states whether limited retained fields are available in strict pre-event source and immediate-predecessor version objects.",
    "A present field means only that the current registry response retains that field on the frozen version object; it is not evidence of trustworthy authority, compromise, or risk.",
    "A missing field is an availability condition, not a hygiene, benign, or no-known-event label.",
  ],
  prohibitedInterpretations: [
    "Do not use repository, gitHead, publishConfig, dist, or embedded-maintainer availability as a release-authority score.",
    "Do not infer a historical maintainer transition, publisher change, repository transfer, provenance change, or workflow change from the retained fields.",
    "Do not compare or emit metadata values, classify field differences, rank records, fit a model, estimate an effect, or calculate predictive metrics.",
    "Do not combine this availability audit with current registry root state, current repository state, current workflow data, controls, or incident absence.",
  ],
};

await writeFile(path.join(researchDir, "95_release_authority_metadata_availability_audit.json"), `${JSON.stringify(output, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ exactSnapshots: output.summary.exactPreEventSourceSnapshots, predecessorAvailable: output.summary.predecessorAvailable, repositoryDescriptorComparisonAvailable: output.summary.repositoryDescriptorComparisonAvailable, gitHeadComparisonAvailable: output.summary.gitHeadComparisonAvailable, featureValuesExtracted: output.summary.featureValuesExtracted, scores: output.summary.releaseAuthorityScoresComputed }, null, 2));
