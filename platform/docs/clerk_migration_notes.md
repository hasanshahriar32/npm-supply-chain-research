# Clerk Migration Notes

The platform is using the Next.js Pages Router. The Clerk Pages Router quickstart requires `@clerk/nextjs`, a root-level `ClerkProvider`, and two user-controlled environment variables: `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` and `CLERK_SECRET_KEY`.[1]

Protected server-rendered pages and API routes should use `getAuth()` close to the protected resource. `buildClerkProps()` passes the authenticated server state to the client provider for Pages Router SSR.[2]

The platform will retain its tRPC router but replace the custom Manus session context with Clerk's `getAuth()` user identifier. Administrative authority will be determined by a Clerk public metadata role (`publicMetadata.role === "admin"`) rather than a platform owner environment variable. The public landing page remains unauthenticated.

## References

[1]: https://clerk.com/docs/getting-started/quickstart/pages-router "Clerk Next.js Pages Router quickstart"
[2]: https://clerk.com/docs/nextjs/guides/users/reading "Clerk user data in Next.js Pages Router"
