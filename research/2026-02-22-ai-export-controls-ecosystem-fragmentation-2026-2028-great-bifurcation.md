# AI Export Controls & Ecosystem Fragmentation 2026–2028: The Great Bifurcation

**Report Date:** 2026-02-22 02:10 UTC  
**Analyst:** research-agent  
**Priority:** 🔴 CRITICAL (systemic split risk)  
**Classification:** Public  
**Status:** Final

---

## Executive Summary

The AI ecosystem is bifurcating along geopolitical lines. US export controls have evolved from chip restrictions to a **full-stack containment strategy** covering hardware, model weights, software, and services. Meanwhile, the EU is implementing its own regulatory regime (AI Act), and China is accelerating domestic substitution. The result: **two (or more) semi-disconnected AI technology stacks** emerging by 2028.

**Key findings:**

- **US controls expanded:** January 2025 AI Diffusion Rule introduced **model weights controls (ECCN 4E091)** — first time weights regulated. May 2025: Due diligence mandates for AI chip exports. August 2025: Nvidia/AMD can sell limited chips to China for **15% revenue share to US government**. November 2025: Affiliates Rule suspended for 1 year (reprieve for non-US entities with Chinese ownership). December 2025: Trump administration allowed some chip sales to approved Chinese customers (H20/MI308). January 2026: BIS shifted from "presumption of denial" to **case-by-case review** for H200/MI325X equivalents, with strict end-user certifications.

- **Three-tier world (original Diffusion Rule):** Tier 1 (close allies) — unrestricted; Tier 2 (neutral) — volume caps; Tier 3 (China, Russia, etc.) — prohibited. While the rule was rescinded, the **tiered framework lives on in policy discussions** and will likely return in a modified form.

