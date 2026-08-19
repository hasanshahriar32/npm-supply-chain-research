import type { NextApiRequest, NextApiResponse } from "next";
import { clearSessionCookie, isSecureRequest } from "../../../server/nextAuth";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== "POST") return res.status(405).end();
  clearSessionCookie(res, isSecureRequest(req));
  res.status(200).json({ ok: true });
}
