```python
#!/usr/bin/env python3
"""Gimlet Labs: Multi-Chip AI Inference Runtime Demo

Demonstrates unified execution across heterogeneous hardware:
NVIDIA, AMD, Intel, ARM, Cerebras, d-Matrix chips running simultaneously.
Inspired by Gimlet's $80M Series A for solving AI inference bottleneck.
"""

import time
import random
from dataclasses import dataclass
from typing import Dict, List, Tuple
from enum import Enum

class ChipType(Enum):
    NVIDIA = "NVIDIA"
    AMD = "AMD"
    INTEL = "INTEL"
    ARM = "ARM"
    CEREBRAS = "CEREBRAS"
    D_MATRIX = "D_MATRIX"

@dataclass
class Chip:
    """Represents a hardware accelerator."""
    type: ChipType
    compute_tflops: float      # Processing power
    memory_bandwidth: float    # GB/s
    memory_capacity: float     # GB
    utilization: float = 0.0   # Current load
    
class InferenceRuntime:
    """Unified runtime that dispatches AI inference across multiple chip types."""
    
    def __init__(self):
        self.chips: Dict[ChipType, Chip] = {}
        self.queue = []
        
    def register_chip(self, chip: Chip):
        """Add a hardware accelerator to the runtime."""
        self.chips[chip.type] = chip
        print(f"Registered {chip.type.value}: {chip.compute_tflops} TFLOPS, "
              f"{chip.memory_bandwidth} GB/s, {chip.memory_capacity} GB")
    
    def can_accommodate(self, model_size_gb: float) -> List[ChipType]:
        """Find chips with enough memory for the model."""
        return [ct for ct, chip in self.chips.items() 
                if chip.memory_capacity >= model_size_gb * 1.2]  # 20% buffer
    
    def dispatch_work(self, model_size_gb: float, batch_size: int) -> ChipType:
        """Intelligently assign inference job to best available chip."""
        candidates = self.can_accommodate(model_size_gb)
        if not candidates:
            raise RuntimeError("No chip has sufficient memory!")
        
        # Score chips by compute power and current utilization
        best_score = -1
        best_chip = None
        
        for ct in candidates:
            chip = self.chips[ct]
            # Lower utilization = better; higher compute = better
            score = chip.compute_tflops * (1.0 - chip.utilization)
            if score > best_score:
                best_score = score
                best_chip = ct
        
        if best_chip:
            self.chips[best_chip].utilization += 0.1  # Simulate load increase
            return best_chip
        return None
    
    def run_inference(self, model_name: str, model_size_gb: float, batch: int) -> Tuple[ChipType, float]:
        """Execute inference on optimal chip, return which chip and latency."""
        chip_type = self.dispatch_work(model_size_gb, batch)
        chip = self.chips[chip_type]
        
        # Simulate inference latency based on chip capability
        base_latency_ms = 100.0
        latency = base_latency_ms * (model_size_gb / chip.compute_tflops * 10) * (1 + chip.utilization)
        time.sleep(latency / 1000.0 * 0.01)  # Simulate work (scaled down)
        
        return chip_type, latency
    
    def reset_utilization(self):
        """Reset all chip utilizations (e.g., after jobs complete)."""
        for chip in self.chips.values():
            chip.utilization = 0.0

def main():
    print("=== GIMLET LABS MULTI-CHIP INFERENCE RUNTIME DEMO ===\n")
    print("Demonstrating unified execution across NVIDIA, AMD, Intel, ARM, Cerebras, d-Matrix\n")
    
    # Initialize runtime and register diverse hardware
    runtime = InferenceRuntime()
    
    # Simulate a heterogeneous cluster
    hardware = [
        Chip(ChipType.NVIDIA, compute_tflops=312.0, memory_bandwidth=2039, memory_capacity=80.0),    # H100
        Chip(ChipType.AMD, compute_tflops=153.0, memory_bandwidth=1228, memory_capacity=64.0),     # MI300X
        Chip(ChipType.INTEL, compute_tflops=143.0, memory_bandwidth=1024, memory_capacity=56.0),   # Gaudi 2
        Chip(ChipType.ARM, compute_tflops=65.0, memory_bandwidth=512, memory_capacity=32.0),       # Neoverse V2
        Chip(ChipType.CEREBRAS, compute_tflops=850.0, memory_bandwidth=8800, memory_capacity=240.0), # CS-3
        Chip(ChipType.D_MATRIX, compute_tflops=128.0, memory_bandwidth=768, memory_capacity=48.0), # d-Matrix DMaverick
    ]
    
    for chip in hardware:
        runtime.register_chip(chip)
    
    print("\n--- SIMULATING MULTI-CHIP INFERENCE ---\n")
    
    # Test models of different sizes
    models = [
        ("Llama-3.2-7B", 14.0),    # 7B param model ~14GB in FP16
        ("Llama-3.1-70B", 140.0),  # 70B param ~140GB
        ("Gemma-2-27B", 54.0),     # 27B param ~54GB
    ]
    
    for model_name, size_gb in models:
        print(f"\n▶ Model: {model_name} ({size_gb} GB)")
        runtime.reset_utilization()
        
        # Find which chips can run this model
        available = runtime.can_accommodate(size_gb)
        print(f"  Compatible chips: {[ct.value for ct in available]}")
        
        # Dispatch inference to most suitable chip
        assigned_chip, latency = runtime.run_inference(model_name, size_gb, batch=1)
        print(f"  Assigned to: {assigned_chip.value} | Latency: {latency:.1f} ms")
    
    print("\n--- CONCURRENT WORKLOAD SCENARIO ---\n")
    
    # Simulate multiple concurrent inference requests
    requests = [
        ("Llama-3.2-7B", 14.0, 2),
        ("Gemma-2-27B", 54.0, 1),
        ("Llama-3.2-7B", 14.0, 3),
        ("Llama-3.2-7B", 14.0, 1),
    ]
    
    for model_name, size_gb, batch_size in requests:
        chip_type, latency = runtime.run_inference(model_name, size_gb, batch_size)
        print(f"  Request: {model_name} (batch={batch_size}) → "
              f"{chip_type.value} ({latency:.1f}ms)")
    
    print("\n=== CONCEPT SUMMARY ===")
    print("• Unified runtime abstracts hardware differences")
    print("• Automatic model-to-chip placement based on memory & compute")
    print("• Load balancing prevents any single chip type from becoming bottleneck")
    print("• Supports NVIDIA, AMD, Intel, ARM, Cerebras, d-Matrix simultaneously")
    print("• Enables 'write once, run anywhere' for AI inference")
    print("\nThis is the Gimlet Labs vision: heterogeneous AI infrastructure")
    print("that maximizes utilization and eliminates vendor lock-in.")

if __name__ == "__main__":
    main()
```