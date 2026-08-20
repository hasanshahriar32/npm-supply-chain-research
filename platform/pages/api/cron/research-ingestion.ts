import type { NextApiRequest, NextApiResponse } from "next";
import { ingestMetricsArchive } from "../../../server/researchIngestion";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "GET") return res.status(405).json({ error: "method_not_allowed" });
  const expected = process.env.CRON_SECRET;
  if (!expected || req.headers.authorization !== `Bearer ${expected}`) return res.status(401).json({ error: "unauthorized" });
  try {
    const result = await ingestMetricsArchive();
    return res.status(200).json({ ok: true, result });
  } catch (error) {
    return res.status(500).json({ ok: false, error: error instanceof Error ? error.message : "ingestion_failed" });
  }
}
