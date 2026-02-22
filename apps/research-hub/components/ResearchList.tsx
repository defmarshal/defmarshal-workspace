"use client";

import { format, parseISO, isValid } from "date-fns";

export type ResearchItem = {
  slug: string;
  title: string;
  date: string;
  excerpt: string;
  hasAudio: boolean;
};

interface ResearchListProps {
  items: ResearchItem[];
}

function safeFormatDate(dateStr: string): string {
  try {
    const parsed = parseISO(dateStr);
    if (isValid(parsed)) {
      return format(parsed, "MMMM d, yyyy");
    }
  } catch {
    // fall through
  }
  return dateStr; // raw if unparsable
}

export default function ResearchList({ items }: ResearchListProps) {
  if (items.length === 0) {
    return <p className="text-muted-foreground">No research found.</p>;
  }

  return (
    <div className="space-y-6">
      {items.map((item) => (
        <article
          key={item.slug}
          className="border rounded-lg p-6 hover:shadow-md transition-shadow"
        >
          <time className="text-sm text-muted-foreground">
            {safeFormatDate(item.date)}
          </time>
          <h2 className="text-2xl font-semibold mt-1 mb-3">{item.title}</h2>
          <p className="text-muted-foreground mb-4">{item.excerpt}</p>
          <div className="flex items-center gap-3">
            <a
              href={`/research/${item.slug}`}
              className="inline-flex items-center justify-center rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
            >
              Read more
            </a>
            {item.hasAudio && (
              <span
                className="inline-flex items-center gap-1 text-xs font-medium text-green-700 dark:text-green-400 bg-green-100 dark:bg-green-900/30 px-2 py-1 rounded-full"
                title="Audio narration available"
              >
                🔊 Audio
              </span>
            )}
          </div>
        </article>
      ))}
    </div>
  );
}
