import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  saveContentRecord: vi.fn(async (input: unknown) => [input]),
  saveBlogPost: vi.fn(async (input: unknown) => [input]),
  reviewContentRecord: vi.fn(async () => ({ id: 1, status: "approved" })),
  reviewSnapshot: vi.fn(async () => ({ id: 2, status: "published" })),
  updateResearchUserRole: vi.fn(async () => ({ openId: "new-admin", role: "admin" })),
  setClerkRole: vi.fn(async () => "admin"),
  ingest: vi.fn(async () => ({ status: "staged", snapshotId: 2 })),
}));
vi.mock("./platformDb", () => ({
  getResearchUser: vi.fn(async () => null), getCurrentSnapshot: vi.fn(async () => null), upsertResearchUser: vi.fn(async () => null), listResearchUsers: vi.fn(async () => []), listContentRecords: vi.fn(async () => []), listBlogPosts: vi.fn(async () => []), listManagedRecords: vi.fn(async () => ({ snapshots: [], incidents: [], experiments: [], ingestion: [] })), listSnapshotHistory: vi.fn(async () => []),
  saveContentRecord: mocks.saveContentRecord, saveBlogPost: mocks.saveBlogPost, reviewContentRecord: mocks.reviewContentRecord, reviewSnapshot: mocks.reviewSnapshot, updateResearchUserRole: mocks.updateResearchUserRole,
}));
vi.mock("./clerkAuth", () => ({ setClerkResearchUserRole: mocks.setClerkRole }));
vi.mock("./researchIngestion", () => ({ ingestMetricsArchive: mocks.ingest }));

import { appRouter } from "./researchRouter";

const baseContext = { req: { headers: {} }, res: {} } as any;
const researcher = { openId: "researcher", name: "Researcher", email: null, role: "researcher" as const };
const admin = { openId: "admin", name: "Administrator", email: null, role: "admin" as const };

describe("research platform tRPC procedures", () => {
  beforeEach(() => Object.values(mocks).forEach((mock) => mock.mockClear()));

  it("keeps research data unavailable to an unauthenticated caller", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: null });
    await expect(caller.research.literature()).rejects.toMatchObject({ code: "UNAUTHORIZED" });
  });

  it("serves the repository literature matrix and chart summary to an authenticated researcher", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: researcher });
    const [literature, analytics] = await Promise.all([caller.research.literature(), caller.research.analytics()]);
    expect(literature).toHaveLength(15);
    expect(literature[0]?.study_id).toBe("L01");
    expect(analytics.recordCount).toBe(25228);
  });

  it("blocks researcher access to administrative procedures", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: researcher });
    await expect(caller.admin.overview()).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("permits content review and staged ingestion only to an administrator", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: admin });
    await caller.admin.saveContent({ slug: "methodology-note", title: "Methodology note", category: "methodology", sourceFile: "30_proposed_methodology.md", status: "pending", summary: "A managed source note." });
    await caller.admin.reviewContent({ id: 1, status: "approved" });
    await caller.admin.runIngestion();
    expect(mocks.saveContentRecord).toHaveBeenCalledWith(expect.objectContaining({ status: "pending" }));
    expect(mocks.reviewContentRecord).toHaveBeenCalledWith(1, "approved", "admin");
    expect(mocks.ingest).toHaveBeenCalledOnce();
  });

  it("synchronizes a promoted researcher role with Clerk and PostgreSQL", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: admin });
    await caller.admin.setUserRole({ openId: "new-admin", role: "admin" });
    expect(mocks.setClerkRole).toHaveBeenCalledWith("new-admin", "admin");
    expect(mocks.updateResearchUserRole).toHaveBeenCalledWith("new-admin", "admin");
  });

  it("prevents an administrator from removing their own access", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: admin });
    await expect(caller.admin.setUserRole({ openId: "admin", role: "researcher" })).rejects.toThrow("cannot remove your own administrator access");
  });
});
