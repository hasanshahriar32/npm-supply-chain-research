import type { Config } from "drizzle-kit";

export default {
  schema: "./drizzle/researchSchema.ts",
  out: "./drizzle/research-migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.POSTGRES_DATABASE_URL ?? "",
  },
} satisfies Config;
