import { boolean, integer, jsonb, pgTable, serial, text, timestamp, varchar } from "drizzle-orm/pg-core";

export const researchUsers = pgTable("research_users", {
  id: serial("id").primaryKey(),
  openId: varchar("open_id", { length: 128 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  role: varchar("role", { length: 32 }).notNull().default("researcher"),
  lastSignedIn: timestamp("last_signed_in", { withTimezone: true }).notNull().defaultNow(),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export const contentRecords = pgTable("content_records", {
  id: serial("id").primaryKey(),
  slug: varchar("slug", { length: 160 }).notNull().unique(),
  title: text("title").notNull(),
  category: varchar("category", { length: 64 }).notNull(),
  sourceFile: varchar("source_file", { length: 256 }),
  status: varchar("status", { length: 32 }).notNull().default("pending"),
  summary: text("summary"),
  metadata: jsonb("metadata"),
  reviewedByOpenId: varchar("reviewed_by_open_id", { length: 128 }),
  reviewedAt: timestamp("reviewed_at", { withTimezone: true }),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export const blogPosts = pgTable("blog_posts", {
  id: serial("id").primaryKey(),
  slug: varchar("slug", { length: 160 }).notNull().unique(),
  title: text("title").notNull(),
  excerpt: text("excerpt"),
  body: text("body"),
  status: varchar("status", { length: 32 }).notNull().default("draft"),
  authorOpenId: varchar("author_open_id", { length: 128 }),
  publishedAt: timestamp("published_at", { withTimezone: true }),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});

export const benchmarkSnapshots = pgTable("benchmark_snapshots", {
  id: serial("id").primaryKey(),
  snapshotDate: timestamp("snapshot_date", { withTimezone: true }).notNull(),
  packages: integer("packages").notNull(),
  versions: integer("versions").notNull(),
  maintainers: integer("maintainers").notNull(),
  dependencyEdges: integer("dependency_edges").notNull(),
  repositoryMappings: integer("repository_mappings").notNull(),
  workflowChecks: integer("workflow_checks").notNull(),
  workflowDetections: integer("workflow_detections").notNull(),
  advisoryRecords: integer("advisory_records").notNull(),
  metricsRecords: integer("metrics_records").notNull(),
  isCurrent: boolean("is_current").notNull().default(true),
  status: varchar("status", { length: 32 }).notNull().default("published"),
  sourceRef: varchar("source_ref", { length: 255 }),
  chartData: jsonb("chart_data"),
  reviewedByOpenId: varchar("reviewed_by_open_id", { length: 128 }),
  reviewedAt: timestamp("reviewed_at", { withTimezone: true }),
});

export const ingestionRuns = pgTable("ingestion_runs", {
  id: serial("id").primaryKey(),
  sourceRef: varchar("source_ref", { length: 255 }).notNull().unique(),
  status: varchar("status", { length: 32 }).notNull(),
  detail: text("detail"),
  snapshotId: integer("snapshot_id"),
  startedAt: timestamp("started_at", { withTimezone: true }).notNull().defaultNow(),
  completedAt: timestamp("completed_at", { withTimezone: true }),
});

export const incidentLabels = pgTable("incident_labels", {
  id: serial("id").primaryKey(),
  name: text("name").notNull(),
  incidentType: varchar("incident_type", { length: 64 }).notNull(),
  eventDate: timestamp("event_date", { withTimezone: true }),
  scope: text("scope"),
  assessment: text("assessment"),
  evidenceSource: text("evidence_source"),
  status: varchar("status", { length: 32 }).notNull().default("review"),
  createdAt: timestamp("created_at", { withTimezone: true }).notNull().defaultNow(),
});

export const experimentResults = pgTable("experiment_results", {
  id: serial("id").primaryKey(),
  model: text("model").notNull(),
  featureSet: text("feature_set").notNull(),
  evaluation: text("evaluation").notNull(),
  status: varchar("status", { length: 32 }).notNull().default("planned"),
  note: text("note"),
  updatedAt: timestamp("updated_at", { withTimezone: true }).notNull().defaultNow(),
});
