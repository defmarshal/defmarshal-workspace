'use client';

export default function Achievements({ achieved, achievementsList }) {
  return (
    <div className="kawaii-card max-w-2xl mx-auto">
      <h3 className="text-lg font-bold text-purple-600 mb-4 flex items-center gap-2">🏆 Achievements</h3>
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {achievementsList.map(a => {
          const isDone = achieved.includes(a.id);
          return (
            <div
              key={a.id}
              className={`p-3 rounded-2xl border-2 text-center transition-all ${
                isDone
                  ? 'bg-yellow-100/60 border-yellow-300 shadow-sm scale-105'
                  : 'bg-white/40 border-pink-200 opacity-60'
              }`}
            >
              <div className="text-2xl mb-1">{isDone ? '🌟' : '☆'}</div>
              <div className="font-bold text-purple-700 text-sm">{a.name}</div>
              <div className="text-xs text-pink-500 mt-1">{a.desc}</div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
