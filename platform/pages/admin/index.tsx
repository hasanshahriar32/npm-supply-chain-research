import { UserButton } from "@clerk/nextjs";
import { buildClerkProps } from "@clerk/nextjs/server";
import type { GetServerSidePropsContext, NextApiRequest } from "next";
import Head from "next/head";
import Link from "next/link";
import { useState } from "react";
import { trpc } from "../../lib/trpc";
import { getClerkResearchUser } from "../../server/clerkAuth";

type Tab = "overview" | "reviews" | "access" | "ingestion";
type UserRecord = { openId: string; name?: string | null; email?: string | null; role: string; lastSignedIn: string | Date };
type ContentRecord = { id: number; title: string; slug: string; category: string; status: string; summary?: string | null; updatedAt: string | Date };
type Snapshot = { id: number; snapshotDate: string | Date; packages: number; status: string; sourceRef?: string | null; isCurrent: boolean };
type Ingestion = { id: number; sourceRef: string; status: string; detail?: string | null; completedAt?: string | Date | null };

function ConsoleHeader({ user }: { user: { name: string; role: string } }) {
  return <header className="admin-console-header"><Link className="brand" href="/workspace/literature-review">Supply Chain<br />Research Hub</Link><div className="admin-console-status"><span className="eyebrow">Separate administrator console</span><Link href="/workspace/literature-review">Return to research</Link><UserButton /><span>{user.name}</span></div></header>;
}

