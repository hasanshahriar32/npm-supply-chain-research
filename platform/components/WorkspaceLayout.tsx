import Link from "next/link";
import { useRouter } from "next/router";
import { UserButton } from "@clerk/nextjs";
import type { ReactNode } from "react";

const sections = [
  ["Literature Review", "/workspace/literature-review"],
  ["Gap Analysis", "/workspace/gap-analysis"],
  ["Benchmark Findings", "/workspace/benchmark-findings"],
  ["Methodology", "/workspace/methodology"],
  ["Incident Labels", "/workspace/incident-labels"],
  ["Experiment Results", "/workspace/experiment-results"],
] as const;

export function WorkspaceLayout({ children, user }: { children: ReactNode; user: { name: string; role: string } }) {
  const router = useRouter();
  return <div className="workspace"><aside className="workspace-aside"><Link className="brand" href="/workspace/literature-review">Supply Chain<br />Research Hub</Link><p className="workspace-subtitle">Private research workspace</p><nav className="workspace-nav">{sections.map(([label, href]) => <Link className={router.asPath === href ? "active" : ""} href={href} key={href}>{label}</Link>)}{user.role === "admin" && <Link className={router.asPath === "/workspace/admin" ? "active" : ""} href="/workspace/admin">Administration</Link>}</nav><div className="workspace-meta"><UserButton /><p>{user.name}</p><p>{user.role}</p></div></aside><main className="workspace-main"><header className="workspace-top"><span className="eyebrow">Research platform / v0.1</span><span className="status-dot">Repository sources live</span></header><nav className="mobile-nav">{sections.map(([label, href]) => <Link className={router.asPath === href ? "active" : ""} href={href} key={href}>{label}</Link>)}</nav><div className="workspace-content">{children}</div></main></div>;
}
