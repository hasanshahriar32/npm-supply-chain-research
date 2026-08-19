import { describe, expect, it } from "vitest";
import { Pool } from "pg";

describe("PostgreSQL configuration", () => {
  it("provides a parseable PostgreSQL connection URL to the server", () => {
    const connectionString = process.env.POSTGRES_DATABASE_URL;

    expect(connectionString).toBeTruthy();
    const parsed = new URL(connectionString ?? "");
    expect(["postgres:", "postgresql:"]).toContain(parsed.protocol);
    expect(parsed.hostname).toBeTruthy();
  });

  it("accepts a lightweight server-side connectivity query", async () => {
    const pool = new Pool({ connectionString: process.env.POSTGRES_DATABASE_URL, max: 1, ssl: { rejectUnauthorized: false } });
    try {
      const result = await pool.query("SELECT 1 AS connected");
      expect(result.rows[0]?.connected).toBe(1);
    } finally {
      await pool.end();
    }
  });
});
