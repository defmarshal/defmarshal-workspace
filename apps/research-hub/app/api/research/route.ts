import { NextResponse } from "next/server";
import matter from "gray-matter";
import { remark } from "remark";
import html from "remark-html";
import { readdir, readFile } from "fs/promises";
import { join } from "path";

const RESEARCH_DIR = join(process.cwd(), "public", "research");

export async function GET() {
  try {
    const files = await readdir(RESEARCH_DIR).catch(() => []);
    const markdownFiles = files.filter((f) => f.endsWith(".md"));

    const research = await Promise.all(
      markdownFiles.map(async (filename) => {
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
        };
      })
    );

    // Sort by date descending
    research.sort((a, b) => (b.date > a.date ? 1 : -1));

    return NextResponse.json(research);
  } catch (error) {
    console.error("Error reading research directory:", error);
    return NextResponse.json({ error: "Failed to fetch research" }, { status: 500 });
  }
}
