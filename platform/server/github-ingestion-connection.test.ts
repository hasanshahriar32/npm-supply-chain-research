import { describe, expect, it } from "vitest";

describe("GitHub ingestion credential", () => {
  it("can access the configured GitHub account with the server-side token", async () => {
    const token = process.env.GITHUB_TOKEN;
    expect(token).toBeTruthy();
    const response = await fetch("https://api.github.com/user", {
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${token}`,
        "X-GitHub-Api-Version": "2022-11-28",
      },
    });
    expect(response.status).toBe(200);
    const account = await response.json() as { login?: string };
    expect(account.login).toBe("ashik-hstu");
  }, 30_000);
});
