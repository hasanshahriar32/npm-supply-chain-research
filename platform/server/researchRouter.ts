import { z } from "zod";
import { listBlogPosts, listContentRecords, listManagedRecords, listResearchUsers, saveBlogPost, saveContentRecord } from "./platformDb";
import { getDocument, getDocuments, getExperiments, getIncidents, getLiterature, getSnapshot } from "./researchSources";
import { adminProcedure, protectedProcedure, publicProcedure, router } from "./trpc";

export const appRouter = router({
  auth: router({
    me: publicProcedure.query(({ ctx }) => ctx.user),
  }),
  research: router({
    overview: protectedProcedure.query(async () => ({ snapshot: getSnapshot(), documents: await getDocuments(), incidents: getIncidents(), experiments: getExperiments() })),
    literature: protectedProcedure.query(() => getLiterature()),
    document: protectedProcedure.input(z.object({ slug: z.string() })).query(({ input }) => getDocument(input.slug)),
    incidents: protectedProcedure.query(() => getIncidents()),
    experiments: protectedProcedure.query(() => getExperiments()),
  }),
  admin: router({
    overview: adminProcedure.query(async () => {
      const [users, content, blogs, managed] = await Promise.all([listResearchUsers(), listContentRecords(), listBlogPosts(), listManagedRecords()]);
      return { users, content, blogs, ...managed, databaseConnected: Boolean(process.env.POSTGRES_DATABASE_URL) };
    }),
    saveContent: adminProcedure.input(z.object({ slug: z.string().min(2), title: z.string().min(2), category: z.string().min(2), sourceFile: z.string().optional(), status: z.enum(["draft", "published", "archived"]), summary: z.string().optional() })).mutation(({ input }) => saveContentRecord(input)),
    saveBlog: adminProcedure.input(z.object({ slug: z.string().min(2), title: z.string().min(2), excerpt: z.string().optional(), body: z.string().optional(), status: z.enum(["draft", "published", "archived"]) })).mutation(({ input, ctx }) => saveBlogPost({ ...input, authorOpenId: ctx.user.openId })),
  }),
});

export type AppRouter = typeof appRouter;
