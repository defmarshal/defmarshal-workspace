import { NextResponse } from 'next/server';
import matter from 'gray-matter';
import { readdir, readFile } from 'fs/promises';
import { join } from 'path';

function xmlEscape(str: string): string {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

export async function GET() {
  const RESEARCH_DIR = join(process.cwd(), 'public', 'research');
  const files = await readdir(RESEARCH_DIR).catch(() => []);
  const markdownFiles = files.filter((f) => f.endsWith('.md'));

  const items = await Promise.all(
    markdownFiles.map(async (filename) => {
      const slug = filename.replace(/\.md$/, '');
      const fullPath = join(RESEARCH_DIR, filename);
      let fileContent: string;
      try {
        fileContent = await readFile(fullPath, 'utf8');
      } catch {
        return null;
      }
      const { data, content } = matter(fileContent);
      const dateStr = data.date || filename.split('-').slice(0, 3).join('-');
      const pubDate = new Date(dateStr).toUTCString();
      return {
        slug,
        title: data.title || slug,
        description: content.slice(0, 160).replace(/\n/g, ' '),
        pubDate,
      };
    })
  );

  const validItems = items.filter((i): i is NonNullable<typeof i> => i !== null);
  validItems.sort((a, b) => new Date(b.pubDate).getTime() - new Date(a.pubDate).getTime());

  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL || 'https://research-hub-flame.vercel.app';
  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Research Hub Feed</title>
  <link>${siteUrl}</link>
  <description>Latest research reports on AI, tech, and infrastructure</description>
  <lastBuildDate>${new Date().toUTCString()}</lastBuildDate>
  ${validItems.map(item => `
  <item>
    <title>${xmlEscape(item.title)}</title>
    <link>${siteUrl}/research/${item.slug}</link>
    <description>${xmlEscape(item.description)}...</description>
    <pubDate>${item.pubDate}</pubDate>
    <guid>${siteUrl}/research/${item.slug}</guid>
  </item>`).join('\n')}
</channel>
</rss>`;

  return new NextResponse(rss, {
    headers: {
      'Content-Type': 'application/rss+xml',
      'Cache-Control': 'public, max-age=3600',
    },
  });
}
