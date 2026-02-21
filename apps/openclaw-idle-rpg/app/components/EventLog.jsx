export default function EventLog({ entries }) {
  if (entries.length === 0) {
    return (
      <div className="kawaii-card text-center text-purple-800 italic py-12 text-2xl font-bold">
        ✨ No events yet... Start playing to see magic! ✨
      </div>
    );
  }
  return (
    <div className="kawaii-card h-64 overflow-y-auto p-6 text-lg font-bold">
      {entries.map((entry, i) => (
        <div key={i} className="mb-3 text-purple-900 flex items-start gap-3">
          <span className="text-pink-500 text-2xl">•</span>
          <span className="text-purple-800">{entry}</span>
        </div>
      ))}
    </div>
  );
}

