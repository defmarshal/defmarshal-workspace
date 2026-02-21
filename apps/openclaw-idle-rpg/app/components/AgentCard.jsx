export default function AgentCard({ agent, onUpgrade, resources, onUseAbility, abilityCooldown }) {
  const cost = Math.floor(10 * Math.pow(agent.costMultiplier, agent.level));
  const canAfford = resources >= cost;
  const rate = (agent.baseRate * agent.level).toFixed(2);
  const ability = agent.ability;
  const onCooldown = abilityCooldown > 0;
  const cooldownTotal = ability?.cooldown || 0;
  const cooldownPercent = cooldownTotal > 0 ? ((cooldownTotal - abilityCooldown) / cooldownTotal) * 100 : 0;

  return (
    <div className={`kawaii-card relative overflow-hidden ${onCooldown ? 'opacity-80' : 'ability-ready'}`}>
      {/* Kawaii decorations */}
      <div className="absolute -top-2 -right-2 text-yellow-300 text-xl animate-sparkle">✦</div>

      <div className="flex justify-between items-center mb-3">
        <h3 className="text-lg font-bold text-purple-600">{agent.name}</h3>
        <span className="px-3 py-1 bg-gradient-to-r from-pink-300 to-purple-300 rounded-full text-purple-800 font-bold text-sm">
          Lv {agent.level}
        </span>
      </div>

      <div className="text-sm text-pink-500 mb-3 flex items-center gap-1">
        <span>⚡</span>
        <span>~{rate} resources/sec</span>
      </div>

      {/* Upgrade button */}
      <button
        onClick={() => canAfford && onUpgrade(agent.id)}
        disabled={!canAfford}
        className={`kawaii-btn w-full mb-3 ${!canAfford ? 'opacity-50 cursor-not-allowed' : ''}`}
      >
        <span className="flex items-center justify-center gap-2">
          <span>📈</span>
          <span>Upgrade</span>
          <span>{cost} 💾</span>
        </span>
      </button>

      {/* Ability section */}
      {ability && (
        <div className="border-t-2 border-pink-200 pt-3 mt-2">
          <button
            onClick={() => onUseAbility()}
            disabled={onCooldown}
            title={ability.desc}
            className={`w-full py-2 rounded-full text-sm font-bold flex items-center justify-center gap-2 relative overflow-hidden transition-all ${
              onCooldown
                ? 'bg-gray-200 text-gray-400 cursor-not-allowed'
                : 'bg-gradient-to-r from-purple-400 to-pink-400 text-white hover:shadow-lg hover:scale-105'
            }`}
          >
            {onCooldown && (
              <div className="absolute inset-0 bg-white/50" style={{ width: `${cooldownPercent}%` }} />
            )}
            <span className="relative z-10">{ability.name}</span>
            {onCooldown && <span className="relative z-10 text-xs">⏳ {(abilityCooldown/1000).toFixed(0)}s</span>}
            {!onCooldown && <span className="relative z-10">✨</span>}
          </button>
          <div className="text-xs text-purple-400 mt-2 text-center">{ability.desc}</div>
        </div>
      )}
    </div>
  );
}

