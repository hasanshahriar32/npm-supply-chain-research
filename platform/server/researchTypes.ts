export type ResearchDocument = {
  slug: string;
  title: string;
  category: "literature" | "gap" | "methodology" | "benchmark" | "governance";
  sourceFile: string;
  summary: string;
};

export type LiteratureStudy = {
  study_id: string;
  study: string;
  year: string;
  ecosystem: string;
  task: string;
  unit_or_data: string;
  method: string;
  main_finding_or_contribution: string;
  closest_overlap: string;
  limitation_for_proposed_task: string;
  source_url: string;
};

export type BenchmarkSnapshot = {
  packages: number;
  versions: number;
  maintainers: number;
  dependencyEdges: number;
  repositoryMappings: number;
  workflowChecks: number;
  workflowCoverage: number;
  advisoryRecords: number;
  metricsRecords: number;
};

export type IncidentLabel = {
  id: string;
  name: string;
  incidentType: string;
  eventDate: string;
  scope: string;
  assessment: string;
  evidenceSource: string;
  status: "confirmed" | "review";
};

export type ExperimentResult = {
  id: string;
  model: string;
  featureSet: string;
  evaluation: string;
  status: "planned" | "baseline" | "blocked";
  note: string;
};
