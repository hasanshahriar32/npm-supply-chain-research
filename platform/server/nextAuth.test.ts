import { describe, expect, it } from "vitest";
import { createSession, getSession } from "./nextAuth";

describe("research-platform session guard", () => {
  it("reads a valid session from the protected platform cookie", async () => {
    const token = await createSession({ openId: "researcher-1", name: "Researcher", email: "researcher@example.test", role: "researcher" });
    const session = await getSession({ headers: { cookie: `research_platform_session=${encodeURIComponent(token)}` } });
    expect(session).toMatchObject({ openId: "researcher-1", name: "Researcher", role: "researcher" });
  });

  it("does not authenticate a request without the platform cookie", async () => {
    await expect(getSession({ headers: {} })).resolves.toBeNull();
  });
});
