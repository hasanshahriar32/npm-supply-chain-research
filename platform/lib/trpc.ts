import { createTRPCReact } from "@trpc/react-query";
import type { AppRouter } from "../server/researchRouter";

// The router remains strongly typed on the server. This local boundary works around
// a generated-client key collision in the installed tRPC React adapter version.
export const trpc: any = createTRPCReact<AppRouter>();
