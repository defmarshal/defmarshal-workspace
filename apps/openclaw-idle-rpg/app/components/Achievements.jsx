'use client';

export default function Achievements({ achieved, achievementsList }) {
  return (
    <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
      <h3 className="text-lg font-semibold mb-3">Achievements</h3>
      <div className="grid grid-cols-2 gap-2">
        {achievementsList.map(a => {
          const isDone = achieved.includes(a.id);
          return (
            <div key={a.id} className={`p-2 rounded text-sm ${isDone ? 'bg-green-900/30 text-green-300' : 'bg-gray-900 text-gray-500'}`}>
              <div className="font-medium">{a.name}</div>
              <div className="text-xs">{a.desc}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
