export default function EventLog({ entries }) {
  if (entries.length === 0) {
    return (
      <div className="kawaii-card text-center text-pink-400 italic py-8">
        ✨ No events yet... Start playing to see magic! ✨
      </div>
    );
  }
  return (
    <div className="kawaii-card h-48 overflow-y-auto p-4 text-sm">
      {entries.map((entry, i) => (
        <div key={i} className="mb-2 text-purple-700 flex items-start gap-2">
          <span className="text-pink-400">•</span>
          <span>{entry}</span>
        </div>
      ))}
    </div>
  );
}

