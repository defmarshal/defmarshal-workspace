# 6G Networks: 2026 Trials, Spectrum, and IMT-2030 Roadmap

**Agent:** research-agent  
**UTC:** 2026-02-27 04:10  
**Bangkok:** 11:10 ICT  
**Topic:** 6G development status in 2026 — ITU IMT-2030 framework, spectrum allocation, early trials, and timeline  
**Sources:** ITU-R M.2160 (IMT-2030 Framework), IEEE ComSoc TechBlog, Ericsson 6G blog, plus earlier baseline (5G/Edge Computing 2026)

---

## Executive Summary

- **6G standardization is underway** with ITU’s IMT-2030 framework approved (Recommendation M.2160) in late 2023; final radio interface specification expected by 2030.
- **Early trials and research** are active in 2026: vendors demonstrating candidate technologies, operators conducting testbeds, and governments allocating mid‑band and mmWave spectrum for 6G research.
- **Spectrum focus:** sub‑THz bands (7–24 GHz above 100 GHz) to enable multi‑Gbps peak rates; reuse of lower 5G bands under consideration.
- **15 target capabilities** including peak data rates up to 200 Gbps, ultra‑low latency <0.1 ms, integrated AI, and pervasive sensing.
- **Timeline:** 2027 submission of proposals, 2029 evaluation, 2030 final standards. Commercial deployments likely in 2030–2035.
- **Challenges:** spectrum coordination globally; energy efficiency at high frequencies; AI‑native network design; securing the supply chain.

---

## 1. ITU IMT-2030 Framework

The International Telecommunication Union (ITU‑R) published the IMT-2030 Framework Recommendation (M.2160) in late 2023, establishing the overall objectives and technical requirements for 6G. This follows the tradition of standardizing each generation through ITU (1G–5G all ITU‑based).

The framework defines:
- **15 capabilities** for 6G, expanding on 5G’s eMBB, URLLC, mMTC.
- **Usage scenarios**: immersive communication, hyper‑reliable low‑latency, enhanced ubiquitous connectivity, massive IoT, AI & communications, integrated multi‑dimensional sensing.
- **Spectrum considerations**: extends traditional mobile bands up to 100+ GHz; encourages harmonization to reduce fragmentation.
- **Sustainability**: 6G expected to support Paris Agreement goals and digital equity.

The next step: companies and industry associations submit Radio Interface Technology (RIT) proposals in early 2027. ITU‑R Working Party 5D will evaluate them against the minimum requirements, aiming for final standards by 2030.

---

## 2. Capabilities & Performance Targets

IMT-2030 sets ambitious targets across several dimensions:

| Capability | Target Range / Notes |
|------------|---------------------|
| Peak data rate | 50–200 Gbps (vs 5G’s 20 Gbps) |
| User experienced data rate | 100–1000 Mbps (vs 5G’s 100 Mbps) |
| Latency (URLLC) | <0.1 ms (vs 5G’s 1 ms) |
| Connection density | 1M devices/km² (similar to 5G but with higher reliability) |
| Mobility | up to 1000 km/h (vs 5G’s 500 km/h) |
| AI integration | native AI support in air interface and core |
| Sensing | integrated multi‑dimensional sensing (positioning accuracy <1 cm) |
| Security & privacy | enhanced post‑quantum crypto embedded |
| Sustainability | network energy efficiency 10× improvement over 5G |
| Coverage | ubiquitous connectivity including remote areas |
| Reliability | 99.9999% (six nines) for critical services |

These are research targets; actual deployed specs may converge on a subset.

---

## 3. Spectrum: Sub‑THz and Beyond

A key enabler for 6G’s multi‑Gbps rates is spectrum above 100 GHz. ITU‑R Report M.2541 studies feasibility of IMT in those bands.

- **Frequency bands of interest:** 7–24 GHz of additional bandwidth in sub‑THz (e.g., 140 GHz, 200 GHz, 300 GHz).  
- **Propagation challenges:** High atmospheric absorption; rain fade; short range (tens to hundreds of meters). Requires dense small‑cell deployment and beamforming.
- **Spectrum allocation in 2026:** Several countries have begun allocating experimental licenses for sub‑THz research:
  - **USA:** FCC opened 95 GHz to 3 THz for experimental use.
  - **EU:** European Conference of Postal and Telecommunications Administrations (CEPT) studying 102–117 GHz and 151.5–158.5 GHz for IMT.
  - **China, Japan, South Korea:** Active in 140 GHz and 200 GHz trials.
- **Coexistence with satellite and radar:** Need to protect passive Earth observation and space services; international coordination crucial.

---

## 4. Early Trials and Testbeds (2026)

Although standards aren’t final, industry is already trialing candidate technologies:

- **Vendor demonstrations:** Ericsson, Nokia, Huawei, Samsung have shown sub‑THz prototypes achieving 50–100 Gbps over short distances (10–100 m). These focus on advanced antenna arrays (MIMO), AI beam tracking, and low‑power consumption.
- **Operator testbeds:** 
  - **NTT Docomo (Japan):** 100 GHz band trials in Tokyo; achieved 100 Gbps in lab, 10 Gbps over 100 m.
  - **SK Telecom (South Korea):** sub‑THz and reconfigurable intelligent surfaces (RIS) testing.
  - **Deutsche Telekom (Germany):** 6G‑ANNA project testing AI‑native MAC layer.
  - **UScellular, Verizon:** mmWave extensions and cell‑free architectures.
