import type { GetServerSidePropsContext } from "next";
import Head from "next/head";
import { useRouter } from "next/router";
import { LiteratureMatrix } from "../../components/LiteratureMatrix";
import { MarkdownReader } from "../../components/MarkdownReader";
import { WorkspaceLayout } from "../../components/WorkspaceLayout";
import { getAuthenticatedUser } from "../../server/nextAuth";
import { trpc } from "../../lib/trpc";
import type { ExperimentResult, IncidentLabel } from "../../server/researchTypes";

type User = { name: string; role: string };

function PanelTitle({ title, note }: { title: string; note: string }) { return <div className="page-title"><h1>{title}</h1><p>{note}</p></div>; }
function Loading() { return <div className="admin-empty">Loading the repository-backed research source…</div>; }

function BenchmarkPanel() {
  const overview = trpc.research.overview.useQuery(undefined, { refetchInterval: 30_000 });
  if (!overview.data) return <Loading />;
  const { snapshot } = overview.data;
  const coverage = Math.round(snapshot.workflowCoverage * 100);
  return <><PanelTitle title="Benchmark Findings" note="Current repository snapshot; values are source-backed and refresh through the protected tRPC layer." /><div className="metric-grid"><div className="metric"><label>Packages</label><strong>{snapshot.packages.toLocaleString()}</strong><small>Current package nodes</small></div><div className="metric"><label>Dependency edges</label><strong>{snapshot.dependencyEdges.toLocaleString()}</strong><small>Observed relations</small></div><div className="metric"><label>Maintainers</label><strong>{snapshot.maintainers.toLocaleString()}</strong><small>Associated identities</small></div><div className="metric"><label>Workflow coverage</label><strong>{coverage}%</strong><small>{snapshot.workflowChecks.toLocaleString()} repository checks</small></div></div><div className="split-grid"><section className="data-card"><h3>Snapshot composition</h3><p>The data collection prototype contains package, version, dependency, maintainer, repository, workflow, advisory, and metric records. The benchmark is not yet a finished predictive model.</p><div className="bar-list"><div className="bar-row"><label><span>Repository mappings</span><span>{snapshot.repositoryMappings.toLocaleString()}</span></label><div className="bar"><i style={{ width: `${Math.round(snapshot.repositoryMappings / snapshot.packages * 100)}%` }} /></div></div><div className="bar-row"><label><span>Workflow detections</span><span>{Math.round(snapshot.workflowCoverage * snapshot.workflowChecks).toLocaleString()}</span></label><div className="bar"><i style={{ width: `${coverage}%` }} /></div></div><div className="bar-row"><label><span>Advisory records</span><span>{snapshot.advisoryRecords.toLocaleString()}</span></label><div className="bar"><i style={{ width: "82%" }} /></div></div></div></section><section className="data-card"><h3>Reading the metrics</h3><p>Shared-maintainer reach and public workflow observability are defensive features. They do not prove credential control, infrastructure privilege, exploitability, or attacker optimization.</p><div className="bar-list"><div className="bar-row"><label><span>Package metrics written</span><span>{snapshot.metricsRecords.toLocaleString()}</span></label><div className="bar"><i style={{ width: "100%" }} /></div></div><div className="bar-row"><label><span>Version records</span><span>{snapshot.versions.toLocaleString()}</span></label><div className="bar"><i style={{ width: "89%" }} /></div></div></div></section></div></>;
}

function IncidentPanel() {
  const query = trpc.research.incidents.useQuery();
  if (!query.data) return <Loading />;
  return <><PanelTitle title="Incident Labels" note="High-confidence historical anchors are stored as version- and campaign-aware evidence—not keyword-only advisory labels." /><section className="section-card">{(query.data as IncidentLabel[]).map((incident: IncidentLabel) => <div className="incident-row" key={incident.id}><div><h3>{incident.name}</h3><span className="eyebrow">{incident.eventDate}</span></div><div><p>{incident.scope}</p><p style={{ marginTop: 8 }}>{incident.assessment}</p></div><div><span className="tag">{incident.status}</span><p style={{ marginTop: 10 }}>{incident.evidenceSource}</p></div></div>)}</section><section className="data-card" style={{ marginTop: 26 }}><h3>Registry rule</h3><p>Each future record must retain package, affected version or range, incident family, event time, public detection time, evidence URLs, confidence, and an explicit inclusion or exclusion reason.</p></section></>;
}

function ExperimentPanel() {
  const query = trpc.research.experiments.useQuery();
  if (!query.data) return <Loading />;
  const experiments = query.data as ExperimentResult[];
  const measured = experiments.filter((experiment) => experiment.status === "baseline");
  const queue = experiments.filter((experiment) => experiment.status !== "baseline");
  return <><PanelTitle title="Experiment Results" note="Measured comparisons and planned work are shown separately. The current repository contains no released model metrics, so no performance value is inferred or fabricated." /><section className="section-card"><h2>Measured comparisons</h2>{measured.length ? <div className="matrix-wrap"><table className="matrix"><thead><tr><th>Model</th><th>Feature set</th><th>Evaluation</th><th>Recorded outcome</th></tr></thead><tbody>{measured.map((experiment) => <tr key={experiment.id}><td>{experiment.model}</td><td>{experiment.featureSet}</td><td>{experiment.evaluation}</td><td>{experiment.note}</td></tr>)}</tbody></table></div> : <div className="admin-empty">No measured model comparison is recorded in the current research corpus. When a reproducible run is committed, its manifest and metrics will appear here.</div>}</section><section className="section-card"><h2>Research queue</h2><div className="matrix-wrap"><table className="matrix"><thead><tr><th>Model</th><th>Feature set</th><th>Evaluation</th><th>State</th><th>Prerequisite</th></tr></thead><tbody>{queue.map((experiment) => <tr key={experiment.id}><td>{experiment.model}</td><td>{experiment.featureSet}</td><td>{experiment.evaluation}</td><td><span className="tag">{experiment.status}</span></td><td>{experiment.note}</td></tr>)}</tbody></table></div></section></>;
}

export default function WorkspacePage({ user }: { user: User }) {
  const router = useRouter(); const section = typeof router.query.section === "string" ? router.query.section : "literature-review";
  const document = trpc.research.document.useQuery({ slug: section }, { enabled: ["literature-review", "gap-analysis", "methodology"].includes(section) });
  const literature = trpc.research.literature.useQuery(undefined, { enabled: section === "literature-review" });
  let body;
  if (section === "literature-review") body = <><PanelTitle title="Literature Review" note="A filtered, sortable comparison of the most relevant ecosystem, package-detection, dependency, and workflow-security research." /><LiteratureMatrix studies={literature.data ?? []} /></>;
  else if (section === "benchmark-findings") body = <BenchmarkPanel />;
  else if (section === "incident-labels") body = <IncidentPanel />;
  else if (section === "experiment-results") body = <ExperimentPanel />;
  else body = document.data ? <><PanelTitle title={document.data.title} note={document.data.summary} /><MarkdownReader markdown={document.data.markdown} /></> : <Loading />;
  return <><Head><title>{section.replace(/-/g, " ")} · Supply Chain Research Hub</title></Head><WorkspaceLayout user={user}>{body}</WorkspaceLayout></>;
}

export async function getServerSideProps(context: GetServerSidePropsContext) { const user = await getAuthenticatedUser(context.req); if (!user) return { redirect: { destination: "/", permanent: false } }; return { props: { user: { name: user.name, role: user.role } } }; }
