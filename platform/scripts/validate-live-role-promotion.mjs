import { listResearchUsers, upsertResearchUser } from "../server/platformDb.ts";
import { randomBytes } from "node:crypto";

const validationExternalId = `supply-chain-role-validation-${new Date().toISOString().replace(/[^0-9]/g, "")}`;
const validationEmail = `${validationExternalId}@example.com`;
const validationPassword = `${randomBytes(24).toString("base64url")}Aa1!`;
const clerkSecretKey = process.env.CLERK_SECRET_KEY;
if (!clerkSecretKey) throw new Error("CLERK_SECRET_KEY is required to create the isolated validation identity.");

async function clerkRequest(path, init) {
  const response = await fetch(`https://api.clerk.com/v1${path}`, {
    ...init,
    headers: {
      Authorization: `Bearer ${clerkSecretKey}`,
      "Content-Type": "application/json",
      ...init.headers,
    },
  });
  const body = await response.json();
  if (!response.ok) throw new Error(`Clerk request failed (${response.status}): ${JSON.stringify(body)}`);
  return body;
}

const administrators = (await listResearchUsers()).filter((user) => user.role === "admin");
const administrator = administrators[0];

if (!administrator) {
  throw new Error("A synchronized administrator is required before validating the role-management mutation.");
}

const validationIdentity = await clerkRequest("/users", {
  method: "POST",
  body: JSON.stringify({
    external_id: validationExternalId,
    first_name: "Governance",
    last_name: "Validation",
    email_address: [validationEmail],
    password: validationPassword,
    public_metadata: { role: "researcher", purpose: "isolated-role-promotion-verification" },
  }),
});

const validationName = [validationIdentity.firstName, validationIdentity.lastName].filter(Boolean).join(" ") || "Governance Validation";
await upsertResearchUser({
  openId: validationIdentity.id,
  name: validationName,
  email: validationEmail,
  role: "researcher",
});

console.log(JSON.stringify({
  verificationAccountId: validationIdentity.id,
  verificationExternalId: validationExternalId,
  initialRole: validationIdentity.publicMetadata?.role,
  administratorOpenId: administrator.openId,
  preserved: true,
}, null, 2));
