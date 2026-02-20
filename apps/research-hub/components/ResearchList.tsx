import matter from "gray-matter";
import { remark } from "remark";
import html from "remark-html";
import { format } from "date-fns";
import { readFile } from "fs/promises";
import { join } from "path";

type ResearchFile = {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
  content: string;
};

const RESEARCH_DIR = join(process.cwd(), "public", "research");

async function getResearch(): Promise<ResearchFile[]> {
  try {
    const files = await readFile(RESEARCH_DIR).catch(() => []);
    const markdownFiles = files.filter((f: string) => f.endsWith(".md"));

    const research = await Promise.all(
      markdownFiles.map(async (filename: string) => {
        const slug = filename.replace(/\.md$/, "");
        const fullPath = join(RESEARCH_DIR, filename);
        const fileContent = await readFile(fullPath, "utf8");
        const { data, content } = matter(fileContent);
        const processed = await remark().use(html).process(content);
        const htmlContent = processed.toString();

        return {
          slug,
          title: data.title || slug,
          date: data.date || slug.split("-").slice(0, 3).join("-"),
          excerpt: htmlContent.slice(0, 200).replace(/<[^>]*>?/gm, "") + "...",
          content: htmlContent,
        };
      })
    );

    return research.sort((a, b) => (b.date > a.date ? 1 : -1));
  } catch (error) {
    console.error("Error reading research directory:", error);
    return [];
  }
}

export default async function ResearchList() {
  const research = await getResearch();

  if (research.length === 0) {
    return <p className="text-muted-foreground">No research found.</p>;
  }

  return (
    <div className="space-y-6">
      {research.map((item) => (
        <article
          key={item.slug}
          className="border rounded-lg p-6 hover:shadow-md transition-shadow"
        >
          <time className="text-sm text-muted-foreground">
            {format(new Date(item.date), "MMMM d, yyyy")}
          </time>
          <h2 className="text-2xl font-semibold mt-1 mb-3">{item.title}</h2>
          <p className="text-muted-foreground mb-4">{item.excerpt}</p>
          <a
            href={`/research/${item.slug}`}
            className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
          >
            Read more
          </a>
        </article>
      ))}
    </div>
  );
}
