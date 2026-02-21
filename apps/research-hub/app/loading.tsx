export default function Loading() {
  return (
    <main className="min-h-screen bg-background p-8">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="space-y-2">
          <div className="h-10 w-64 bg-muted animate-pulse rounded" />
          <div className="h-6 w-96 bg-muted animate-pulse rounded" />
        </header>

        {/* Search skeleton */}
        <div className="flex justify-center">
          <div className="h-10 w-full max-w-md bg-muted animate-pulse rounded" />
        </div>

        {/* Stats skeleton */}
        <div className="text-center">
          <div className="h-4 w-48 bg-muted animate-pulse rounded mx-auto" />
        </div>

        {/* List skeletons */}
        <div className="space-y-4">
          {Array.from({ length: 10 }).map((_, i) => (
            <div key={i} className="border rounded-lg p-4 space-y-3">
              <div className="h-6 w-3/4 bg-muted animate-pulse rounded" />
              <div className="h-4 w-1/4 bg-muted animate-pulse rounded" />
              <div className="h-4 w-full bg-muted animate-pulse rounded" />
              <div className="h-4 w-2/3 bg-muted animate-pulse rounded" />
            </div>
          ))}
        </div>

        {/* Pagination skeleton */}
        <div className="flex justify-center items-center gap-4">
          <div className="h-9 w-20 bg-muted animate-pulse rounded" />
          <div className="h-4 w-24 bg-muted animate-pulse rounded" />
          <div className="h-9 w-20 bg-muted animate-pulse rounded" />
        </div>
      </div>
    </main>
  );
}
