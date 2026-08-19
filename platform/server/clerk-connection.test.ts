import { describe, expect, it } from "vitest";

describe("Clerk configuration", () => {
  it("has a configured publishable key", () => {
    expect(process.env.NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY).toMatch(/^pk_/);
  });

  it("validates the configured secret against Clerk's instance endpoint", async () => {
    const secret = process.env.CLERK_SECRET_KEY;
    expect(secret).toMatch(/^sk_/);
    const response = await fetch("https://api.clerk.com/v1/instance", {
      headers: { Authorization: `Bearer ${secret}` },
    });
    expect(response.ok).toBe(true);
  }, 30_000);
});
