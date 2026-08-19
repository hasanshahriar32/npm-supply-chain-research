import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

const slugify = (value: string) => value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");

export function MarkdownReader({ markdown }: { markdown: string }) {
  const headings = markdown
    .split(/\r?\n/)
    .filter((line) => line.startsWith("## "))
    .map((line) => line.slice(3));
  const headingIds = new Map<string, number>();
  const nextHeadingId = (text: string) => {
    const base = slugify(text);
    const count = headingIds.get(base) ?? 0;
    headingIds.set(base, count + 1);
    return count ? `${base}-${count + 1}` : base;
  };

  return <div className="document-layout"><article className="markdown"><ReactMarkdown remarkPlugins={[remarkGfm]} components={{
    h1: ({ children }) => <h1>{children}</h1>,
    h2: ({ children }) => { const text = String(children); return <h2 id={nextHeadingId(text)}>{children}</h2>; },
    h3: ({ children }) => <h3>{children}</h3>,
    a: ({ href, children }) => <a href={href} target="_blank" rel="noreferrer">{children}</a>,
  }}>{markdown}</ReactMarkdown></article><aside className="contents"><p>On this page</p>{headings.map((heading, index) => <a key={`${heading}-${index}`} href={`#${slugify(heading)}`}>{String(index + 1).padStart(2, "0")} / {heading}</a>)}</aside></div>;
}
