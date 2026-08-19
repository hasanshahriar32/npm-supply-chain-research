import type { NextApiRequest, NextApiResponse } from "next";
import { completeOAuth } from "../../../server/nextAuth";

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  try {
    await completeOAuth(req, res);
    res.redirect(302, "/workspace/literature-review");
  } catch (error) {
    res.status(403).json({ error: error instanceof Error ? error.message : "OAuth authentication failed" });
  }
}
