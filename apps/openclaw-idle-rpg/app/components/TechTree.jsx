'use client';

export default function TechTree({ upgrades, onPurchase, upgradesList }) {
  return (
    <div className="kawaii-card max-w-2xl mx-auto">
      <h3 className="text-lg font-bold text-purple-600 mb-4 flex items-center gap-2">🔧 Tech Tree</h3>
      <div className="grid gap-3">
        {upgradesList.map(tech => {
          const owned = upgrades.includes(tech.id);
          return (
            <div
              key={tech.id}
              className={`p-4 rounded-2xl border-2 transition-all ${
                owned
                  ? 'bg-green-100/60 border-green-300 shadow-sm'
                  : 'bg-white/60 border-pink-200 hover:shadow-md'
              }`}
            >
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-bold text-purple-700">{tech.name}</div>
                  <div className="text-xs text-pink-500 mt-1">{tech.desc}</div>
                </div>
                {!owned ? (
                  <button
                    onClick={() => onPurchase(tech)}
                    className="kawaii-btn text-sm px-3 py-1"
                  >
                    💖 Purchase
                  </button>
                ) : (
                  <span className="text-green-600 font-bold flex items-center gap-1">
                    <span>✔</span> Owned
                  </span>
                )}
              </div>
              <div className="text-xs text-purple-500 mt-2">
                Cost: {Object.entries(tech.cost).map(([k,v]) => `${v} ${k === 'memory' ? '💾' : k === 'cpu' ? '⚡' : k === 'tokens' ? '🔮' : k} ${v > 1 ? 'each' : ''}`).join(', ') || 'Free'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