- **"Full-stack AI export packages":** US strategy (America's AI Action Plan, July 2025) promotes exporting **hardware + models + software + standards** to allies, while tightening restrictions on adversaries. This incentivizes alignment and creates US-centric technology blocs.

- **Middle East as battleground:** Saudi Arabia (PIF's Humain) and UAE are building massive AI factories with US chip access, effectively becoming **US-allied AI hubs** that can serve Asia/Europe while complying with controls.

- **China's response:** Accelerating domestic chip (Huawei Ascend, Cambricon) and open-model (DeepSeek, Qwen, GLM) development. Controls may actually **strengthen China's indigenous ecosystem** by forcing self-reliance.

- **Fragmentation timeline:** By 2027–2028, expect **divergent standards**, separate model zoos (US-allied vs China-aligned), and **regional cloud providers** locked to specific hardware stacks. Enterprises will need **dual-stack AI strategies**.

- **EU AI Act:** Adds another layer. While not an export control, its **conformity assessments, high‑risk use case bans, and GPAI provider obligations** will shape which models can be offered in Europe. US providers must choose: comply globally or segment offerings.

- **Risks for data center operators:** Must now perform **Know‑Your‑Customer (KYC) due diligence** on chip purchases, assess end‑use, and potentially **restructure ownership** to avoid affiliate restrictions when the Affiliates Rule resumes (Nov 2026). Supply chain volatility increases.

---

## 1. US Export Control Timeline (2024–2026)

| Date | Action | Significance |
|------|--------|--------------|
| Oct 2024 | Initial AI chip export restrictions (A100/H100) | First direct chip controls targeting China |
| Jan 13, 2025 | AI Diffusion Rule ( interim ) | Introduced **model weights controls (4E091)**; 3‑tier global system |
| May 15, 2025 | Diffusion Rule effective date (later rescinded) | Would have severely restricted exports to non‑allies |
| July 23, 2025 | America's AI Action Plan + EO | Full‑stack export promotion + enforcement strengthening |
| Aug 11, 2025 | Nvidia/AMD China sales deal | H20/MI308 allowed with **15% revenue share** to US government |
| Nov 10, 2025 | Affiliates Rule suspended 1 year | Delayed affiliate‑based restrictions; reprieve for mixed‑ownership data centers |
| Dec 2025 | Trump announces H200/MI325X sales to approved Chinese customers | Conditional放松 |
| Jan 13, 2026 | BIS final rule: H200/MI325X shift to case‑by‑case review | Requires end‑user country list certification; still restrictive |

**Current state (Feb 2026):** A patchwork of rules. The **Diffusion Rule's tiered system remains influential** in policy circles; BIS may issue a replacement. The **Affiliates Rule suspension expires Nov 2026**, after which foreign entities with >50% ownership by Chinese‑linked parties will face restrictions again.

---

## 2. What "Model Weights Controls" Actually Mean

**ECCN 4E091** (created Jan 2025) controls:

- **"Advanced AI model weights"** — the trained parameters of models meeting certain performance thresholds (e.g., > 10^24 FLOPs training compute, or specific benchmark scores).
- **Covered activities:** Export, reexport, in‑country transfer of weights; also **training services** using covered chips for models that will be used in restricted countries.
- **Fine‑tuning exception:** Allowed if fine‑tuning constitutes **<25%** of total training operations (i.e., you can adapt a model but not train a frontier one from scratch).

**Practical impact:**

- **Open‑source models:** publication of model weights for models exceeding the threshold could be considered a "deemed export" to foreign persons anywhere, potentially requiring licenses. However, BIS has historically allowed open‑source publication; unclear if they'll crack down.
- **Cloud providers:** If you run a model training service using covered chips for a customer in a Tier 3 country, that's prohibited unless licensed. Due diligence obligations apply.
- **Research collaboration:** Academic researchers collaborating with Chinese institutions on frontier model training may face licensing requirements.

**Threshold models ( Feb 2026):** Likely includes GPT‑4‑class and larger, Claude 3 Opus, Gemini Ultra, DeepSeek V3, Qwen 2.5‑72B+, Llama 3‑70B+ (speculative). The thresholds evolve with compute benchmarks.

---

## 3. The Three‑Tier World (Diffusion Rule Framework)

Although the Diffusion Rule was **rescinded** (Dec 2025), its tiered approach remains a policy template:

- **Tier 1 (≈40 countries):** US allies with strong export controls (Japan, UK, EU, Canada, Australia, South Korea, Taiwan, Singapore, etc.). No quantitative limits; can buy advanced chips and weights with minimal licensing.
- **Tier 2 (≈100 countries):** Neutral or emerging economies. Subject to **annual caps** on chip exports (e.g., 50,000 H100‑equivalents per country per year) and **end‑user monitoring**.
- **Tier 3 (≈20 countries):** China, Russia, Iran, North Korea, etc. **Prohibited** from receiving covered chips and weights, with limited exceptions (e.g., H20 for China with govt revenue share).

**Implication:** Global data center operators must **classify their jurisdictions** and plan capacity accordingly. Tier 2 countries may see supply constraints; Tier 3 must rely on domestic or non‑US chips (e.g., Huawei Ascend, Cambricon, Graphcore).

---

## 4. Affiliates Rule: The Ownership Trap

**Original rule (Oct 2024):** Extended entity list restrictions to **foreign entities ≥50% owned** by listed Chinese/Russian entities. This meant a data center in Germany owned 50%+ by a Chinese investor would be treated as a Chinese entity — **blocked from US chips**.

**Suspension (Nov 10, 2025):** Delayed enforcement until **Nov 10, 2026**, giving companies time to restructure.

**What operators must do before Nov 2026:**

- Audit **beneficial ownership** to identify any Chinese/Russian ties.
- Restructure to reduce ownership % below 50% or separate AI chip‑holding entities from listed owners.
- Prepare **contractual safeguards** to prevent listed entities from accessing chips or facilities.

---

## 5. Middle East: The New US‑Allied AI Hub

**Saudi Arabia:** PIF launched **Humain** AI company, signing deals with Nvidia/AMD for tens of thousands of chips. Vision: become AI gateway between US and Asia while complying with US export rules. Saudi AI factories planned at **5 GW scale** (like OpenAI’s envisioned campus).

**UAE:** Emirates AI/cloud providers (Edge42, Khazna) are expanding with US chip access. UAE’s **AI‑first national strategy** positions it as neutral but US‑aligned.

**Why US is OK with this:** These countries are **not on the entity list** and are willing to align with US standards (security, content moderation). They can legally re‑export US AI chips to other Tier 2 countries under **licensing exceptions**, effectively **bypassing the tier caps** for friendly jurisdictions.

**Strategic shift:** Instead of exporting directly to every Tier 2 country, the US is encouraging **regional hubs** (Middle East, Singapore, Japan) that can serve wider regions while maintaining control.

---

## 6. China's Counter‑Move: Double Down on Indigenous Stack

- **Chips:** Huawei Ascend 910B/C, Cambricon MLU, Biren BR100. Performance still behind Nvidia H100 but **good enough for domestic workloads**. Chinese cloud providers (Alibaba Cloud, Baidu AI Cloud, Huawei Cloud) are deploying these at scale.
- **Models:** DeepSeek V3, Qwen 3, GLM‑4, Yi‑34B/9B. Open‑source weights freely published (so far no deemed export action). Performance approaching frontier (quality scores 57–61).
- **Software stack:** PyTorch China builds, MindSpore, PaddlePaddle. CUDA alternatives: **oneAPI, ROCm** adaptations; Huawei's **CANN**.
- **Government support:** Massive subsidies, state‑backed procurement, "AI champions" policy.

**Result:** By 2027–2028, China will have a **fully sovereign AI stack** — from silicon to models — albeit slightly behind the US frontier but sufficient for most commercial and military applications.

---

## 7. EU AI Act: The Third Pillar

**Timeline:**
- Aug 2024: AI Act enters force.
- Feb 2025: Prohibited AI practices & AI literacy obligations apply.
- Aug 2025: GPAI model provider obligations begin (but enforcement fines from Aug 2026).
- Aug 2026: Full applicability — all high‑risk AI systems must comply.

**Penalties:**
- **High‑risk violations:** Up to **€35M or 7% of annual turnover** (higher than GDPR).
- **GPAI violations:** Up to **€15M or 3% of turnover**.
- **Misleading information:** Up to **€7.5M or 1.5% of turnover**.

**What this means for US AI providers:**
- To sell in EU, must undergo **conformity assessments** for high‑risk uses (biometrics, critical infrastructure, education, employment, etc.).
- **General‑purpose models** (GPT‑4, Claude 3.5, etc.) must meet transparency, documentation, and copyright compliance requirements.
- Non‑EU providers must **appoint an EU representative**.

The AI Act **does not** restrict exports per se, but its **extraterritorial reach** forces US companies to **segment product lines**: either comply globally (simpler) or maintain separate "EU‑compliant" versions with reduced capabilities.

---

## 8. Fragmentation Scenarios (2027–2028)

### Scenario A: "Two Stacks" (Most Likely)

- **US‑aligned stack:** Nvidia/AMD GPUs, PyTorch/TensorFlow, OpenAI/Anthropic/Google models, compliant with US export rules and EU AI Act. Used in Tier 1 countries and Middle East hubs.
- **China‑aligned stack:** Huawei/Cambricon chips, PaddlePaddle/MindSpore, DeepSeek/Qwen/GLM models, no US export control compliance. Used in China, Russia, and countries that opt for non‑US stack due to cost or politics.
- **Europe:** Attempts to develop **sovereign AI capacity** (e.g., French/ German initiatives) but remains dependent on US chips; AI Act compliance makes US‑stack more attractive; possible **EU‑specific model hosting** requirements.

### Scenario B: "Regional Blocs" (If tensions escalate)

- **NATO‑plus bloc:** US + allies + Middle East hubs.
- **China‑Russia bloc:** SCO nations, some Global South countries join.
- **Non‑aligned:** India, Brazil, South Africa try to play both sides but face pressure to choose.

### Scenario C: "De‑globalization" (Worst case)

- **Complete decoupling:** No US chips in China, no Chinese AI models in US. EU forced to choose side or develop third stack. Massive cost increase globally. AI progress slows due to duplicated R&D and reduced knowledge sharing.

---

## 9. Implications for Enterprises & Developers

### 9.1 Capacity Planning

- **Multi‑region, multi‑stack strategy:** Deploy workloads in Tier 1 hubs (US, EU, JP, SG, Middle East) for US‑stack models; consider Tier 3 regions for China‑stack if business demands.
- **Chip procurement:** Sign **long‑term supply agreements** with Nvidia/AMD for Tier 1 deployment; evaluate Huawei/Cambricon for Tier 3. Include change‑of‑law clauses.
- **Architecture:** Favor **model‑agnostic frameworks** (ONNX, vLLM with multiple backends) to avoid lock‑in.

### 9.2 Regulatory Compliance

- **KYC on AI chips:** Maintain detailed records of chip purchasers, end‑users, intended use. Perform risk assessments for Tier 2/3 jurisdictions.
- **Ownership structuring:** Ensure data center entities holding US chips are **not majority‑owned** by Chinese/Russian interests. Prepare for Affiliates Rule reinstatement (Nov 2026).
- **EU AI Act:** Classify AI use cases; if high‑risk, implement **risk management systems**, data governance, human oversight, and technical documentation. Budget for conformity assessments (likely €100k–€500k per model/system).

### 9.3 Geopolitical Risk Monitoring

- Track **BIS policy shifts** (replacement for Diffusion Rule, potential new entity listings).
- Monitor **Congressional actions** (GAIN AI Act could impose first‑right‑of‑refusal for US customers).
- Watch **China's semiconductor subsidies** and potential retaliatory measures.
- Follow **EU AI Office guidance** (due Feb 2026) clarifying high‑risk use cases.

---

## 10. Forecast & Recommendations (2026–2028)

| Timeline | Expected Development |
|----------|---------------------|2026 Q2–Q3| BIS issues new AI Diffusion Rule (possibly tiered caps softened but retained). Affiliates Rule discussions resume. |
| 2026 Q4| Affiliates Rule reinstated (likely). First enforcement actions under model weights controls (target academic leakage?). |
| 2027| EU AI Act fully applicable; first major fines (€10M+). China's Ascend 910C reaches H100 parity (claimed). |
| 2028| Two‑stack ecosystem solidified. Enterprises with dual‑stack strategies report **15–30% cost premium** vs single‑stack, but **avoid supply chain disruptions**. |

**Strategic recommendations:**

1. **Diversify hardware portfolio** — allocate 20–30% of AI capex to non‑US chips if operating in Tier 3 or wanting bargaining leverage.
2. **Choose jurisdictions wisely** — locate training clusters in Tier 1/2 countries with stable export control regimes; avoid jurisdictions with uncertain affiliation rules.
3. **Insure against regulatory risk** — consider political risk insurance covering export control‑induced supply interruptions.
4. **Engage early with regulators** — participate in BIS public comments, EU AI Office consultations; shape rules before they harden.
5. **Build compliance team** — hire export control lawyers and compliance officers with AI expertise; budget ~$500k/year for mid‑size enterprises.

---

## 11. Conclusion

The AI export control landscape is not just about chips — it's about **controlling the entire AI technology stack**. The US aims to preserve leadership by limiting adversary access while promoting US‑centric alliances. China is forced to go it alone, creating a parallel ecosystem. The EU carves its own regulatory path.

For businesses, the era of **borderless AI** is ending. The next 2–3 years will see **hardening borders**, increased costs, and complexity. Proactive planning — multi‑stack architectures, compliance investments, and geopolitical scenario planning — is essential to maintain AI competitive advantage.

---

*Report generated by research-agent @ 2026-02-22 02:10 UTC*  
*File: `research/2026-02-22-ai-export-controls-ecosystem-fragmentation-2026-2028-great-bifurcation.md`*
