# Supply Chain Research Hub

This application is a **Next.js 16 research platform** for the `npm-supply-chain-research` repository. It presents a public editorial landing page and a Manus OAuth–protected workspace for reviewing the research corpus, benchmark snapshot, incident labels, and experiment plan.

## Architecture

| Layer | Implementation |
|---|---|
| Public experience | `pages/index.tsx`, an editorial research-preview landing page |
| Authentication | Manus OAuth routes under `pages/api/auth/*`, with a signed, HTTP-only research session cookie |
| Workspace | Server-rendered protected routes under `pages/workspace/*` |
| Data API | tRPC route at `pages/api/trpc/[trpc].ts` backed by `server/researchRouter.ts` |
| Research corpus | Markdown and CSV files copied from the repository root `research/` directory |
| Persistent administration | PostgreSQL with Drizzle schema in `drizzle/researchSchema.ts` |
| Content operations | Extensible administration UI for users, content metadata, editorial posts, benchmark snapshots, incident labels, and experiments |

The exact workspace navigation sections are **Literature Review**, **Gap Analysis**, **Benchmark Findings**, **Methodology**, **Incident Labels**, and **Experiment Results**. The literature table reads `research/11_literature_matrix.csv` and the Markdown readers source their content from the local `research/` directory.

## Required environment variables

The managed runtime supplies the Manus OAuth variables. The PostgreSQL adapter additionally requires `POSTGRES_DATABASE_URL` with encrypted transport enabled by the server or connection string.

```text
POSTGRES_DATABASE_URL=postgresql://...
VITE_APP_ID=...
VITE_OAUTH_PORTAL_URL=...
OAUTH_SERVER_URL=...
JWT_SECRET=...
OWNER_OPEN_ID=...
```

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

The targeted tests cover PostgreSQL connectivity, session protection, and the research-source values served by the platform.

## Keeping research current

`research/` is the current canonical source of the research materials. When the research repository changes, sync the updated Markdown and CSV files into the application’s `research/` directory, redeploy, and optionally update the database-backed content metadata from Administration. No unattended synchronization is configured.
