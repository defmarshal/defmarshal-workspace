'use client';

import { useState, useEffect, useCallback } from 'react';
import AgentCard from './components/AgentCard';
import EventLog from './components/EventLog';
import TechTree from './components/TechTree';
import Achievements from './components/Achievements';

const INITIAL_AGENTS = [
  { id: 'dev', name: 'Dev Agent', baseRate: 1, level: 1, costMultiplier: 1.5, ability: { id: 'quick-fix', name: 'Quick Fix', cost: { memory: 10, cpu: 0, tokens: 0 }, cooldown: 30000, lastUsed: 0, desc: 'Instantly resolve a crisis.' } },
  { id: 'content', name: 'Content Agent', baseRate: 0.8, level: 1, costMultiplier: 1.6, ability: { id: 'burst-write', name: 'Burst Write', cost: { memory: 0, cpu: 0, tokens: 20 }, cooldown: 45000, lastUsed: 0, desc: '2x all production for 15s.' } },
  { id: 'research', name: 'Research Agent', baseRate: 0.6, level: 1, costMultiplier: 1.7, ability: { id: 'deep-dive', name: 'Deep Dive', cost: { memory: 50, cpu: 0, tokens: 0 }, cooldown: 60000, lastUsed: 0, desc: '5x Token production for 10s.' } },
  { id: 'idea-gen', name: 'Idea Generator', baseRate: 0.4, level: 1, costMultiplier: 1.8, ability: { id: 'eureka', name: 'Eureka', cost: { memory: 0, cpu: 100, tokens: 0 }, cooldown: 90000, lastUsed: 0, desc: 'Instant +10 Ideas count (todo).' } },
  { id: 'idea-exec', name: 'Idea Executor', baseRate: 0.5, level: 1, costMultiplier: 1.6, ability: { id: 'overclock', name: 'Overclock', cost: { memory: 0, cpu: 0, tokens: 100 }, cooldown: 120000, lastUsed: 0, desc: 'Execute 3 ideas instantly (todo).' } },
];

const RESOURCE_NAMES = {
  memory: 'Memory (MB)',
  cpu: 'CPU Units',
  tokens: 'Tokens',
};

const TECHNICAL_UPGRADES = [
  { id: 'better-servers', name: 'Better Servers', cost: { memory: 100 }, effect: 'productionMultiply', attribute: null, value: 1.2, desc: '+20% all production' },
  { id: 'auto-upgrades', name: 'Auto Upgrades', cost: { memory: 250 }, effect: 'autoUpgrade', value: true, desc: 'Agents auto-upgrade when affordable' },
  { id: 'llm-optimization', name: 'LLM Optimization', cost: { memory: 300, tokens: 50 }, effect: 'productionMultiply', attribute: 'tokens', value: 1.5, desc: '+50% Token production' },
  { id: 'parallel-agents', name: 'Parallel Agents', cost: { memory: 500 }, effect: 'addAgentSlot', value: 1, desc: '+1 agent slot' },
  { id: 'ai-coach', name: 'AI Coach', cost: { memory: 800 }, effect: 'crisisReduction', value: 0.5, desc: '-50% crisis frequency' },
  { id: 'infinite-tokens', name: 'Infinite Tokens', cost: { memory: 2000, cpu: 200 }, effect: 'productionMultiply', attribute: 'tokens', value: 2, desc: '2x Token production' },
];

const ACHIEVEMENTS = [
  { id: 'first-upgrade', name: 'First Upgrade', desc: 'Upgrade any agent to level 2', condition: (s) => s.agents.some(a => a.level > 1) },
  { id: 'memory-1000', name: 'Gigabyte', desc: 'Reach 1000 Memory', condition: (s) => s.resources.memory >= 1000 },
  { id: 'cpu-500', name: 'Half Kilocore', desc: 'Reach 500 CPU', condition: (s) => s.resources.cpu >= 500 },
  { id: 'tokens-1000', name: 'Token Hoarder', desc: 'Reach 1000 Tokens', condition: (s) => s.resources.tokens >= 1000 },
  { id: 'level-10', name: 'Senior Agent', desc: 'Have an agent at level 10', condition: (s) => s.agents.some(a => a.level >= 10) },
  { id: 'survive-10-crises', name: 'Resilient', desc: 'Survive 10 crises', condition: (s) => s.stats.crisesSurvived >= 10 },
  { id: 'purchase-3-upgrades', name: 'Tech Explorer', desc: 'Purchase 3 tech upgrades', condition: (s) => s.techUpgrades.length >= 3 },
];