export default function AdminConsole({ user }: { user: { name: string; role: string } }) {
  const [tab, setTab] = useState<Tab>("overview");
  const admin = trpc.admin.overview.useQuery();
  const utils = trpc.useUtils();
  const invalidate = () => utils.admin.overview.invalidate();
  const saveContent = trpc.admin.saveContent.useMutation({ onSuccess: invalidate });
  const reviewContent = trpc.admin.reviewContent.useMutation({ onSuccess: invalidate });
  const setUserRole = trpc.admin.setUserRole.useMutation({ onSuccess: invalidate });
  const reviewSnapshot = trpc.admin.reviewSnapshot.useMutation({ onSuccess: invalidate });
  const runIngestion = trpc.admin.runIngestion.useMutation({ onSuccess: invalidate });

  if (!admin.data) return <><ConsoleHeader user={user} /><main className="admin-console"><div className="admin-empty">Loading the administrative control surface…</div></main></>;
  const data = admin.data as { users: UserRecord[]; content: ContentRecord[]; snapshots: Snapshot[]; ingestion: Ingestion[]; databaseConnected: boolean };
  const pendingContent = data.content.filter((item) => item.status === "pending" || item.status === "approved");
  const pendingSnapshots = data.snapshots.filter((item) => item.status === "pending" || item.status === "approved");

  return <><Head><title>Administration · Supply Chain Research Hub</title></Head><ConsoleHeader user={user} /><main className="admin-console"><section className="admin-console-intro"><div><span className="eyebrow">Governance and operations</span><h1>Admin<br /><em>console.</em></h1></div><p>This independent surface governs access, staged research publication, and deterministic benchmark refreshes. Research readers remain inside the separate workspace.</p></section><nav className="admin-console-tabs">{(["overview", "reviews", "access", "ingestion"] as Tab[]).map((item) => <button className={tab === item ? "active" : ""} key={item} onClick={() => setTab(item)}>{item}</button>)}</nav>
    {tab === "overview" && <section className="admin-console-grid"><article><span className="eyebrow">Pending research</span><strong>{pendingContent.length}</strong><p>Content records awaiting a review or publication decision.</p></article><article><span className="eyebrow">Pending snapshots</span><strong>{pendingSnapshots.length}</strong><p>Data refreshes held until an administrator publishes them.</p></article><article><span className="eyebrow">Active researchers</span><strong>{data.users.length}</strong><p>Signed-in users recorded in the platform database.</p></article><article><span className="eyebrow">Database</span><strong>{data.databaseConnected ? "On" : "Off"}</strong><p>PostgreSQL connection state for governance records.</p></article></section>}
    {tab === "reviews" && <section className="admin-surface"><div className="admin-surface-heading"><div><span className="eyebrow">Approval queue</span><h2>Research content</h2></div><p>New records enter as pending. Approval does not publish automatically; publication is a separate deliberate action.</p></div><form className="console-form" onSubmit={(event) => { event.preventDefault(); const form = new FormData(event.currentTarget); saveContent.mutate({ title: String(form.get("title")), slug: String(form.get("slug")), category: String(form.get("category")), summary: String(form.get("summary")), status: "pending" }); event.currentTarget.reset(); }}><input name="title" placeholder="Research finding title" required /><input name="slug" placeholder="research-finding-slug" required /><input name="category" placeholder="Category" required /><textarea name="summary" placeholder="Concise evidence summary" required /><button type="submit">Submit for approval</button></form><div className="approval-list">{data.content.length ? data.content.map((item) => <article className="approval-row" key={item.id}><div><span className="tag">{item.status}</span><h3>{item.title}</h3><p>{item.summary || item.category}</p></div><div className="approval-actions"><button disabled={reviewContent.isPending} onClick={() => reviewContent.mutate({ id: item.id, status: "approved" })}>Approve</button><button disabled={reviewContent.isPending} onClick={() => reviewContent.mutate({ id: item.id, status: "published" })}>Publish</button><button className="danger" disabled={reviewContent.isPending} onClick={() => reviewContent.mutate({ id: item.id, status: "rejected" })}>Reject</button></div></article>) : <div className="admin-empty">No staged research records yet.</div>}</div></section>}
    {tab === "access" && <section className="admin-surface"><div className="admin-surface-heading"><div><span className="eyebrow">Clerk identity governance</span><h2>Researcher access</h2></div><p>Promoting a user updates their Clerk public metadata and the local governance record. Administrators can access this console; researchers cannot.</p></div><div className="matrix-wrap"><table className="matrix"><thead><tr><th>Name</th><th>Email</th><th>Current role</th><th>Change role</th><th>Last sign-in</th></tr></thead><tbody>{data.users.map((item) => <tr key={item.openId}><td>{item.name || "—"}</td><td>{item.email || "—"}</td><td><span className="tag">{item.role}</span></td><td><select className="select" value={item.role} onChange={(event) => setUserRole.mutate({ openId: item.openId, role: event.target.value as "admin" | "researcher" })} disabled={setUserRole.isPending}><option value="researcher">Researcher</option><option value="admin">Administrator</option></select></td><td>{new Date(item.lastSignedIn).toLocaleDateString()}</td></tr>)}</tbody></table></div></section>}
    {tab === "ingestion" && <section className="admin-surface"><div className="admin-surface-heading"><div><span className="eyebrow">Daily repository refresh</span><h2>Benchmark snapshots</h2></div><p>The automated job stages a new snapshot from the private repository metrics archive. It is never made current until you publish it below.</p></div><div className="ingestion-controls"><button className="run-ingestion" disabled={runIngestion.isPending} onClick={() => runIngestion.mutate()}>{runIngestion.isPending ? "Fetching source…" : "Run refresh now"}</button><span>Configured for daily Vercel cron execution at 03:00 UTC after deployment.</span></div><div className="approval-list">{data.snapshots.map((snapshot) => <article className="approval-row" key={snapshot.id}><div><span className="tag">{snapshot.isCurrent ? "current" : snapshot.status}</span><h3>{new Date(snapshot.snapshotDate).toLocaleString()}</h3><p>{snapshot.packages.toLocaleString()} package metrics · {snapshot.sourceRef ? `source ${snapshot.sourceRef.slice(0, 12)}` : "seeded repository snapshot"}</p></div><div className="approval-actions"><button disabled={reviewSnapshot.isPending} onClick={() => reviewSnapshot.mutate({ id: snapshot.id, status: "approved" })}>Approve</button><button disabled={reviewSnapshot.isPending} onClick={() => reviewSnapshot.mutate({ id: snapshot.id, status: "published" })}>Publish</button><button className="danger" disabled={reviewSnapshot.isPending} onClick={() => reviewSnapshot.mutate({ id: snapshot.id, status: "rejected" })}>Reject</button></div></article>)}</div><section className="run-log"><span className="eyebrow">Ingestion history</span>{data.ingestion.length ? data.ingestion.map((run) => <p key={run.id}><strong>{run.status}</strong> · {run.detail || run.sourceRef}</p>) : <p>No automated refresh has been recorded yet.</p>}</section></section>}
  </main></>;
}

export async function getServerSideProps(context: GetServerSidePropsContext) {
  const user = await getClerkResearchUser(context.req as NextApiRequest);
  if (!user) return { redirect: { destination: "/", permanent: false } };
  if (user.role !== "admin") return { redirect: { destination: "/workspace/literature-review", permanent: false } };
  return { props: { ...buildClerkProps(context.req as NextApiRequest), user: { name: user.name, role: user.role } } };
}
