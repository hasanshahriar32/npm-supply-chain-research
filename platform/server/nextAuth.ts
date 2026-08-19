import axios from "axios";
import { parse } from "cookie";
import { SignJWT, jwtVerify } from "jose";
import type { NextApiRequest, NextApiResponse } from "next";
import { getResearchUser, upsertResearchUser } from "./platformDb";

const SESSION_COOKIE = "research_platform_session";
const STATE_COOKIE = "__Host-research_oauth_state";
const YEAR_MS = 365 * 24 * 60 * 60 * 1000;

type Session = { openId: string; name: string; email?: string | null; role: "admin" | "researcher" };
type CookieRequest = { headers: { cookie?: string | string[] | undefined } };

const getSecret = () => new TextEncoder().encode(process.env.JWT_SECRET ?? "development-secret-change-me");

const asBase64Url = (value: unknown) => Buffer.from(JSON.stringify(value)).toString("base64url");
const fromBase64Url = <T,>(value: string): T | null => {
  try { return JSON.parse(Buffer.from(value, "base64url").toString("utf8")) as T; } catch { return null; }
};

function serializeCookie(name: string, value: string, options: { secure: boolean; maxAge: number }) {
  const parts = [`${name}=${encodeURIComponent(value)}`, "Path=/", "HttpOnly", "SameSite=Lax", `Max-Age=${options.maxAge}`];
  if (options.secure) parts.push("Secure");
  return parts.join("; ");
}

export function isSecureRequest(req: NextApiRequest) {
  return (req.headers["x-forwarded-proto"] ?? "").toString().includes("https") || process.env.NODE_ENV === "production";
}

export async function createSession(session: Session) {
  return new SignJWT(session).setProtectedHeader({ alg: "HS256" }).setIssuedAt().setExpirationTime("365d").sign(getSecret());
}

export async function getSession(req: CookieRequest): Promise<Session | null> {
  const rawCookie = Array.isArray(req.headers.cookie) ? req.headers.cookie.join("; ") : req.headers.cookie ?? "";
  const token = parse(rawCookie)[SESSION_COOKIE];
  if (!token) return null;
  try {
    const { payload } = await jwtVerify(token, getSecret(), { algorithms: ["HS256"] });
    if (typeof payload.openId !== "string" || typeof payload.name !== "string") return null;
    return { openId: payload.openId, name: payload.name, email: typeof payload.email === "string" ? payload.email : null, role: payload.role === "admin" ? "admin" : "researcher" };
  } catch { return null; }
}

export async function getAuthenticatedUser(req: CookieRequest) {
  const session = await getSession(req);
  if (!session) return null;
  const dbUser = await getResearchUser(session.openId).catch(() => null);
  return { ...session, role: dbUser?.role === "admin" || session.openId === process.env.OWNER_OPEN_ID ? "admin" as const : "researcher" as const };
}

export function setSessionCookie(res: NextApiResponse, token: string, secure: boolean) {
  res.setHeader("Set-Cookie", serializeCookie(SESSION_COOKIE, token, { secure, maxAge: YEAR_MS / 1000 }));
}

export function clearSessionCookie(res: NextApiResponse, secure: boolean) {
  res.setHeader("Set-Cookie", serializeCookie(SESSION_COOKIE, "", { secure, maxAge: 0 }));
}

export function buildLoginUrl(req: NextApiRequest, res: NextApiResponse) {
  const origin = `${isSecureRequest(req) ? "https" : "http"}://${req.headers.host}`;
  const redirectUri = `${origin}/api/auth/callback`;
  const nonce = crypto.randomUUID();
  const state = asBase64Url({ redirectUri, nonce });
  res.setHeader("Set-Cookie", serializeCookie(STATE_COOKIE, nonce, { secure: isSecureRequest(req), maxAge: 600 }));
  const portal = process.env.VITE_OAUTH_PORTAL_URL ?? "";
  const appId = process.env.VITE_APP_ID ?? "";
  return `${portal}/login?${new URLSearchParams({ app_id: appId, redirect_url: redirectUri, state }).toString()}`;
}

export async function completeOAuth(req: NextApiRequest, res: NextApiResponse) {
  const code = typeof req.query.code === "string" ? req.query.code : "";
  const rawState = typeof req.query.state === "string" ? req.query.state : "";
  const state = fromBase64Url<{ redirectUri: string; nonce: string }>(rawState);
  const expectedNonce = parse(req.headers.cookie ?? "")[STATE_COOKIE];
  if (!code || !state?.nonce || state.nonce !== expectedNonce) throw new Error("Invalid OAuth state");
  const api = axios.create({ baseURL: process.env.OAUTH_SERVER_URL, timeout: 30_000 });
  const exchange = await api.post("/webdev.v1.WebDevAuthPublicService/ExchangeToken", { clientId: process.env.VITE_APP_ID, grantType: "authorization_code", code, redirectUri: state.redirectUri });
  const userInfo = await api.post("/webdev.v1.WebDevAuthPublicService/GetUserInfo", { accessToken: exchange.data.accessToken });
  const user = userInfo.data as { openId?: string; name?: string; email?: string; loginMethod?: string };
  if (!user.openId) throw new Error("OAuth user information was incomplete");
  const dbUser = await upsertResearchUser({ openId: user.openId, name: user.name ?? null, email: user.email ?? null }).catch(() => null);
  const session = await createSession({ openId: user.openId, name: user.name ?? "Researcher", email: user.email ?? null, role: dbUser?.role === "admin" || user.openId === process.env.OWNER_OPEN_ID ? "admin" : "researcher" });
  setSessionCookie(res, session, isSecureRequest(req));
  res.setHeader("Set-Cookie", [res.getHeader("Set-Cookie") as string, serializeCookie(STATE_COOKIE, "", { secure: isSecureRequest(req), maxAge: 0 })]);
}
