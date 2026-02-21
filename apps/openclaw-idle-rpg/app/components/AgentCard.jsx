export default function AgentCard({ agent, onUpgrade, resources, onUseAbility, abilityCooldown }) {
  const cost = Math.floor(10 * Math.pow(agent.costMultiplier, agent.level));
  const canAfford = resources >= cost;
  const rate = (agent.baseRate * agent.level).toFixed(2);
  const ability = agent.ability;
  const onCooldown = abilityCooldown > 0;
  const cooldownTotal = ability?.cooldown || 0;
  const cooldownPercent = cooldownTotal > 0 ? ((cooldownTotal - abilityCooldown) / cooldownTotal) * 100 : 0;

  return (
    <div className={`bg-gray-800 p-4 rounded-lg border ${onCooldown ? 'border-gray-600 opacity-75' : 'border-indigo-500'}`}>
      <div className="flex justify-between items-center mb-2">
        <h3 className="text-lg font-semibold">{agent.name}</h3>
        <span className="text-sm bg-gray-700 px-2 py-1 rounded">Lv {agent.level}</span>
      </div>
      <div className="text-sm text-gray-400 mb-3">
        Produces ~{rate} resources/sec
      </div>
      <button
        onClick={() => canAfford && onUpgrade(agent.id)}
        disabled={!canAfford}
        className={`w-full py-2 rounded font-medium mb-2 transition-transform active:scale-95 ${
          canAfford
            ? 'bg-indigo-600 hover:bg-indigo-700 text-white hover:shadow-lg'
            : 'bg-gray-700 text-gray-500 cursor-not-allowed'
        }`}
      >
        Upgrade ({cost} Memory)
      </button>
      {ability && (
        <div className="border-t border-gray-700 pt-2 mt-2">
          <button
            onClick={() => onUseAbility()}
            disabled={onCooldown}
            title={ability.desc}
            className={`w-full py-2 rounded text-sm font-medium flex items-center justify-center gap-2 relative overflow-hidden ${
              onCooldown
                ? 'bg-gray-600 text-gray-400 cursor-not-allowed'
                : 'bg-pink-600 hover:bg-pink-700 text-white hover:shadow-lg'
            }`}
          >
            {onCooldown && (
              <div className="absolute inset-0 bg-black/30" style={{ width: `${cooldownPercent}%` }} />
            )}
            <span className="relative z-10">{ability.name}</span>
            {onCooldown && <span className="relative z-10 text-xs">({(abilityCooldown/1000).toFixed(0)}s)</span>}
          </button>
          <div className="text-xs text-gray-400 mt-1">{ability.desc}</div>
        </div>
      )}
    </div>
  );
}

