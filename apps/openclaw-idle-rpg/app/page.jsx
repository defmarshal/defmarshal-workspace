'use client';

import { useState, useEffect, useCallback } from 'react';
import AgentCard from './components/AgentCard';
import EventLog from './components/EventLog';

const INITIAL_AGENTS = [
  { id: 'dev', name: 'Dev Agent', baseRate: 1, level: 1, costMultiplier: 1.5 },
  { id: 'content', name: 'Content Agent', baseRate: 0.8, level: 1, costMultiplier: 1.6 },
  { id: 'research', name: 'Research Agent', baseRate: 0.6, level: 1, costMultiplier: 1.7 },
  { id: 'idea-gen', name: 'Idea Generator', baseRate: 0.4, level: 1, costMultiplier: 1.8 },
  { id: 'idea-exec', name: 'Idea Executor', baseRate: 0.5, level: 1, costMultiplier: 1.6 },
];

const RESOURCE_NAMES = {
  memory: 'Memory (MB)',
  cpu: 'CPU Units',
  tokens: 'Tokens',
};

export default function HomePage() {
  const [resources, setResources] = useState({ memory: 0, cpu: 0, tokens: 0 });
  const [agents, setAgents] = useState(INITIAL_AGENTS);
  const [log, setLog] = useState([]);
  const [lastTick, setLastTick] = useState(Date.now());

  // Load saved game on mount
  useEffect(() => {
    const saved = localStorage.getItem('openclaw-idle-rpg-save');
    if (saved) {
      try {
        const data = JSON.parse(saved);
        setResources(data.resources);
        setAgents(data.agents);
        setLog(data.log || []);
      } catch (e) {
        console.error('Save load failed', e);
      }
    }
  }, []);

  // Auto-save every 10 seconds
  useEffect(() => {
    const interval = setInterval(() => {
      const save = { resources, agents, log };
      localStorage.setItem('openclaw-idle-rpg-save', JSON.stringify(save));
    }, 10000);
    return () => clearInterval(interval);
  }, [resources, agents, log]);

  // Production loop: every second, add resources based on agent levels
  useEffect(() => {
    const interval = setInterval(() => {
      setLastTick(Date.now());
      setResources(prev => {
        const newRes = { ...prev };
        agents.forEach(agent => {
          const rate = agent.baseRate * agent.level;
          newRes.memory += rate * 0.5;
          newRes.cpu += rate * 0.3;
          newRes.tokens += rate * 0.2;
        });
        // Round to 2 decimals
        Object.keys(newRes).forEach(k => (newRes[k] = Math.round(newRes[k] * 100) / 100));
        return newRes;
      });
    }, 1000);
    return () => clearInterval(interval);
  }, [agents]);

  const upgradeAgent = useCallback((id) => {
    const agent = agents.find(a => a.id === id);
    if (!agent) return;
    const cost = Math.floor(10 * Math.pow(agent.costMultiplier, agent.level));
    if (resources.memory < cost) {
      addLog(`Not enough Memory to upgrade ${agent.name} (need ${cost})`);
      return;
    }
    // Deduct memory first
    setResources(prev => ({ ...prev, memory: prev.memory - cost }));
    // Then upgrade agent
    setAgents(prev => prev.map(a => a.id === id ? { ...a, level: a.level + 1 } : a));
    addLog(`Upgraded ${agent.name} to level ${agent.level + 1} (cost ${cost})`);
  }, [agents, resources]);

  const addLog = (msg) => {
    setLog(prev => [...prev.slice(-9), `${new Date().toLocaleTimeString()} — ${msg}`]);
  };

  // Random events: every 30 seconds, chance of crisis or boon
  useEffect(() => {
    const interval = setInterval(() => {
      if (Math.random() < 0.3) {
        const roll = Math.random();
        if (roll < 0.5) {
          // Crisis
          const loss = Math.round(resources.memory * 0.1);
          setResources(r => ({ ...r, memory: Math.max(0, r.memory - loss) }));
          addLog(`🚨 Crisis: Memory leak! Lost ${loss} Memory.`);
        } else {
          // Boon
          const gain = Math.round(10 + resources.cpu * 0.1);
          setResources(r => ({ ...r, tokens: r.tokens + gain }));
          addLog(`✨ Boon: Token bonus +${gain}!`);
        }
      }
    }, 30000);
    return () => clearInterval(interval);
  }, [resources]);

  return (
    <div className="min-h-screen p-4">
      <header className="mb-6 text-center">
        <h1 className="text-4xl font-bold text-mewmew-primary">OpenClaw Idle RPG</h1>
        <p className="text-gray-400">Manage agents, gather resources, survive crises!</p>
      </header>

      {/* Resources */}
      <div className="grid grid-cols-3 gap-4 mb-8">
        {Object.entries(RESOURCE_NAMES).map(([key, label]) => (
          <div key={key} className="bg-gray-800 p-4 rounded-lg text-center">
            <div className="text-sm text-gray-400">{label}</div>
            <div className="text-2xl font-bold text-mewmew-accent">{Math.floor(resources[key])}</div>
          </div>
        ))}
      </div>

      {/* Agents */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-8">
        {agents.map(agent => (
          <AgentCard
            key={agent.id}
            agent={agent}
            onUpgrade={upgradeAgent}
            resources={resources.memory}
          />
        ))}
      </div>

      {/* Event Log */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-2">Event Log</h2>
        <EventLog entries={log} />
      </div>

      <footer className="text-center text-gray-500 text-sm">
        <p>Auto-save every 10s. Close anytime; return to resume.</p>
      </footer>
    </div>
  );
}
