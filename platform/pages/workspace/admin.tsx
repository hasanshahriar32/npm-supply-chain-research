import type { GetServerSidePropsContext } from "next";

export async function getServerSideProps(_context: GetServerSidePropsContext) {
  return { redirect: { destination: "/admin", permanent: false } };
}

export default function RetiredWorkspaceAdmin() { return null; }
