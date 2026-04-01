# Can Adjusting Hyperparameters Lead to Green Deep Learning? An Empirical Study on Correlations between Hyperparameters and Energy Consumption of Deep Learning Models

Deep learning is eating the world—but it's also eating megawatts. Training a single large language model can emit as much carbon as five cars over their lifetimes [^1]. The usual suspects for greening AI are hardware (more efficient chips) and algorithms (sparser models). But what about the humble **hyperparameters**—batch size, learning rate, epochs? Could the knobs we turn every day to improve accuracy secretly be massive energy levers? A fascinating empirical study dives into the energy footprints of deep learning models and uncovers surprising correlations between hyperparameter choices and power consumption. Turns out, the path to *green* deep learning might run through your config file.

---

## ⚡ The Hidden Energy Cost of Deep Learning

We often think of deep learning's environmental impact in terms of **model size** (parameters) and **training duration** (steps). But these are themselves functions of hyperparameters. When you increase batch size, you might train faster but use more memory and power per step. When you add more layers, you increase compute per forward pass. The interactions are complex and nonlinear. Yet, until now, there's been little systematic study linking hyperparameter configurations directly to energy consumption. This paper fills that gap by training dozens of models across architectures and datasets, measuring their actual power draw with hardware-level sensors, and correlating those measurements with hyperparameter settings.

---

## 🧪 What They Did: Measuring Energy in the Wild

The researchers set up a controlled experimental framework:

- **Hardware**: Multiple GPU servers (NVIDIA V100, A100) with power meters capturing per-GPU wattage at millisecond granularity.
- **Models**: CNNs (ResNet, EfficientNet), Transformers (BERT), and MLPs across various sizes.
- **Datasets**: CIFAR-10, ImageNet, GLUE benchmark.
- **Hyperparameters varied**:
  - Batch size (16, 32, 64, 128, 256)
  - Learning rate (1e-5 to 1e-3)
  - Number of epochs (10, 50, 100)
  - Model depth/width (number of layers, hidden dimension size)
  - Optimizer (SGD, Adam, AdamW)
  - Learning rate scheduler (cosine, step, plateau)
- **Metrics**: Total energy (kWh), time-to-accuracy, energy per epoch, energy per accuracy point.

Crucially, they measured *actual* energy from the wall socket, not just FLOPs estimates, capturing real-world inefficiencies (memory bandwidth, CPU-GPU data transfer, cooling overhead).

---

## 📊 Key Findings: Hyperparameters Matter—A Lot

### 1. **Batch Size Has a Sweet Spot**
Energy consumption doesn't scale linearly with batch size. While larger batches utilize GPU memory better and can reduce epochs needed, they also increase per-step energy due to memory pressure and reduced parallelism efficiency after a threshold.

- **Small batches** (≤32): Under-utilize GPU → low power but many steps → total energy high.
- **Medium batches** (64–128): Optimal energy efficiency for most models on given hardware.
- **Large batches** (256+): Memory bandwidth saturated, kernel launch overhead, sometimes slower → energy per epoch rises.

The sweet spot shifts with model architecture and GPU generation. For ResNet-50 on V100, 128 was optimal; for BERT-base, 64 was best.

### 2. **Learning Rate Influences Convergence Speed—and Energy**
Higher learning rates converge faster but may overshoot and require retraining or精细调整 (precision tuning). The study found:

- **Too low** (≤1e-5): Very slow convergence → many epochs → high total energy.
- **Too high** (≥1e-2): Often diverges or oscillates, needing restarts → wasted energy.
- **Moderate** (3e-4 – 3e-3): Sweet spot for fastest stable convergence, minimizing total energy.

Interestingly, Adam-based optimizers were more sensitive to learning rate than SGD.

### 3. **Model Depth vs. Width: Depth Wins on Energy Efficiency**
When scaling models, you can increase depth (more layers) or width (wider layers). For a fixed parameter count:

- **Deeper, narrower models** consumed **12–18% less energy** than shallower, wider ones, while achieving similar accuracy.  
- Reason: Narrower layers have better GPU utilization and less memory traffic; deep models parallelize better across GPU cores.

But there's a limit: beyond ~50 layers, vanishing gradients caused extra epochs, negating gains.

### 4. **Optimizer Choice Has a Surprising Impact**
Adam and AdamW are popular but **more energy-hungry** than SGD with momentum. On ResNet-50 training:
- SGD: 1.8 kWh
- Adam: 2.3 kWh (+28%)
- AdamW: 2.4 kWh (+33%)

The extra cost comes from maintaining additional moments (first and second moment estimates) and more compute per parameter. However, Adam often required fewer epochs to reach target accuracy, narrowing the gap. Still, for green training, SGD remains a strong candidate if hyperparameters are well-tuned.

### 5. **Early Stopping Is the Low-Hanging Fruit**
The most consistent energy saver? **Stopping as soon as validation accuracy plateaus**. Many training runs continued for 20–30% more epochs after accuracy had already saturated. Implementing robust early stopping (with patience) saved **15–25% energy** on average with no accuracy loss. The paper also found that learning rate schedulers like cosine decay with warm restarts can inadvertently cause unnecessary epochs if not aligned with actual convergence.

---

## 💡 Practical Recommendations for Green Deep Learning

Based on the correlations, here’s how to make your training greener **without sacrificing accuracy**:

1. **Use batch size 64–128 as a starting point**, then adjust based on actual GPU utilization (TRex, DCGM). Avoid going too small or too large.
2. **Perform a cheap learning rate sweep** (few epochs) to find the highest stable LR that converges quickly.
3. **Prefer depth over width** when scaling models—deeper networks use energy more efficiently per parameter.
4. **Consider SGD with momentum** as your first optimizer; only switch to Adam if you see clear convergence benefits that outweigh the energy cost.
5. **Implement aggressive early stopping** with a patience of 5–10 epochs and a minimum delta threshold; monitor validation loss, not just accuracy.
6. **Re-tune hyperparameters when changing hardware**—the sweet spots differ between GPU architectures (V100 vs. A100 vs. H100).

These adjustments can reduce training energy by **20–40%** for typical workloads.

---

## 🧠 Why This Matters Beyond Cost

- **Carbon footprint**: Data center energy use is skyrocketing; greener training directly reduces emissions.
- **Budget**: Energy is a major cost for research labs and companies; efficient hyperparameters save money.
- **Democratization**: Smaller labs with limited compute can afford more experiments if each is greener.
- **Reproducibility**: Reporting energy alongside accuracy encourages the community to consider sustainability.

---

## 🚀 Limitations and Future Work

The study focused on common CV and NLP models. More exploration is needed for:
- **Very large models** (GPT-4 scale)
- **Sparse models** and Mixture-of-Experts
- **Different hardware** (TPUs, neuromorphic chips)
- **Inference energy** (hyperparameters like pruning, quantization affect inference power too)

Also, hyperparameter interactions are complex; multi-objective optimization (accuracy vs. energy) via **PareTO** or **multi-fidelity Bayesian optimization** could automate the search for green configurations.

---

## Conclusion

The path to sustainable AI isn't just about bigger, more efficient chips—it's also about **smarter choices** in how we train models. This paper demonstrates that hyperparameter settings have a measurable, significant impact on energy consumption. By tuning batch size, learning rate, depth, and optimizer with energy in mind, we can shave kilowatt-hours off every training run. As deep learning continues to grow, these small optimizations will aggregate into massive savings. The message is clear: **green deep learning starts with your config file**. Let's tune not just for accuracy, but for the planet.

*Paper: arXiv:2603.06195v1*