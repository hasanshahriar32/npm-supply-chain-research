import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const researchDir = path.join(root, "research");
const availabilityPath = path.join(researchDir, "95_release_authority_metadata_availability_audit.json");
const deltaProtocolPath = path.join(researchDir, "96_release_authority_delta_semantics_protocol.json");
const outputPath = path.join(researchDir, "97_official_npm_provenance_attestation_access_assessment.json");

const [availabilityText, deltaProtocolText] = await Promise.all([
  readFile(availabilityPath, "utf8"),
  readFile(deltaProtocolPath, "utf8"),
]);
const availability = JSON.parse(availabilityText);
const deltaProtocol = JSON.parse(deltaProtocolText);

if (!Number.isInteger(availability.summary?.exactPreEventSourceSnapshots) || availability.summary.exactPreEventSourceSnapshots <= 0) {
  throw new Error("The provenance-access screen requires at least one strict source snapshot from the availability audit.");
}
if (deltaProtocol.currentDecision?.observedDeltasClassified !== 0) {
  throw new Error("The input delta protocol must not contain observed deltas.");
}

const output = {
  study: "official-npm-provenance-attestation-access-assessment",
  artifactVersion: 1,
  assessmentDateUtc: new Date().toISOString(),
  decision: "metadata_only_version_specific_attestation_access_not_established",
  sourceInputs: {
    strictAvailabilityAudit: {
      path: "research/95_release_authority_metadata_availability_audit.json",
      sha256: createHash("sha256").update(availabilityText).digest("hex"),
      exactPreEventSourceSnapshots: availability.summary.exactPreEventSourceSnapshots,
    },
    futureDeltaSemanticsProtocol: {
      path: "research/96_release_authority_delta_semantics_protocol.json",
      sha256: createHash("sha256").update(deltaProtocolText).digest("hex"),
      attestationDeltaTypeDeclared: deltaProtocol.deltaOntology.some((entry) => entry.deltaType === "verifiable_provenance_attestation_state_transition"),
    },
  },
  officialDocumentationScreen: {
    npmProvenanceDocumentation: {
      url: "https://docs.npmjs.com/generating-provenance-statements",
      documentedMechanism: "npm audit signatures verifies provenance attestations for downloaded package dependency sets.",
      documentedLimit: "Established provenance does not guarantee that a package has no malicious code.",
    },
    npmRegistryApiDocumentation: {
      url: "https://api-docs.npmjs.com/",
      documentedObservation: "The public Registry API reference reviewed during this assessment does not document a public unauthenticated endpoint for retrieving a version-specific attestation bundle as metadata-only evidence.",
    },
    provenanceAnnouncement: {
      url: "https://github.blog/security/supply-chain-security/introducing-npm-package-provenance/",
      documentedContext: "Provenance links a package to source and build instructions, but is not a compromise or benignness label.",
    },
  },
  boundedAccessDecision: {
    strictPreEventVersionsEligibleForFutureScreen: availability.summary.exactPreEventSourceSnapshots,
    documentedMetadataOnlyVersionSpecificRetrievalPath: false,
    endpointGuessingPermitted: false,
    packagePayloadDownloadPermitted: false,
    installationPermitted: false,
    signatureVerificationRunPermitted: false,
    result: "No package-version attestation retrieval was attempted because the reviewed official materials did not establish a bounded, documented, metadata-only retrieval endpoint. The documented verification mechanism is dependency-set oriented and would require downloaded packages, which is outside this assessment's access policy.",
  },
  counts: {
    versionSpecificEndpointRequestsAttempted: 0,
    undocumentedEndpointsGuessed: 0,
    packagePayloadsDownloaded: 0,
    packagesInstalled: 0,
    attestationBundlesRetrieved: 0,
    signatureVerificationRuns: 0,
    attestationStatesClassified: 0,
    controlsCreated: 0,
    authorityScoresComputed: 0,
    modelsFitted: 0,
    rankingsComputed: 0,
    predictiveMetricsComputed: 0,
  },
  permittedInterpretations: [
    "The official documentation supports provenance as a verifiable release-time linkage concept and establishes a documented verification mechanism for downloaded dependency sets.",
    "The strict pre-event ledger has twelve candidate source versions that could be screened in a future authorized or officially documented metadata-only access path.",
    "This result is an access-contract finding, not an attestation-state observation for any package version.",
  ],
  prohibitedInterpretations: [
    "Do not infer that any strict pre-event version lacks an attestation because no metadata-only access path was established.",
    "Do not use current npm package badges, current provenance views, current repository state, or current transparency-log search results as historical attestation evidence.",
    "Do not download packages, install dependencies, guess registry endpoints, execute npm audit signatures, or retrieve an attestation bundle under this assessment.",
    "Do not create controls, benign labels, authority scores, rankings, models, or predictive metrics from this access assessment.",
  ],
};

await writeFile(outputPath, `${JSON.stringify(output, null, 2)}\n`, "utf8");
console.log(JSON.stringify({ outputPath, decision: output.decision, strictVersionsEligible: output.boundedAccessDecision.strictPreEventVersionsEligibleForFutureScreen, endpointRequests: output.counts.versionSpecificEndpointRequestsAttempted, downloads: output.counts.packagePayloadsDownloaded, attestationStates: output.counts.attestationStatesClassified }, null, 2));
