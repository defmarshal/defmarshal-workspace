import ResearchClient from "@/components/ResearchClient";
import matter from "gray-matter";
import { remark } from "remark";
import html from "remark-html";
import gfm from "remark-gfm";
import { readdir, readFile, access } from "fs/promises";
import { join } from "path";

export const dynamic = "force-dynamic"; // avoid caching

export default async function HomePage() {
  const RESEARCH_DIR = join(process.cwd(), "public", "research");
  let researchData: { slug: string; title: string; date: string; excerpt: string; hasAudio: boolean }[] = [];

  try {
    const files = await readdir(RESEARCH_DIR).catch(() => []);
    const markdownFiles = files.filter((f) => f.endsWith(".md"));

    researchData = await Promise.all(
      markdownFiles.map(async (filename) => {
        const slug = filename.replace(/\.md$/, "");
        const fullPath = join(RESEARCH_DIR, filename);
        const fileContent = await readFile(fullPath, "utf8");
        const { data, content } = matter(fileContent);
        const processed = await remark()
          .use(gfm)
          .use(html)
          .process(content);
        const htmlContent = processed.toString();

        // Check if audio file exists
        const audioPath = join(RESEARCH_DIR, `${slug}.mp3`);
        let hasAudio = false;
        try {
          await access(audioPath);
          hasAudio = true;
        } catch {
          // no audio
        }

        return {
          slug,
          title: data.title || slug,
          date: data.date || slug.split("-").slice(0, 3).join("-"),
          excerpt: htmlContent.slice(0, 200).replace(/<[^>]*>?/gm, "") + "...",
          hasAudio,
        };
      })
    );

    // Sort by date descending
    researchData.sort((a, b) => (b.date > a.date ? 1 : -1));
  } catch (error) {
    console.error("Error reading research directory:", error);
  }

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">Research Hub</h1>
          <p className="text-muted-foreground text-lg">
            Insights on AI, web development, infrastructure, and more.
          </p>
        </header>

        <ResearchClient initialData={researchData} />
      </div>
    </main>
  );
}
