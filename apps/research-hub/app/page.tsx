import ResearchList from "@/components/ResearchList";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="space-y-2">
          <h1 className="text-4xl font-bold tracking-tight">Research Hub</h1>
          <p className="text-muted-foreground text-lg">
            Insights on AI, web development, infrastructure, and more.
          </p>
        </header>

        <ResearchList />
      </div>
    </main>
  );
}
