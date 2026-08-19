import type { NextApiRequest, NextApiResponse } from "next";
import { buildLoginUrl } from "../../../server/nextAuth";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "GET") return res.status(405).end();
  return res.redirect(302, buildLoginUrl(req, res));
}
