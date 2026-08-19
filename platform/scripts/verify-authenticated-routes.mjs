import { SignJWT } from "jose";

const secret = new TextEncoder().encode(process.env.JWT_SECRET ?? "development-secret-change-me");
const openId = process.env.OWNER_OPEN_ID;
if (!openId) throw new Error("OWNER_OPEN_ID is required for admin-route verification");

const token = await new SignJWT({ openId, appId: process.env.VITE_APP_ID ?? "", name: "Verification Administrator", role: "admin" })
  .setProtectedHeader({ alg: "HS256" })
  .setIssuedAt()
  .setExpirationTime("10m")
  .sign(secret);

const headers = { cookie: `research_platform_session=${encodeURIComponent(token)}` };
const routes = [["/workspace/literature-review", "Literature Review"], ["/workspace/admin", "Administration"]];

for (const [route, marker] of routes) {
  const response = await fetch(`http://localhost:3000${route}`, { headers, redirect: "manual" });
  if (response.status !== 200) throw new Error(`${route} returned ${response.status}`);
  const body = await response.text();
  if (!body.includes(marker)) throw new Error(`${route} did not render the expected protected page`);
  console.log(`${route}: ${response.status}`);
}

const trpcInput = encodeURIComponent(JSON.stringify({ "0": { json: null } }));
const apiChecks = [
  ["/api/trpc/research.literature", "L01"],
  ["/api/trpc/admin.overview", "databaseConnected"],
];

for (const [route, marker] of apiChecks) {
  const response = await fetch(`http://localhost:3000${route}?batch=1&input=${trpcInput}`, { headers });
  if (response.status !== 200) throw new Error(`${route} returned ${response.status}`);
  const body = await response.text();
  if (!body.includes(marker)) throw new Error(`${route} did not return the expected protected data`);
  console.log(`${route}: ${response.status}`);
}
