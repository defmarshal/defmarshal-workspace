export default function EventLog({ entries }) {
  if (entries.length === 0) {
    return <div className="text-gray-500 italic">No events yet...</div>;
  }
  return (
    <div className="bg-gray-800 p-4 rounded-lg border border-gray-700 h-48 overflow-y-auto font-mono text-sm">
      {entries.map((entry, i) => (
        <div key={i} className="mb-1 text-gray-300">{entry}</div>
      ))}
    </div>
  );
}