export default function HomePage() {
  const [resources, setResources] = useState({ memory: 0, cpu: 0, tokens: 0 });
  const [agents, setAgents] = useState(INITIAL_AGENTS);
  const [log, setLog] = useState([]);
  const [lastTick, setLastTick] = useState(Date.now());
  const [activeAbilities, setActiveAbilities] = useState({}); // { [abilityId]: remainingSeconds }
  const [techUpgrades, setTechUpgrades] = useState([]);
  const [achieved, setAchieved] = useState([]);
  const [stats, setStats] = useState({ crisesSurvived: 0, boonsFound: 0, totalUpgrades: 0 });
  const [activeTab, setActiveTab] = useState('agents');

  // Load saved game (versioned)
  useEffect(() => {
    const saved = localStorage.getItem('openclaw-idle-rpg-save');
    if (saved) {
      try {
        const data = JSON.parse(saved);
        if (data.version && data.version >= 2) {
          setResources(data.resources);
          setAgents(data.agents);
          setLog(data.log || []);
          setTechUpgrades(data.techUpgrades || []);
          setAchieved(data.achieved || []);
          setStats(data.stats || { crisesSurvived: 0, boonsFound: 0, totalUpgrades: 0 });
        }
      } catch (e) {
        console.error('Save load failed', e);
      }
    }
  }, []);

  // Auto-save every 10 seconds (version 2)
  useEffect(() => {
    const interval = setInterval(() => {
      const save = { version: 2, resources, agents, log, techUpgrades, achieved, stats };
      localStorage.setItem('openclaw-idle-rpg-save', JSON.stringify(save));
    }, 10000);
    return () => clearInterval(interval);
  }, [resources, agents, log, techUpgrades, achieved, stats]);

  // Compute production multipliers from tech upgrades
  const getProductionMultiplier = useCallback((attr) => {
    let mult = 1;
    techUpgrades.forEach(t => {
      if (t.effect === 'productionMultiply' && (!t.attribute || t.attribute === attr)) {
        mult *= t.value;
      }
    });
    return mult;
  }, [techUpgrades]);

  // Production loop (combined tech + ability multipliers)
  useEffect(() => {
    const interval = setInterval(() => {
      setLastTick(Date.now());
      setResources(prev => {
        const newRes = { ...prev };
        agents.forEach(agent => {
          const base = agent.baseRate * agent.level;
          const memMult = getProductionMultiplier('memory') * (activeAbilities['burst-write'] ? 2 : 1);
          const cpuMult = getProductionMultiplier('cpu') * (activeAbilities['burst-write'] ? 2 : 1);
          const tokenMult = getProductionMultiplier('tokens') * (activeAbilities['burst-write'] ? 2 : 1) * (activeAbilities['deep-dive'] ? 5 : 1);
          newRes.memory += base * 0.5 * memMult;
          newRes.cpu += base * 0.3 * cpuMult;
          newRes.tokens += base * 0.2 * tokenMult;
        });
        Object.keys(newRes).forEach(k => (newRes[k] = Math.round(newRes[k] * 100) / 100);
        return newRes;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [agents, getProductionMultiplier, activeAbilities]);

  // Ability cooldown countdown
  useEffect(() => {
    const tick = setInterval(() => {
      setActiveAbilities(prev => {
        const next = {};
        Object.entries(prev).forEach(([k, sec]) => {
          if (sec > 1) next[k] = sec - 1;
        });
        return next;
      });
    }, 1000);
    return () => clearInterval(tick);
  }, []);

  const upgradeAgent = useCallback((id) => {
    const agent = agents.find(a => a.id === id);
    if (!agent) return;
    const cost = Math.floor(10 * Math.pow(agent.costMultiplier, agent.level));
    if (resources.memory < cost) {
      addLog(`Not enough Memory to upgrade ${agent.name} (need ${cost})`);
      return;
    }
    setResources(prev => ({ ...prev, memory: prev.memory - cost }));
    setAgents(prev => prev.map(a => a.id === id ? { ...a, level: a.level + 1 } : a));
    setStats(s => ({ ...s, totalUpgrades: s.totalUpgrades + 1 }));
    addLog(`Upgraded ${agent.name} to level ${agent.level + 1} (cost ${cost})`);
  }, [agents, resources]);

  const useAbility = useCallback((agentId) => {
    const agent = agents.find(a => a.id === agentId);
    if (!agent || !agent.ability) return;
    const ab = agent.ability;
    const now = Date.now();
    if (ab.lastUsed && now - ab.lastUsed < ab.cooldown) {
      const remaining = Math.round((ab.cooldown - (now - ab.lastUsed)) / 1000);
      addLog(`${agent.name}'s ${ab.name} on cooldown (${remaining}s)`);
      return;
    }
    // Check cost
    if (resources.memory < ab.cost.memory || resources.cpu < ab.cost.cpu || resources.tokens < ab.cost.tokens) {
      addLog(`Not enough resources for ${agent.name}'s ${ab.name}`);
      return;
    }
    // Deduct cost
    setResources(prev => ({
      memory: prev.memory - ab.cost.memory,
      cpu: prev.cpu - ab.cost.cpu,
      tokens: prev.tokens - ab.cost.tokens,
    }));
    // Set cooldown
    setAgents(prev => prev.map(a => a.id === agentId ? { ...a, ability: { ...ab, lastUsed: now } } : a));
    setActiveAbilities(prev => ({ ...prev, [ab.id]: Math.round(ab.cooldown / 1000) }));
    addLog(`${agent.name} used ${ab.name}!`);
  }, [agents, resources]);

  const purchaseTech = useCallback((tech) => {
    if (techUpgrades.includes(tech.id)) {
      addLog(`Already purchased: ${tech.name}`);
      return;
    }
    const c = tech.cost;
    if (resources.memory < c.memory || resources.cpu < c.cpu || resources.tokens < c.tokens) {
      addLog(`Insufficient resources for ${tech.name}`);
      return;
    }
    setResources(prev => ({
      memory: prev.memory - c.memory,
      cpu: prev.cpu - c.cpu,
      tokens: prev.tokens - c.tokens,
    }));
    setTechUpgrades(prev => [...prev, tech.id]);
    addLog(`Purchased tech: ${tech.name}`);
  }, [resources, techUpgrades]);

  // Random events: crises & boons
  useEffect(() => {
    const interval = setInterval(() => {
      const crisisChance = techUpgrades.includes('ai-coach') ? 0.15 : 0.3;
      if (Math.random() < crisisChance) {
        const roll = Math.random();
        if (roll < 0.5) {
          // Crisis: Memory leak
          const loss = Math.max(1, Math.round(resources.memory * 0.1));
          setResources(r => ({ ...r, memory: Math.max(0, r.memory - loss) }));
          setStats(s => ({ ...s, crisesSurvived: s.crisesSurvived + 1 }));
          addLog(`🚨 Crisis: Memory leak! Lost ${loss} Memory.`);
        } else {
          // Boon: Token bonus
          const gain = Math.round(10 + resources.cpu * 0.1);
          setResources(r => ({ ...r, tokens: r.tokens + gain }));
          setStats(s => ({ ...s, boonsFound: s.boonsFound + 1 }));
          addLog(`✨ Boon: Token bonus +${gain}!`);
        }
      }
    }, 30000);
    return () => clearInterval(interval);
  }, [resources, techUpgrades]);

  // Check achievements
  useEffect(() => {
    ACHIEVEMENTS.forEach(a => {
      if (!achieved.includes(a.id) && a.condition({ resources, agents, techUpgrades, stats })) {
        setAchieved(prev => [...prev, a.id]);
        if (a.reward) {
          setResources(prev => ({ ...prev, ...a.reward }));
          addLog(`🏆 Achievement: ${a.name} — rewarded ${Object.entries(a.reward).map(([k,v]) => `${v} ${RESOURCE_NAMES[k]}`).join(', ')}`);
        } else {
          addLog(`🏆 Achievement: ${a.name}`);
        }
      }
    });
  }, [resources, agents, techUpgrades, stats, achieved]);

  // Auto-upgrade tech effect
  useEffect(() => {
    if (techUpgrades.includes('auto-upgrades')) {
      const interval = setInterval(() => {
        setResources(prev => {
          let anyUpgrade = false;
          const newAgents = agents.map(agent => {
            const cost = Math.floor(10 * Math.pow(agent.costMultiplier, agent.level));
            if (prev.memory >= cost) {
              anyUpgrade = true;
              return { ...agent, level: agent.level + 1 };
            }
            return agent;
          });
          if (anyUpgrade) {
            setAgents(newAgents);
            setStats(s => ({ ...s, totalUpgrades: s.totalUpgrades + 1 }));
            addLog('Auto-upgrade triggered!');
          }
          return prev;
        });
      }, 5000);
      return () => clearInterval(interval);
    }
  }, [techUpgrades, agents]);

  const addLog = (msg) => {
    setLog(prev => [...prev.slice(-9), `${new Date().toLocaleTimeString()} — ${msg}`]);
  };

  return (
    <div className="min-h-screen p-4 bg-gray-900 text-gray-100">
      <header className="mb-6 text-center">
        <h1 className="text-4xl font-bold text-indigo-400">OpenClaw Idle RPG</h1>
        <p className="text-gray-400">Manage agents, gather resources, survive crises!</p>
      </header>

      {/* Resources */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {Object.entries(RESOURCE_NAMES).map(([key, label]) => (
          <div key={key} className="bg-gray-800 p-4 rounded-lg text-center border border-gray-700">
            <div className="text-sm text-gray-400">{label}</div>
            <div className="text-2xl font-bold text-indigo-300">{Math.floor(resources[key])}</div>
          </div>
        ))}
      </div>

      {/* Tabs */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-2">
          <button onClick={() => setActiveTab('agents')} className={`px-4 py-2 rounded ${activeTab === 'agents' ? 'bg-indigo-700' : 'bg-gray-700'}`}>Agents</button>
          <button onClick={() => setActiveTab('tech')} className={`px-4 py-2 rounded ${activeTab === 'tech' ? 'bg-indigo-700' : 'bg-gray-700'}`}>Tech Tree</button>
          <button onClick={() => setActiveTab('achievements')} className={`px-4 py-2 rounded ${activeTab === 'achievements' ? 'bg-indigo-700' : 'bg-gray-700'}`}>Achievements</button>
        </div>
      </div>

      {/* Tab content */}
      {activeTab === 'agents' && (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {agents.map(agent => (
            <AgentCard
              key={agent.id}
              agent={agent}
              onUpgrade={upgradeAgent}
              resources={resources.memory}
              onUseAbility={() => useAbility(agent.id)}
              abilityCooldown={activeAbilities[agent.ability?.id] ? activeAbilities[agent.ability.id] * 1000 : 0}
            />
          ))}
        </div>
      )}

      {activeTab === 'tech' && (
        <TechTree upgrades={techUpgrades} onPurchase={purchaseTech} upgradesList={TECHNICAL_UPGRADES} />
      )}

      {activeTab === 'achievements' && (
        <Achievements achieved={achieved} achievementsList={ACHIEVEMENTS} />
      )}

      {/* Event Log */}
      <div className="mt-8 mb-8">
        <h2 className="text-xl font-semibold mb-2">Event Log</h2>
        <EventLog entries={log} />
      </div>

      <footer className="text-center text-gray-500 text-sm">
        <p>Auto-save every 10s. Close anytime; return to resume.</p>
      </footer>
    </div>
  );
}
