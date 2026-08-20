import { clerkClient, getAuth } from "@clerk/nextjs/server";
import type { NextApiRequest } from "next";
import { getResearchUser, upsertResearchUser } from "./platformDb";

export type ClerkResearchUser = {
  openId: string;
  name: string;
  email: string | null;
  role: "admin" | "researcher";
};

export async function getClerkResearchUser(req: NextApiRequest): Promise<ClerkResearchUser | null> {
  const { isAuthenticated, userId } = getAuth(req);
  if (!isAuthenticated || !userId) return null;

  const client = await clerkClient();
  const clerkUser = await client.users.getUser(userId);
  const name = [clerkUser.firstName, clerkUser.lastName].filter(Boolean).join(" ") || clerkUser.username || "Researcher";
  const email = clerkUser.primaryEmailAddress?.emailAddress ?? null;
  const existingUser = await getResearchUser(userId).catch(() => null);
  const metadataRole = typeof clerkUser.publicMetadata?.role === "string" ? clerkUser.publicMetadata.role : "researcher";
  const role = metadataRole === "admin" || existingUser?.role === "admin" ? "admin" : "researcher";
  await upsertResearchUser({ openId: userId, name, email, role }).catch(() => null);

  return {
    openId: userId,
    name,
    email,
    role,
  };
}

export async function setClerkResearchUserRole(openId: string, role: "admin" | "researcher") {
  const client = await clerkClient();
  const user = await client.users.getUser(openId);
  await client.users.updateUserMetadata(openId, { publicMetadata: { ...user.publicMetadata, role } });
  return role;
}
