'use client';

export default function TechTree({ upgrades, onPurchase, upgradesList }) {
  return (
    <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
      <h3 className="text-lg font-semibold mb-3">Tech Tree</h3>
      <div className="space-y-3">
        {upgradesList.map(tech => {
          const owned = upgrades.includes(tech.id);
          return (
            <div key={tech.id} className={`p-3 rounded border ${owned ? 'bg-green-900/30 border-green-700' : 'bg-gray-900 border-gray-700'}`}>
              <div className="flex justify-between items-center">
                <div>
                  <div className="font-medium">{tech.name}</div>
                  <div className="text-xs text-gray-400">{tech.desc}</div>
                </div>
                {!owned ? (
                  <button
                    onClick={() => onPurchase(tech)}
                    className="px-3 py-1 bg-indigo-600 hover:bg-indigo-700 rounded text-sm"
                  >
                    Purchase
                  </button>
                ) : (
                  <span className="text-green-400 text-sm">✓ Owned</span>
                )}
              </div>
              <div className="text-xs text-gray-400 mt-2">
                Cost: {Object.entries(tech.cost).map(([k,v]) => `${v} ${k}`).join(', ') || 'Free'}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
