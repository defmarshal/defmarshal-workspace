import matter from "gray-matter";
import { remark } from "remark";
import html from "remark-html";
import { notFound } from "next/navigation";
import { readFile, access } from "fs/promises";
import { join } from "path";

type Props = {
  params: Promise<{ slug: string }>;
};

async function getResearchBySlug(slug: string) {
  const fullPath = join(process.cwd(), "public", "research", `${slug}.md`);
  try {
    const fileContent = await readFile(fullPath, "utf8");
    const { data, content } = matter(fileContent);
    const processed = await remark().use(html).process(content);
    const htmlContent = processed.toString();

    return {
      title: data.title || slug,
      date: data.date || slug.split("-").slice(0, 3).join("-"),
      content: htmlContent,
    };
  } catch (e) {
    return null;
  }
}

// Check if audio exists for this slug
async function hasAudio(slug: string): Promise<boolean> {
  const audioPath = join(process.cwd(), "public", "research", `${slug}.mp3`);
  try {
    await access(audioPath);
    return true;
  } catch {
    return false;
  }
}

export async function generateMetadata({ params }: Props) {
  const { slug } = await params;
  const research = await getResearchBySlug(slug);

  if (!research) {
    return { title: "Not Found" };
  }

  return {
    title: research.title,
  };
}

export default async function ResearchPage({ params }: Props) {
  const { slug } = await params;
  const research = await getResearchBySlug(slug);
  const audioAvailable = await hasAudio(slug);

  if (!research) {
    notFound();
  }

  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-6">
        <article className="prose prose-slate dark:prose-invert max-w-none">
          <header className="mb-8">
            <h1 className="text-4xl font-bold tracking-tight mb-2">
              {research.title}
            </h1>
            <time className="text-muted-foreground">
              {new Date(research.date).toLocaleDateString(undefined, {
                year: "numeric",
                month: "long",
                day: "numeric",
              })}
            </time>
            {audioAvailable && (
              <div className="mt-4">
                <audio controls className="w-full max-w-md">
                  <source src={`/research/${slug}.mp3`} type="audio/mpeg" />
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
          </header>
          <div
            className="research-content"
            dangerouslySetInnerHTML={{ __html: research.content }}
          />
        </article>
        <a
          href="/"
          className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-secondary text-secondary-foreground hover:bg-secondary/80 h-10 px-4 py-2"
        >
          ← Back to all research
        </a>
      </div>
    </main>
  );
}