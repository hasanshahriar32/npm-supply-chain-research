import type { NextApiRequest, NextApiResponse } from "next";
import { initTRPC, TRPCError } from "@trpc/server";
import { getClerkResearchUser } from "./clerkAuth";

export async function createContext({ req, res }: { req: NextApiRequest; res: NextApiResponse }) {
  const user = await getClerkResearchUser(req);
  return { req, res, user };
}

const t = initTRPC.context<typeof createContext>().create();
export const router = t.router;
export const publicProcedure = t.procedure;
export const protectedProcedure = t.procedure.use(({ ctx, next }) => {
  if (!ctx.user) throw new TRPCError({ code: "UNAUTHORIZED", message: "Sign in to access the research workspace." });
  return next({ ctx: { ...ctx, user: ctx.user } });
});
export const adminProcedure = protectedProcedure.use(({ ctx, next }) => {
  if (ctx.user.role !== "admin") throw new TRPCError({ code: "FORBIDDEN", message: "Administrator access is required." });
  return next({ ctx });
});
