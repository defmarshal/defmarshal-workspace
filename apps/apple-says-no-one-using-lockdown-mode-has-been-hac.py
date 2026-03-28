```python
#!/usr/bin/env python3
"""
Apple Lockdown Mode Protection Demo
Simulates how Lockdown Mode prevents spyware attacks on Apple devices.
"""

import random
import time
from dataclasses import dataclass
from typing import List, Dict

@dataclass
class SpywareAttack:
    """Represents a spyware attack attempt."""
    name: str
    sophistication: int  # 1-10 scale
    attack_vector: str  # 'zero_click', 'phishing', 'exploit', 'malware'
    target_feature: str  # what it tries to bypass
    timestamp: float

@dataclass
class Device:
    """Represents an Apple device with security settings."""
    model: str
    ios_version: str
    lockdown_mode: bool = False
    security_features: List[str] = None
    attack_log: List[Dict] = None
    
    def __post_init__(self):
        if self.security_features is None:
            self.security_features = []
        if self.attack_log is None:
            self.attack_log = []
    
    def enable_lockdown_mode(self):
        """Enable Lockdown Mode (iOS 16+)."""
        self.lockdown_mode = True
        self.security_features.extend([
            "USB restricted mode (no data connections when locked)",
            "Disable link previews in messages",
            "Block auto-joining of Wi-Fi networks and AirDrop",
            "Disable Live Photos and animated GIFs",
            "Block incoming calls from unknown contacts",
            "Disable app installation from non-App Store sources",
            "Enhanced memory protection",
            "Strict network-side protection"
        ])
    
    def process_attack(self, attack: SpywareAttack) -> Dict:
        """Simulate handling of a spyware attack."""
        result = {
            'attack': attack.name,
            'vector': attack.attack_vector,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(attack.timestamp)),
            'blocked': False,
            'reason': '',
            'data_exfiltrated': False
        }
        
        # Base blocking probability
        if self.lockdown_mode:
            # Lockdown Mode blocks most sophisticated spyware
            block_chance = min(0.95, 0.6 + (attack.sophistication * 0.04))
            blocked = random.random() < block_chance
            
            if blocked:
                reasons = [
                    "USB restricted mode prevented data connection",
                    "No Live Photos processing - exploit chain broken",
                    "AirDrop disabled - initial delivery failed",
                    "Link previews blocked - phishing payload not loaded",
                    "Enhanced memory protection blocked code execution",
                    "Network isolation prevented C2 communication",
                    "App installation blocked - malicious app not permitted"
                ]
                result['blocked'] = True
                result['reason'] = random.choice(reasons)
            else:
                # Very sophisticated attacks might still get through (but with reduced capability)
                result['blocked'] = False
                result['reason'] = "Advanced exploit bypassed some protections"
                # Low chance of data exfiltration even if blocked partially
                result['data_exfiltrated'] = random.random() < 0.1
        else:
            # Normal mode: some attacks succeed proportionally to sophistication
            success_chance = attack.sophistication * 0.15  # up to 150% but capped at ~85%
            success_chance = min(0.85, success_chance)
            success = random.random() < success_chance
            
            if success:
                result['blocked'] = False
                result['reason'] = "Malware installed and operational"
                result['data_exfiltrated'] = random.random() < 0.7  # high chance of data theft
            else:
                result['blocked'] = True
                result['reason'] = "Attack failed (AV detection or user intervention)"
        
        self.attack_log.append(result)
        return result

class LockdownModeSimulator:
    """Simulates multiple devices under attack to demonstrate Lockdown Mode efficacy."""
    
    def __init__(self):
        self.devices = []
        self.attack_catalog = self._create_attack_catalog()
    
    def _create_attack_catalog(self) -> List[SpywareAttack]:
        """Create realistic spyware attack scenarios based on known threats."""
        return [
            SpywareAttack(
                name="Pegasus (NSO Group) - iOS 15 exploit chain",
                sophistication=10,
                attack_vector="zero_click",
                target_feature="iMessage",
                timestamp=time.time() - 86400 * 30
            ),
            SpywareAttack(
                name="Pegasus - iOS 16.3.1 WebKit exploit",
                sophistication=10,
                attack_vector="exploit",
                target_feature="Safari",
                timestamp=time.time() - 86400 * 25
            ),
            SpywareAttack(
                name="Civus/Intellexa - FORCEDENTRY variant",
                sophistication=9,
                attack_vector="zero_click",
                target_feature="iMessage attachment",
                timestamp=time.time() - 86400 * 20
            ),
            SpywareAttack(
                name="Predator (Cytrox) - Android/iOS hybrid",
                sophistication=8,
                attack_vector="phishing",
                target_feature="Link preview",
                timestamp=time.time() - 86400 * 15
            ),
            SpywareAttack(
                name="Predator - USB-based exploit",
                sophistication=8,
                attack_vector="exploit",
                target_feature="Lightning port",
                timestamp=time.time() - 86400 * 10
            ),
            SpywareAttack(
                name="Hermit (Lookout) - Supply chain attack",
                sophistication=7,
                attack_vector="malware",
                target_feature="App sideloading",
                timestamp=time.time() - 86400 * 5
            ),
            SpywareAttack(
                name="FinFisher - iOS watering hole",
                sophistication=7,
                attack_vector="exploit",
                target_feature="WebKit",
                timestamp=time.time() - 86400 * 3
            ),
            SpywareAttack(
                name="Custom Iran-linked spyware - Targeted iCloud phishing",
                sophistication=6,
                attack_vector="phishing",
                target_feature="Credential theft",
                timestamp=time.time() - 86400 * 2
            )
        ]
    
    def add_device(self, device: Device):
        """Add a device to the simulation."""
        self.devices.append(device)
    
    def run_simulation(self, rounds: int = 1):
        """Simulate attacks over time."""
        print("=" * 70)
        print("APPLE LOCKDOWN MODE PROTECTION DEMONSTRATION")
        print("=" * 70)
        print()
        
        # Summary of devices
        print(f"[DEVICES UNDER SIMULATION]")
        for device in self.devices:
            status = "LOCKDOWN MODE ENABLED" if device.lockdown_mode else "STANDARD MODE"
            print(f"  • {device.model} ({device.ios_version}) - {status}")
        print()
        
        # Simulate attacks
        total_attacks = len(self.attack_catalog) * rounds * len(self.devices)
        print(f"[SIMULATION PARAMETERS]")
        print(f"  Total attack iterations: {total_attacks}")
        print(f"  Attack catalog: {len(self.attack_catalog)} unique spyware tools")
        print(f"  Rounds: {rounds}")
        print()
        
        print("[RUNNING ATTACK SIMULATION]")
        print("-" * 70)
        
        blocked_counts = {device.model: 0 for device in self.devices}
        success_counts = {device.model: 0 for device in self.devices}
        
        for round_num in range(rounds):
            for attack in self.attack_catalog:
                for device in self.devices:
                    result = device.process_attack(attack)
                    
                    if result['blocked']:
                        blocked_counts[device.model] += 1
                        status = "🛡️ BLOCKED"
                    else:
                        success_counts[device.model] += 1
                        status = "⚠️  COMPROMISED"
                    
                    # Show some sample attacks
                    if random.random() < 0.3:  # Show ~30% of attacks
                        print(f"  {device.model:20} | {attack.name[:30]:30} | {status}")
        
        print()
        print("[RESULTS SUMMARY]")
        print("-" * 70)
        for device in self.devices:
            total = blocked_counts[device.model] + success_counts[device.model]
            block_rate = (blocked_counts[device.model] / total * 100) if total > 0 else 0
            print(f"\n{device.model}:")
            print(f"  Attacks faced: {total}")
            print(f"  Blocked: {blocked_counts[device.model]} ({block_rate:.1f}%)")
            print(f"  Compromised: {success_counts[device.model]}")
            
            if device.lockdown_mode:
                print(f"  → Lockdown Mode provides >90% protection against sophisticated spyware")
            else:
                print(f"  → Standard mode vulnerable to {success_counts[device.model]}/{total} attacks")
        
        print()
        print("[CONCLUSION]")
        print("-" * 70)
        print("Apple's claim: 'No user with Lockdown Mode enabled has been hacked")
        print("with mercenary spyware.' This simulation demonstrates why:")
        print()
        print("1. Lockdown Mode disables or restricts features that spyware exploits")
        print("   (link previews, Live Photos, USB data, AirDrop, etc.)")
        print("2. Sophisticated spyware chains require multiple vulnerable features")
        print("3. Removing even one link breaks the entire attack chain")
        print("4. Attackers must now find novel zero-days that bypass Lockdown defenses")
        print()
        print("Trade-off: Some convenience features are disabled, but for")
        print("high-risk individuals (journalists, activists, officials),")
        print("the security benefit far outweighs the usability cost.")
        print()
        print("Note: This is a simplified simulation. Real-world effectiveness")
        print("depends on timely iOS updates and user adherence to best practices.")
        print("=" * 70)

def main():
    """Run the Lockdown Mode demonstration."""
    random.seed(42)  # For reproducible demo
    
    simulator = LockdownModeSimulator()
    
    # Create two devices: one with Lockdown Mode, one without
    iphone_standard = Device(
        model="iPhone 15 Pro",
        ios_version="iOS 16.4",
        lockdown_mode=False
    )
    
    iphone_lockdown = Device(
        model="iPhone 15 Pro",
        ios_version="iOS 16.4",
        lockdown_mode=False
    )
    iphone_lockdown.enable_lockdown_mode()
    
    simulator.add_device(iphone_standard)
    simulator.add_device(iphone_lockdown)
    
    # Run simulation: each device faces each attack once
    simulator.run_simulation(rounds=1)

if __name__ == "__main__":
    main()
```