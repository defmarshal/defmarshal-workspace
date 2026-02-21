export default function AgentCard({ agent, onUpgrade, resources }) {
  const cost = Math.floor(10 * Math.pow(agent.costMultiplier, agent.level));
  const canAfford = resources >= cost;
  const rate = (agent.baseRate * agent.level).toFixed(2);

  return (
    <div className="bg-gray-800 p-4 rounded-lg border border-gray-700">
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
        className={`w-full py-2 rounded font-medium ${
          canAfford
            ? 'bg-mewmew-primary hover:bg-purple-600 text-white'
            : 'bg-gray-700 text-gray-500 cursor-not-allowed'
        }`}
      >
        Upgrade ({cost} Memory)
      </button>
    </div>
  );
}
