import { describe, expect, it, vi } from "vitest";

const mocks = vi.hoisted(() => ({
  getAuth: vi.fn(),
  getUser: vi.fn(),
  upsertResearchUser: vi.fn(),
}));

vi.mock("@clerk/nextjs/server", () => ({
  getAuth: mocks.getAuth,
  clerkClient: async () => ({ users: { getUser: mocks.getUser } }),
}));

vi.mock("./platformDb", () => ({
  getResearchUser: vi.fn(async () => null),
  upsertResearchUser: mocks.upsertResearchUser,
}));

import { getClerkResearchUser } from "./clerkAuth";

describe("Clerk research identity", () => {
  it("returns null when the request has no Clerk session", async () => {
    mocks.getAuth.mockReturnValue({ isAuthenticated: false, userId: null });
    await expect(getClerkResearchUser({} as any)).resolves.toBeNull();
  });

  it("maps a Clerk administrator to the research user contract", async () => {
    mocks.getAuth.mockReturnValue({ isAuthenticated: true, userId: "user_clerk_admin" });
    mocks.getUser.mockResolvedValue({
      firstName: "Ada",
      lastName: "Researcher",
      username: "ada",
      primaryEmailAddress: { emailAddress: "ada@example.test" },
      publicMetadata: { role: "admin" },
    });
    mocks.upsertResearchUser.mockResolvedValue({ role: "admin" });

    await expect(getClerkResearchUser({} as any)).resolves.toEqual({
      openId: "user_clerk_admin",
      name: "Ada Researcher",
      email: "ada@example.test",
      role: "admin",
    });
    expect(mocks.upsertResearchUser).toHaveBeenCalledWith({ openId: "user_clerk_admin", name: "Ada Researcher", email: "ada@example.test", role: "admin" });
  });
});
