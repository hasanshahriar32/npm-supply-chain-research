import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import path from "node:path";
import next from "next";

const port = Number.parseInt(process.env.PORT ?? "3000", 10);
const hostname = "0.0.0.0";
const runtimeMarkerPath = path.join(process.cwd(), "dist", "public", "__next_runtime_marker__.txt");
const app = next({ dev: false, hostname, port });
const handle = app.getRequestHandler();

await app.prepare();

createServer(async (request, response) => {
  if (request.url?.split("?")[0] === "/__next_runtime_marker__.txt") {
    try {
      const marker = await readFile(runtimeMarkerPath, "utf8");
      response.writeHead(200, { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" });
      response.end(marker);
    } catch {
      response.writeHead(404, { "Content-Type": "text/plain; charset=utf-8" });
      response.end("Managed runtime marker is unavailable.\n");
    }
    return;
  }
  return handle(request, response);
}).listen(port, hostname, () => {
  console.info(`[Next production server] Listening on http://${hostname}:${port}`);
});
