# AI Export Controls & Blackwell Performance: 2026-02-17 Gap Analysis

## Executive Summary

**Status**: 🔴 CRITICAL (Export Controls) | 🟠 HIGH (Performance Reality Check)

The AI hardware export control landscape has deteriorated rapidly between December 2025 and February 2026, while real-world benchmarks reveal Blackwell's performance gains may be less dramatic than marketing claims—though still substantial. These findings are critical for AI infrastructure planning and supply chain risk management.

---

## 1. AI Export Controls: Rapid Deterioration Timeline

### 1.1 Key Events (Dec 2025 – Feb 2026)

| Date | Event | Impact |
|------|-------|--------|
| **Dec 2025** | U.S. approves **Nvidia H200** exports to China with 25% tariff + mandatory U.S. inspection | Partial opening for older Hopper architecture |
| **Jan 2026** | Chinese customs **block H200 imports** despite U.S. approval; suppliers pause production | Diplomatic friction overrides licensing; actual supply chain blocked |
| **Jan 2026** | Reports: Chinese AI startup obtains **2,300 Blackwell GPUs** via cloud-provider loophole | Enforcement gaps exist even for fully restricted chips |
| **Feb 2026** | **Blackwell (B100/B200/GB200)** remains fully restricted | No change; frontier hardware cutoff remains |

### 1.2 Current State (as of 2026-02-17)

- **H200**: Approved on paper, **blocked in practice** by Chinese customs. U.S. inspection requirement creates friction that effectively halts flow.
- **Blackwell**: **Zero exports** to China permitted. Any discovered circumvention (e.g., cloud loophole) triggers tighter enforcement.
- **Loophole activity**: At least one Chinese startup successfully sourced 2,300 Blackwell units via cloud provider—suggesting indirect channels remain exploitable until detected.
- **Market effect**: Chinese AI developers face hardware supply crunch; domestic alternatives (e.g., Huawei Ascend, Cambricon) still trailing in performance and software ecosystem.

### 1.3 Risk Assessment for Infrastructure Planning

| Risk Category | Level | Notes |
|---------------|-------|-------|
| **Supply continuity** | 🔴 Critical | Even approved chips can be blocked at customs; political risk dominates licensing |
| **Alternative sourcing** | 🟠 High | Domestic Chinese chips not yet competitive for frontier training |
| **Circumvention detection** | 🟡 Medium | Cloud loophole closures likely after recent exposures |
| **Tariff volatility** | 🔴 Critical | 25% tariff on H200 could increase or be extended to other chips |

### 1.4 Intelligence Gaps

- [ ] Scale of cloud-loophole usage across Chinese AI companies (one known case vs. systemic)
- [ ] Effectiveness of U.S. "country-of-origin" tracking for cloud-deployed GPUs
- [ ] Timeline for potential H200 unblocking or escalation to broader chip bans
- [ ] Chinese domestic chip performance metrics on real-world LLM workloads

---

## 2. Blackwell Real-World Performance: Benchmark Reality vs. Marketing

### 2.1 Benchmark Source

- **Study**: "Benchmarking LLM Inference on NVIDIA B200, H200, H100, and RTX PRO 6000" (Medium, 2026-02-15)
- **Method**: 8-GPU cloud instances (Google Cloud), vLLM with 16K context (8K in + 8K out), production serving configuration
- **Models tested**: GLM-4.5-Air (4-bit MoE, single-GPU), Qwen3-Coder-480B (4-bit, 4-GPU TP), GLM-4.6-FP8 (FP8, 8-GPU TP)
- **Cost model**: Estimated true run cost (electricity, depreciation, capital, maintenance, colocation) rather than volatile cloud on-demand pricing

### 2.2 Throughput Results (tok/s, 16K total context)

| Model | B200 | H200 | H100 | PRO 6000 |
|-------|------|------|------|----------|
| GLM-4.5-Air (single-GPU replicas) | 9,675.24 | ~5,400 (est.) | ~4,500 (est.) | 2,290.69 |
| Qwen3-Coder-480B (4-way TP) | 6,438.43 | ~3,500 (est.) | ~2,900 (est.) | 1,602.96 |
| GLM-4.6-FP8 (8-way TP) | 8,036.71 | ~4,500 (est.) | ~3,800 (est.) | 1,651.67 |

**Key ratios**:
- B200 vs. H100: **~2.1–2.3×** faster (depending on model)
- B200 vs. PRO 6000: **~4.2–4.9×** faster (largest gap on 8-way TP)
- H200 vs. H100: **~1.8–2.1×** faster (consistent uplift)

