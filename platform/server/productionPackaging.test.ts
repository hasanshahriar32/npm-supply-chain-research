import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

const packageJson = JSON.parse(readFileSync(new URL("../package.json", import.meta.url), "utf8")) as {
  scripts: Record<string, string>;
};
const productionServer = readFileSync(new URL("./_core/nextProductionServer.ts", import.meta.url), "utf8");

describe("managed production packaging", () => {
  it("builds a Node runtime bundle plus a nonempty static-upload marker", () => {
    expect(packageJson.scripts.build).toContain("--outfile=dist/index.js");
    expect(packageJson.scripts.build).toContain("dist/public/__next_runtime_marker__.txt");
    expect(packageJson.scripts.start).toBe("NODE_ENV=production node dist/index.js");
  });

  it("binds the Next request handler to the deployment-provided port", () => {
    expect(productionServer).toContain("process.env.PORT");
    expect(productionServer).toContain('next({ dev: false, hostname, port })');
    expect(productionServer).toContain("createServer");
    expect(productionServer).toContain('"/__next_runtime_marker__.txt"');
    expect(productionServer).toContain("runtimeMarkerPath");
  });
});
