import type { GetServerSidePropsContext } from "next";
import type { NextApiRequest } from "next";
import { buildClerkProps } from "@clerk/nextjs/server";
import Head from "next/head";
import { useRouter } from "next/router";
import { MarkdownReader } from "../../../components/MarkdownReader";
import { WorkspaceLayout } from "../../../components/WorkspaceLayout";
import { getClerkResearchUser } from "../../../server/clerkAuth";
import { trpc } from "../../../lib/trpc";

type User = { name: string; role: string };

export default function EvidencePage({ user }: { user: User }) {
  const router = useRouter();
  const file = typeof router.query.file === "string" ? router.query.file : "";
  const query = trpc.research.evidence.useQuery({ file }, { enabled: Boolean(file) });
  if (!query.data) return <><Head><title>Evidence · Supply Chain Research Hub</title></Head><WorkspaceLayout user={user}><div className="admin-empty">Loading protected evidence…</div></WorkspaceLayout></>;
  const heading = query.data.fileName.replace(/\.(md|json)$/, "").replace(/_/g, " ");
  return <><Head><title>{`${heading} · Evidence`}</title></Head><WorkspaceLayout user={user}><div className="page-title"><h1>Evidence file</h1><p>Protected repository source object. This viewer exposes retained research text without granting public access to the workspace.</p></div><div className="evidence-header"><code>{query.data.fileName}</code><span className="tag">{query.data.format}</span></div>{query.data.format === "markdown" ? <MarkdownReader markdown={query.data.content} /> : <pre className="evidence-json">{JSON.stringify(JSON.parse(query.data.content), null, 2)}</pre>}</WorkspaceLayout></>;
}

export async function getServerSideProps(context: GetServerSidePropsContext) { const user = await getClerkResearchUser(context.req as NextApiRequest); if (!user) return { redirect: { destination: "/", permanent: false } }; return { props: { ...buildClerkProps(context.req as NextApiRequest), user: { name: user.name, role: user.role } } }; }
