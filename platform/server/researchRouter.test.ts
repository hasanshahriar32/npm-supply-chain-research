import { beforeEach, describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  saveContentRecord: vi.fn(async (input: unknown) => [input]),
  saveBlogPost: vi.fn(async (input: unknown) => [input]),
}));
vi.mock("./platformDb", () => ({
  getResearchUser: vi.fn(async () => null),
  upsertResearchUser: vi.fn(async () => null),
  listResearchUsers: vi.fn(async () => []),
  listContentRecords: vi.fn(async () => []),
  listBlogPosts: vi.fn(async () => []),
  listManagedRecords: vi.fn(async () => ({ snapshots: [], incidents: [], experiments: [] })),
  saveContentRecord: mocks.saveContentRecord,
  saveBlogPost: mocks.saveBlogPost,
}));

import { appRouter } from "./researchRouter";

const baseContext = { req: { headers: {} }, res: {} } as any;
const researcher = { openId: "researcher", name: "Researcher", email: null, role: "researcher" as const };
const admin = { openId: "admin", name: "Administrator", email: null, role: "admin" as const };

describe("research platform tRPC procedures", () => {
  beforeEach(() => mocks.saveContentRecord.mockClear());

  it("keeps research data unavailable to an unauthenticated caller", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: null });
    await expect(caller.research.literature()).rejects.toMatchObject({ code: "UNAUTHORIZED" });
  });

  it("serves the repository literature matrix to an authenticated researcher", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: researcher });
    const literature = await caller.research.literature();
    expect(literature).toHaveLength(15);
    expect(literature[0]?.study_id).toBe("L01");
  });

  it("blocks researcher access to administrative procedures", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: researcher });
    await expect(caller.admin.overview()).rejects.toMatchObject({ code: "FORBIDDEN" });
  });

  it("permits an administrator to save managed content", async () => {
    const caller = appRouter.createCaller({ ...baseContext, user: admin });
    await caller.admin.saveContent({ slug: "methodology-note", title: "Methodology note", category: "methodology", sourceFile: "30_proposed_methodology.md", status: "published", summary: "A managed source note." });
    expect(mocks.saveContentRecord).toHaveBeenCalledWith(expect.objectContaining({ slug: "methodology-note", status: "published" }));
  });
});
