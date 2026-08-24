import { getResearchUser } from "../server/platformDb.ts";

const validationAccountId = process.argv[2];
const clerkSecretKey = process.env.CLERK_SECRET_KEY;

if (!validationAccountId) throw new Error("Pass the isolated validation Clerk user ID as the first argument.");
if (!clerkSecretKey) throw new Error("CLERK_SECRET_KEY is required to verify Clerk public metadata.");

const response = await fetch(`https://api.clerk.com/v1/users/${validationAccountId}`, {
  headers: { Authorization: `Bearer ${clerkSecretKey}` },
});
const clerkUser = await response.json();
if (!response.ok) throw new Error(`Clerk verification failed (${response.status}): ${JSON.stringify(clerkUser)}`);

const localUser = await getResearchUser(validationAccountId);
const clerkRole = clerkUser.public_metadata?.role;
if (clerkRole !== "admin" || localUser?.role !== "admin") {
  throw new Error("The promotion is not synchronized to both Clerk public metadata and PostgreSQL.");
}

console.log(JSON.stringify({
  verificationAccountId: validationAccountId,
  clerkRole,
  databaseRole: localUser.role,
  preserved: true,
}, null, 2));
