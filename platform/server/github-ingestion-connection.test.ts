import { describe, expect, it } from "vitest";

describe("GitHub ingestion repository access", () => {
  it.skipIf(!process.env.GITHUB_TOKEN)("can read the configured repository with the server-side token", async () => {
    const token = process.env.GITHUB_TOKEN;
    expect(token).toBeTruthy();
    const response = await fetch("https://api.github.com/repos/hasanshahriar32/npm-supply-chain-research", {
      headers: {
        Accept: "application/vnd.github+json",
        Authorization: `Bearer ${token}`,
        "X-GitHub-Api-Version": "2022-11-28",
      },
    });
    expect(response.status).toBe(200);
    const repository = await response.json() as { full_name?: string };
    expect(repository.full_name).toBe("hasanshahriar32/npm-supply-chain-research");
  }, 30_000);
});
