import { and, desc, eq } from "drizzle-orm";
import { drizzle } from "drizzle-orm/node-postgres";
import { Pool } from "pg";
import {
  benchmarkSnapshots,
  blogPosts,
  contentRecords,
  experimentResults,
  incidentLabels,
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

export async function upsertResearchUser(input: {
  openId: string;
  name?: string | null;
  email?: string | null;
  role?: "admin" | "researcher";
}) {
  const connection = getResearchDb();
  if (!connection) return null;
  const rows = await connection
    .insert(researchUsers)
    .values({ ...input, role: input.role ?? "researcher", lastSignedIn: new Date() })
    .onConflictDoUpdate({
      target: researchUsers.openId,
      set: { name: input.name ?? null, email: input.email ?? null, role: input.role ?? "researcher", lastSignedIn: new Date(), updatedAt: new Date() },
    })
    .returning();
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

export async function listContentRecords() {
  const connection = getResearchDb();
  if (!connection) return [];
  return connection.select().from(contentRecords).orderBy(desc(contentRecords.updatedAt));
}

export async function saveContentRecord(input: {
  slug: string;
  title: string;
  category: string;
  sourceFile?: string | null;
  status: string;
  summary?: string | null;
}) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  return connection.insert(contentRecords).values(input).onConflictDoUpdate({
    target: contentRecords.slug,
    set: { ...input, updatedAt: new Date() },
  }).returning();
}

export async function listBlogPosts() {
  const connection = getResearchDb();
  if (!connection) return [];
  return connection.select().from(blogPosts).orderBy(desc(blogPosts.updatedAt));
}

export async function saveBlogPost(input: {
  slug: string;
  title: string;
  excerpt?: string | null;
  body?: string | null;
  status: string;
  authorOpenId?: string | null;
}) {
  const connection = getResearchDb();
  if (!connection) throw new Error("PostgreSQL is not configured");
  return connection.insert(blogPosts).values(input).onConflictDoUpdate({
    target: blogPosts.slug,
    set: { ...input, updatedAt: new Date() },
  }).returning();
}

export async function listManagedRecords() {
  const connection = getResearchDb();
  if (!connection) return { snapshots: [], incidents: [], experiments: [] };
  const [snapshots, incidents, experiments] = await Promise.all([
    connection.select().from(benchmarkSnapshots).orderBy(desc(benchmarkSnapshots.snapshotDate)),
    connection.select().from(incidentLabels).orderBy(desc(incidentLabels.createdAt)),
    connection.select().from(experimentResults).orderBy(desc(experimentResults.updatedAt)),
  ]);
  return { snapshots, incidents, experiments };
}

export async function getCurrentSnapshot() {
  const connection = getResearchDb();
  if (!connection) return null;
  const rows = await connection.select().from(benchmarkSnapshots).where(and(eq(benchmarkSnapshots.isCurrent, true))).limit(1);
  return rows[0] ?? null;
}