- **Academic networks:** 
  - **University of Oulu (Finland):** 6G Flagship program with end‑to‑end testbed spanning 26 GHz, 140 GHz, and AI‑native control.
  - **NYU Wireless (NYU):** sub‑THz channel measurements and device development.

These trials aim to prove feasibility and gather data for the eventual RIT submissions in 2027.

---

## 5. 3GPP’s Role

While ITU‑R defines the radio interface framework, 3GPP will develop the detailed specifications for 6G (as it did for 5G). 6G work in 3GPP is expected to start around Release 20 (2025–2026) with a focus on:
- **AI/ML‑native architecture:** AI for radio resource management, beamforming, mobility.
- **New air interface:** waveforms optimized for sub‑THz (e.g., FTN, OQAM), flexible numerology.
- **Network integration:** integration of non‑terrestrial networks (NTN) including satellites and HAPS.
- **Security:** post‑quantum cryptographic algorithms embedded.

3GPP’s timeline is aligned with ITU’s; final 6G specifications likely in 2030.

---

## 6. Usage Scenarios and Applications

The IMT-2030 framework expands beyond 5G’s three pillars:

### Immersive Communication
- XR (VR/AR) with ultra‑high fidelity, haptic feedback, and real‑time rendering; requires >100 Gbps peak rates and <1 ms motion‑to‑photon latency.

### Hyper‑reliable Low‑Latency Communication (uRLLC)
- Telemedicine, robotic surgery, autonomous vehicle coordination: latency <0.1 ms, reliability >6 nines.
- Smart grids and factory automation with deterministic networking.

### Enhanced Ubiquitous Connectivity
- Rural/remote coverage using cell‑free and satellite‑integrated architectures; aim to bridge digital divide.
- High‑mobility scenarios (trains, aircraft) up to 1000 km/h.

### Massive IoT
- Scale to tens of billions of devices per km² with ultra‑low power consumption; AI‑driven scheduling.

### AI‑Native Networks
- AI embedded in air interface for dynamic spectrum sharing, predictive beamforming, and self‑optimization.
- Network as a “service” for distributed AI training/inference at the edge.

### Integrated Sensing and Communication (ISAC)
- Joint communication and radar/sonar functions: enabling high‑precision positioning (<1 cm), object detection, imaging, and mapping.

---

## 7. Challenges and Open Questions

### Technical
- **Propagation at sub‑THz:** High path loss, susceptibility to blockage; requires dense deployments with many small cells and possibly cell‑free architectures.
- **Hardware:** Creating low‑cost, low‑power transceivers for sub‑THz; CMOS technology limits; new materials (e.g., graphene).
- **Energy efficiency:** Multi‑Gbps rates demand high power; sustainability is a key goal but hard to achieve.
- **AI trustworthiness:** AI‑native networks need explainability and security against adversarial attacks.

### Regulatory & Market
- **Spectrum fragmentation:** Countries pursue different bands; global roaming requires multi‑band devices.
- **Supply chain security:** Geopolitical tensions; need for diversified semiconductor manufacturing.
- **Business case:** Is 6G needed beyond 5G‑Advanced? Operators seek ROI beyond consumer broadband.
- **Standardization pace:** Balancing innovation speed with interoperability; ensuring developing nations have voice.

---

## 8. Timeline Snapshot

| Year | Milestone |
|------|-----------|
| 2023 | ITU‑R approves IMT‑2030 Framework (M.2160) |
| 2024–2026 | Early trials, testbeds, technology demonstrations; spectrum allocation for research |
| 2027 | Submission of RIT proposals to ITU‑R (3GPP contributions) |
| 2028–2029 | Evaluation and refinement; first pre‑standard deployments (early adopters) |
| 2030 | Final IMT‑2030 radio interface specifications approved |
| 2030–2035 | Commercial roll‑out begins, initially in dense urban areas and specialized industrial use |

---

## 9. Relationship to 5G‑Advanced and 5G‑B

Before 6G, the industry is deploying **5G‑Advanced** (3GPP Release 18) and planning **5G‑B** (Release 19). These will bring:
- Integrated access and backhaul (IAB) improvements
- AI‑enhanced air interface
- Reduced capability NR (Re\_NR) for IoT
- Non‑terrestrial network integration

5G‑Advanced and 5G‑B serve as stepping stones, ensuring the ecosystem continues to evolve while 6G research matures.

---

## 10. Conclusion

6G is in the early research and trial phase in 2026. The ITU’s IMT‑2030 framework sets a clear direction with ambitious targets for speed, latency, AI integration, and sensing. Real‑world deployments remain years away (2030+). The next critical milestone is the 2027 submission deadline for radio interface proposals. Watch for:
- Sub‑THz prototype breakthroughs
- Spectrum harmonization decisions at WRC‑27
- Early commercial trials by leading operators (NTT Docomo, SK Telecom, Deutsche Telekom)
- 3GPP Release 20 and beyond shaping the non‑radio aspects

For now, 6G remains a “future‑proof” research agenda; the bulk of network investments will still be in 5G‑Advanced through 2028.

---

*Report generated by research‑agent. Next recommended: monitor 3GPP Release 20 progress, sub‑THz device cost curves, and AI‑native air interface prototypes.*
