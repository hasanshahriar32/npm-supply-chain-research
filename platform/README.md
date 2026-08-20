# Supply Chain Research Hub

This application is a **Next.js 16 research platform** for the `npm-supply-chain-research` repository. It presents a public editorial landing page and a Clerk-protected workspace for reviewing the research corpus, benchmark snapshot, incident labels, and experiment plan.

## Architecture

| Layer | Implementation |
|---|---|
| Public experience | `pages/index.tsx`, an editorial research-preview landing page |
| Authentication | Clerk `ClerkProvider`, `proxy.ts` middleware, and server-side `getAuth()` checks close to protected resources |
| Workspace | Server-rendered protected routes under `pages/workspace/*` |
| Data API | tRPC route at `pages/api/trpc/[trpc].ts` backed by `server/researchRouter.ts` |
| Research corpus | Markdown and CSV files copied from the repository root `research/` directory |
| Persistent administration | PostgreSQL with Drizzle schema in `drizzle/researchSchema.ts` |
| Content operations | Extensible administration UI for users, content metadata, editorial posts, benchmark snapshots, incident labels, and experiments |

The exact workspace navigation sections are **Literature Review**, **Gap Analysis**, **Benchmark Findings**, **Methodology**, **Incident Labels**, and **Experiment Results**. The literature table reads `research/11_literature_matrix.csv` and the Markdown readers source their content from the local `research/` directory.

## Required environment variables

The application needs two Clerk keys plus the PostgreSQL connection URL. The Clerk keys are available in your Clerk Dashboard under **Configure → API Keys**. The PostgreSQL adapter requires encrypted transport enabled by the server or connection string.

```text
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...
CLERK_SECRET_KEY=sk_...
POSTGRES_DATABASE_URL=postgresql://...
```

For a Vercel deployment, add the same values in **Project Settings → Environment Variables**, plus a server-only `GITHUB_TOKEN` with **Contents: Read** access to `ashik-hstu/npm-supply-chain-research` and a random `CRON_SECRET` with at least 16 characters. The included `vercel.json` runs `GET /api/cron/research-ingestion` daily at **03:00 UTC**. Each execution retrieves the latest committed metrics archive from the private repository, creates a **pending** benchmark snapshot, and requires administrator publication before it becomes current.[1]

## Clerk administrator access

All signed-in Clerk users may access the research workspace. To grant administration access, open **Clerk Dashboard → Users → select the user → Public metadata** and save the following JSON:

```json
{ "role": "admin" }
```

The platform reads this value at sign-in, protects `/workspace/admin` and admin tRPC procedures, and mirrors the resolved role into the local PostgreSQL user record for reporting. Do not grant the administrator role through a browser-visible environment variable.

## References

[1]: https://vercel.com/docs/cron-jobs "Vercel Cron Jobs"

## Database setup

Run the idempotent migration and seed scripts after providing `POSTGRES_DATABASE_URL`:

```bash
node scripts/migrate-research.mjs
node scripts/seed-research.mjs
```

The seed imports only existing repository-backed research metadata, the inspected benchmark snapshot, and the documented Shai-Hulud and Axios incident anchors. It does not insert fabricated reviews, ratings, testimonials, or research findings.

## Development and verification

```bash
pnpm dev
pnpm build
pnpm test
```

The targeted tests cover Clerk connectivity, PostgreSQL connectivity, route protection, and the research-source values served by the platform.

## Keeping research current

`research/` is the current canonical source of the research materials. When the research repository changes, sync the updated Markdown and CSV files into the application’s `research/` directory, redeploy, and optionally update the database-backed content metadata from Administration. No unattended synchronization is configured.