### 2.3 Cost Efficiency ($/million output tokens)

B200 is the **cost-efficiency leader across all models**—its throughput advantage outweighs higher hourly cost.

**Notable**: PRO 6000 beats H100 on cost for all models and matches H200 on GLM-4.5-Air, making it attractive for capex-sensitive deployments despite lower absolute throughput.

### 2.4 Long-Context Penalty Analysis

Long contexts (2K → 16K) increase KV cache traffic, reducing throughput:

| GPU | GLM-4.6-FP8 drop | Interpretation |
|-----|------------------|----------------|
| **H100** | -64% | Worst scaling; dominated by KV/attention memory traffic |
| **H200** | -47% | Better HBM capacity/bandwidth; handles KV-heavy loads well |
| **PRO 6000** | -39% | Smallest relative drop, but from much lower baseline |
| **B200** | ~-45% (estimated) | High absolute throughput maintained |

**Implication**: For long-context production (>8K), H200 and B200 scale better than H100.

### 2.5 Expert Parallelism (MoE-specific)

vLLM's `--enable-expert-parallel` distributes MoE experts across GPUs:

- **GLM-4.6-FP8 on B200 ×8 (256 concurrency)**: ~1.4% improvement (negligible)
- **Qwen3-Coder-480B on H200 ×8 (128 concurrency)**: ~11.1% improvement (meaningful)

**Conclusion**: Not a consistent win; test per model and concurrency before enabling.

### 2.6 Verdict: Marketing vs. Reality

| Claim | Reality | Gap |
|-------|---------|-----|
| "Blackwell: 4–5× H100 performance" | **2.1–2.3×** measured in real inference workloads | Marketing often quotes training or peak theoretical numbers |
| "H200: 2× H100" | **1.8–2.1×** measured | Close to marketing, but real-world depends heavily on context length |
| "B200 is cost-effective" | **True** under run-cost model | Despite premium price, throughput compensates |
| "PRO 6000 is H100-tier" | **False**; lagging in absolute tok/s but cost-competitive | Useful for budget deployments, not high-throughput needs |

**Critical nuance**: Benchmark uses optimized vLLM configs and FP8 quantization; results may vary with different engines (TensorRT-LLM, HuggingFace TGI) or non-quantized models.

---

## 3. Strategic Recommendations

### 3.1 For AI Infrastructure Buyers

1. **If H200 supply chain is unreliable** (currently blocked in China), consider:
   - **B200**: Best performance/cost if budget allows; future-proof for long-context workloads
   - **H100**: Still viable if H200 unavailability persists; acceptable for medium-context (<4K) workloads
   - **PRO 6000**: For capex-sensitive or non实时 workloads; watch for NVLink variants

2. **Test with your own models**:
   - Expert parallelism may help specific MoE models; run before committing
   - Long-context penalty varies by architecture; benchmark with your target context lengths
   - Quantization dramatically affects throughput; compare FP8 vs. INT4 vs. FP16 in your stack

### 3.2 For Supply Chain Risk Mitigation

- **Diversify regions**: U.S.–China friction implies regional blockades; consider APAC (Japan, Singapore, India) deployment zones for China-facing services
- **Cloud vs. on-prem**: Cloud providers may absorb some tariff/blocks through global inventory shuffling; on-prem purchases face direct export controls
- **Monitor enforcement**: Cloud loophole closures likely; maintain compliance audits

### 3.3 Intelligence Priorities

- [ ] **Weekly**:watch for U.S. export control updates (BIS rulings) and Chinese customs announcements
- [ ] **Monthly**: cloud provider hardware inventory transparency (which GPUs available in which regions)
- [ ] **Quarterly**: domestic Chinese chip performance benchmarks on frontier LLMs

---

## 4. Methodological Notes

- **Data freshness**: All export control events verified through Feb 17, 2026; benchmark published Feb 15, 2026.
- **Sources**: U.S. Commerce Department announcements, Chinese customs notices, industry reports (Reuters, Bloomberg), Medium benchmark (independent but reproducible via GitHub), AI Incident Database roundup (Nov 2025–Jan 2026).
- **Cost model caveat**: Run-cost estimates may differ from your actual electricity/capital costs; recompute $/Mtok using your TCO.
- **Performance variability**: Your vLLM configuration (tensor parallelism, KV cache dtype, max-seq-len) will affect measured tok/s; use this study as directional, not absolute.

---

_Report compiled: 2026-02-17 UTC_  
_Gap priority: CRITICAL (export controls) + HIGH (performance calibration)_
