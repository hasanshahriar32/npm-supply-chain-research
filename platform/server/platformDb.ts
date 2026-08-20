import { and, desc, eq } from "drizzle-orm";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import {
  benchmarkSnapshots,
  blogPosts,
  contentRecords,
  experimentResults,
  incidentLabels,
  ingestionRuns,
  researchUsers,
} from "../drizzle/researchSchema";

let pool: Pool | null = null;
let db: ReturnType<typeof drizzle> | null = null;

export function getResearchDb() {
  const connectionString = process.env.POSTGRES_DATABASE_URL;
  if (!connectionString) return null;
  if (!pool) pool = new Pool({ connectionString, max: 4, ssl: { rejectUnauthorized: false } });
  if (!db) db = drizzle(pool);
  return db;
}

export async function upsertResearchUser(input: { openId: string; name?: string | null; email?: string | null; role?: "admin" | "researcher" }) {
  const connection = getResearchDb();
  if (!connection) return null;
  const rows = await connection.insert(researchUsers).values({ ...input, role: input.role ?? "researcher", lastSignedIn: new Date() }).onConflictDoUpdate({
    target: researchUsers.openId,
    set: { name: input.name ?? null, email: input.email ?? null, role: input.role ?? "researcher", lastSignedIn: new Date(), updatedAt: new Date() },
  }).returning();
  return rows[0] ?? null;
}

export async function getResearchUser(openId: string) {
  const connection = getResearchDb();
  if (!connection) return null;
  const rows = await connection.select().from(researchUsers).where(eq(researchUsers.openId, openId)).limit(1);
  return rows[0] ?? null;
}

export async function listResearchUsers() {
  const connection = getResearchDb();
  if (!connection) return [];
  return connection.select().from(researchUsers).orderBy(desc(researchUsers.lastSignedIn));
}

export async function updateResearchUserRole(openId: string, role: "admin" | "researcher") {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  const rows = await connection.update(researchUsers).set({ role, updatedAt: new Date() }).where(eq(researchUsers.openId, openId)).returning();
  return rows[0] ?? null;
}

export async function listContentRecords() {
  const connection = getResearchDb();
  if (!connection) return [];
  return connection.select().from(contentRecords).orderBy(desc(contentRecords.updatedAt));
}

export async function saveContentRecord(input: { slug: string; title: string; category: string; sourceFile?: string | null; status: string; summary?: string | null }) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  return connection.insert(contentRecords).values(input).onConflictDoUpdate({ target: contentRecords.slug, set: { ...input, updatedAt: new Date() } }).returning();
}

export async function reviewContentRecord(id: number, status: "approved" | "published" | "rejected", reviewerOpenId: string) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  const rows = await connection.update(contentRecords).set({ status, reviewedByOpenId: reviewerOpenId, reviewedAt: new Date(), updatedAt: new Date() }).where(eq(contentRecords.id, id)).returning();
  return rows[0] ?? null;
}

export async function listBlogPosts() {
  const connection = getResearchDb();
  if (!connection) return [];
  return connection.select().from(blogPosts).orderBy(desc(blogPosts.updatedAt));
}

export async function saveBlogPost(input: { slug: string; title: string; excerpt?: string | null; body?: string | null; status: string; authorOpenId?: string | null }) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  return connection.insert(blogPosts).values(input).onConflictDoUpdate({ target: blogPosts.slug, set: { ...input, updatedAt: new Date() } }).returning();
}

export async function listManagedRecords() {
  const connection = getResearchDb();
  if (!connection) return { snapshots: [], incidents: [], experiments: [], ingestion: [] };
  const [snapshots, incidents, experiments, ingestion] = await Promise.all([
    connection.select().from(benchmarkSnapshots).orderBy(desc(benchmarkSnapshots.snapshotDate)),
    connection.select().from(incidentLabels).orderBy(desc(incidentLabels.createdAt)),
    connection.select().from(experimentResults).orderBy(desc(experimentResults.updatedAt)),
    connection.select().from(ingestionRuns).orderBy(desc(ingestionRuns.startedAt)),
  ]);
  return { snapshots, incidents, experiments, ingestion };
}

export async function listSnapshotHistory() {
  const connection = getResearchDb();
  if (!connection) return [];
  return connection.select().from(benchmarkSnapshots).orderBy(desc(benchmarkSnapshots.snapshotDate));
}

export async function getCurrentSnapshot() {
  const connection = getResearchDb();
  if (!connection) return null;
  const rows = await connection.select().from(benchmarkSnapshots).where(and(eq(benchmarkSnapshots.isCurrent, true))).limit(1);
  return rows[0] ?? null;
}

export async function createPendingSnapshot(input: Omit<typeof benchmarkSnapshots.$inferInsert, "id" | "isCurrent" | "status">) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  const rows = await connection.insert(benchmarkSnapshots).values({ ...input, isCurrent: false, status: "pending" }).returning();
  return rows[0] ?? null;
}

export async function reviewSnapshot(id: number, status: "approved" | "published" | "rejected", reviewerOpenId: string) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  if (status === "published") await connection.update(benchmarkSnapshots).set({ isCurrent: false }).where(eq(benchmarkSnapshots.isCurrent, true));
  const rows = await connection.update(benchmarkSnapshots).set({ status, isCurrent: status === "published", reviewedByOpenId: reviewerOpenId, reviewedAt: new Date() }).where(eq(benchmarkSnapshots.id, id)).returning();
  return rows[0] ?? null;
}

export async function getIngestionRun(sourceRef: string) {
  const connection = getResearchDb();
  if (!connection) return null;
  const rows = await connection.select().from(ingestionRuns).where(eq(ingestionRuns.sourceRef, sourceRef)).limit(1);
  return rows[0] ?? null;
}

export async function claimIngestionRun(sourceRef: string) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  const rows = await connection.insert(ingestionRuns).values({ sourceRef, status: "running", detail: "Ingestion claim created" }).onConflictDoNothing().returning();
  return rows[0] ?? null;
}

export async function recordIngestionRun(input: { sourceRef: string; status: string; detail?: string; snapshotId?: number | null }) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  const rows = await connection.insert(ingestionRuns).values({ ...input, completedAt: new Date() }).onConflictDoUpdate({ target: ingestionRuns.sourceRef, set: { status: input.status, detail: input.detail ?? null, snapshotId: input.snapshotId ?? null, completedAt: new Date() } }).returning();
  return rows[0] ?? null;
}
