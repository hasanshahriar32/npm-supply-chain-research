import { z } from "zod";
import { getCurrentSnapshot, listBlogPosts, listContentRecords, listManagedRecords, listResearchUsers, listSnapshotHistory, reviewContentRecord, reviewSnapshot, saveBlogPost, saveContentRecord, updateResearchUserRole } from "./platformDb";
import { getChartData, getDocument, getDocuments, getExperiments, getIncidents, getLiterature, getSourceSnapshot } from "./researchSources";
import { ingestMetricsArchive } from "./researchIngestion";
import { setClerkResearchUserRole } from "./clerkAuth";
import { adminProcedure, protectedProcedure, publicProcedure, router } from "./trpc";

const contentStatus = z.enum(["draft", "pending", "approved", "published", "rejected", "archived"]);
const reviewStatus = z.enum(["approved", "published", "rejected"]);

export const appRouter = router({
  auth: router({ me: publicProcedure.query(({ ctx }) => ctx.user) }),
  research: router({
    overview: protectedProcedure.query(async () => {
      const current = await getCurrentSnapshot();
      const snapshot = current ? { packages: current.packages, versions: current.versions, maintainers: current.maintainers, dependencyEdges: current.dependencyEdges, repositoryMappings: current.repositoryMappings, workflowChecks: current.workflowChecks, workflowCoverage: current.workflowDetections / current.workflowChecks, advisoryRecords: current.advisoryRecords, metricsRecords: current.metricsRecords } : await getSourceSnapshot();
      return { snapshot, documents: await getDocuments(), incidents: getIncidents(), experiments: getExperiments() };
    }),
    analytics: protectedProcedure.query(async () => {
      const current = await getCurrentSnapshot();
      if (current?.chartData && typeof current.chartData === "object") return current.chartData as Awaited<ReturnType<typeof getChartData>>;
      return getChartData();
    }),
    literature: protectedProcedure.query(() => getLiterature()),
    document: protectedProcedure.input(z.object({ slug: z.string() })).query(({ input }) => getDocument(input.slug)),
    incidents: protectedProcedure.query(() => getIncidents()),
    experiments: protectedProcedure.query(() => getExperiments()),
  }),
  admin: router({
    overview: adminProcedure.query(async () => {
      const [users, content, blogs, managed, history] = await Promise.all([listResearchUsers(), listContentRecords(), listBlogPosts(), listManagedRecords(), listSnapshotHistory()]);
      return { users, content, blogs, ...managed, history, databaseConnected: Boolean(process.env.POSTGRES_DATABASE_URL) };
    }),
    saveContent: adminProcedure.input(z.object({ slug: z.string().min(2), title: z.string().min(2), category: z.string().min(2), sourceFile: z.string().optional(), status: contentStatus, summary: z.string().optional() })).mutation(({ input }) => saveContentRecord(input)),
    reviewContent: adminProcedure.input(z.object({ id: z.number().int().positive(), status: reviewStatus })).mutation(({ input, ctx }) => reviewContentRecord(input.id, input.status, ctx.user.openId)),
    saveBlog: adminProcedure.input(z.object({ slug: z.string().min(2), title: z.string().min(2), excerpt: z.string().optional(), body: z.string().optional(), status: contentStatus })).mutation(({ input, ctx }) => saveBlogPost({ ...input, authorOpenId: ctx.user.openId })),
    setUserRole: adminProcedure.input(z.object({ openId: z.string().min(1), role: z.enum(["admin", "researcher"]) })).mutation(async ({ input, ctx }) => {
      if (input.openId === ctx.user.openId && input.role !== "admin") throw new Error("You cannot remove your own administrator access.");
      await setClerkResearchUserRole(input.openId, input.role);
      return updateResearchUserRole(input.openId, input.role);
    }),
    reviewSnapshot: adminProcedure.input(z.object({ id: z.number().int().positive(), status: reviewStatus })).mutation(({ input, ctx }) => reviewSnapshot(input.id, input.status, ctx.user.openId)),
    runIngestion: adminProcedure.mutation(() => ingestMetricsArchive()),
  }),
});

export type AppRouter = typeof appRouter;
