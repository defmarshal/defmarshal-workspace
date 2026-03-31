#!/usr/bin/env python3
import random
from collections import defaultdict

class EpidemicEnv:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.infected = [10, 5, 2]  # region A, B, C
        self.susceptible = [90, 95, 98]
        self.recovered = [0, 0, 0]
        self.week = 0
        return tuple(self.infected)
    
    def step(self, actions):
        # actions: allocate 10 medical units across regions
        total = sum(actions)
        if total > 10:
            actions = [int(a * 10 / total) for a in actions]
        
        reward = 0
        for i in range(3):
            spread = 0.1 * self.infected[i] / (sum(self.susceptible) + 1)
            new_inf = int(self.susceptible[i] * spread)
            recover = int(self.infected[i] * 0.3)
            self.susceptible[i] -= new_inf
            self.infected[i] = self.infected[i] + new_inf - recover
            self.recovered[i] += recover
            reward -= (new_inf + self.infected[i] * 0.05)  # minimize infections
        self.week += 1
        done = self.week >= 12
        return tuple(self.infected), reward, done

class QLearningAgent:
    def __init__(self):
        self.q = defaultdict(lambda: defaultdict(float))
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2
    
    def get_state_key(self, state):
        return tuple(min(5, s // 2) for s in state)  # discretize
    
    def choose_action(self, state):
        key = self.get_state_key(state)
        if random.random() < self.epsilon:
            a = [0, 0, 0]
            for _ in range(10):
                a[random.randint(0, 2)] += 1
            return tuple(a)
        if key not in self.q:
            a = [0, 0, 0]
            for _ in range(10):
                a[random.randint(0, 2)] += 1
            return tuple(a)
        return max(self.q[key], key=self.q[key].get)
    
    def learn(self, s, a, r, ns, done):
        sk = self.get_state_key(s)
        nk = self.get_state_key(ns)
        ak = tuple(a)
        old = self.q[sk][ak]
        target = r + (0 if done else self.gamma * max(self.q[nk].values() if self.q[nk] else [0]))
        self.q[sk][ak] = old + self.alpha * (target - old)

def main():
    env = EpidemicEnv()
    agent = QLearningAgent()
    
    for episode in range(200):
        s = env.reset()
        done = False
        while not done:
            a = agent.choose_action(s)
            ns, r, done = env.step(a)
            agent.learn(s, a, r, ns, done)
            s = ns
    
    # Evaluate
    print("Evaluation (10 episodes, no exploration):")
    agent.epsilon = 0
    total_rewards = []
    for _ in range(10):
        s = env.reset()
        done = False
        total_r = 0
        while not done:
            a = agent.choose_action(s)
            s, r, done = env.step(a)
            total_r += r
        total_rewards.append(total_r)
        print(f"  Reward: {total_r:.1f}")
    print(f"Average reward: {sum(total_rewards)/10:.1f} (higher = fewer infections)")
    print("\nLearned policy (state=infected counts -> resource allocation):")
    for s in [(5,3,1), (10,5,2), (1,1,0)]:
        a = agent.choose_action(s)
        print(f"  {s} -> {a}")

if __name__ == "__main__":
    main()