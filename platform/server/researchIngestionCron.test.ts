import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({ ingest: vi.fn() }));
vi.mock("./researchIngestion", () => ({ ingestMetricsArchive: mocks.ingest }));
import handler from "../pages/api/cron/research-ingestion";

function response() {
  const state: { status?: number; body?: unknown } = {};
  const res = { status: (code: number) => { state.status = code; return { json: (body: unknown) => { state.body = body; return undefined; } }; } };
  return { res, state };
}

describe("daily research-ingestion endpoint", () => {
  it("accepts the configured server-only cron secret", async () => {
    const { res, state } = response();
    mocks.ingest.mockResolvedValue({ status: "skipped" });
    await handler({ method: "GET", headers: { authorization: `Bearer ${process.env.CRON_SECRET}` } } as any, res as any);
    expect(state.status).toBe(200);
    expect(mocks.ingest).toHaveBeenCalledOnce();
  });

  it("rejects a request with an invalid cron secret", async () => {
    const { res, state } = response();
    await handler({ method: "GET", headers: { authorization: "Bearer invalid" } } as any, res as any);
    expect(state.status).toBe(401);
  });
});
