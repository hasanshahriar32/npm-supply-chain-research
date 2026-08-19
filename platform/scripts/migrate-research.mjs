import pg from "pg";

const { Pool } = pg;
const connectionString = process.env.POSTGRES_DATABASE_URL;

if (!connectionString) {
  throw new Error("POSTGRES_DATABASE_URL is required");
}

const pool = new Pool({ connectionString, max: 1, ssl: { rejectUnauthorized: false } });

const statements = [
  `CREATE TABLE IF NOT EXISTS research_users (
    id SERIAL PRIMARY KEY,
    open_id VARCHAR(128) NOT NULL UNIQUE,
    name TEXT,
    email VARCHAR(320),
    role VARCHAR(32) NOT NULL DEFAULT 'researcher',
    last_signed_in TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  )`,
  `CREATE TABLE IF NOT EXISTS content_records (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(160) NOT NULL UNIQUE,
    title TEXT NOT NULL,
    category VARCHAR(64) NOT NULL,
    source_file VARCHAR(256),
    status VARCHAR(32) NOT NULL DEFAULT 'published',
    summary TEXT,
    metadata JSONB,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  )`,
  `CREATE TABLE IF NOT EXISTS blog_posts (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(160) NOT NULL UNIQUE,
    title TEXT NOT NULL,
    excerpt TEXT,
    body TEXT,
    status VARCHAR(32) NOT NULL DEFAULT 'draft',
    author_open_id VARCHAR(128),
    published_at TIMESTAMPTZ,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  )`,
  `CREATE TABLE IF NOT EXISTS benchmark_snapshots (
    id SERIAL PRIMARY KEY,
    snapshot_date TIMESTAMPTZ NOT NULL,
    packages INTEGER NOT NULL,
    versions INTEGER NOT NULL,
    maintainers INTEGER NOT NULL,
    dependency_edges INTEGER NOT NULL,
    repository_mappings INTEGER NOT NULL,
    workflow_checks INTEGER NOT NULL,
    workflow_detections INTEGER NOT NULL,
    advisory_records INTEGER NOT NULL,
    metrics_records INTEGER NOT NULL,
    is_current BOOLEAN NOT NULL DEFAULT TRUE
  )`,
  `CREATE TABLE IF NOT EXISTS incident_labels (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    incident_type VARCHAR(64) NOT NULL,
    event_date TIMESTAMPTZ,
    scope TEXT,
    assessment TEXT,
    evidence_source TEXT,
    status VARCHAR(32) NOT NULL DEFAULT 'review',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  )`,
  `CREATE TABLE IF NOT EXISTS experiment_results (
    id SERIAL PRIMARY KEY,
    model TEXT NOT NULL,
    feature_set TEXT NOT NULL,
    evaluation TEXT NOT NULL,
    status VARCHAR(32) NOT NULL DEFAULT 'planned',
    note TEXT,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
  )`,
];

try {
  for (const statement of statements) await pool.query(statement);
  console.log(`Applied ${statements.length} research-platform schema statements.`);
} finally {
  await pool.end();
}
