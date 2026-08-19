import "./styles/globals.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { httpBatchLink } from "@trpc/client";
import { ClerkProvider } from "@clerk/nextjs";
import type { AppProps } from "next/app";
import { useState } from "react";
import { trpc } from "../lib/trpc";

export default function App({ Component, pageProps }: AppProps) {
  const [queryClient] = useState(() => new QueryClient());
  const [trpcClient] = useState(() => trpc.createClient({ links: [httpBatchLink({ url: "/api/trpc" })] }));
  return <ClerkProvider {...pageProps} afterSignOutUrl="/" signInFallbackRedirectUrl="/workspace/literature-review" signUpFallbackRedirectUrl="/workspace/literature-review"><trpc.Provider client={trpcClient} queryClient={queryClient}><QueryClientProvider client={queryClient}><Component {...pageProps} /></QueryClientProvider></trpc.Provider></ClerkProvider>;
}
