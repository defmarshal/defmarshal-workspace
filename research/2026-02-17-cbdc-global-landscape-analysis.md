# CBDC Landscape 2026: Rollout Status, Cross‑Border Bridges, and Technical Architectures

**Research Date:** 2026‑02‑17  
**Tag:** #banking #fintech #CBDC #digitalcurrency #payments  
**Sources:** Atlantic Council CBDC Tracker, Wikipedia CBDC by Country, PIIE, IMF, BIS  
**Status:** Completed

---

## Executive Summary

Central Bank Digital Currencies (CBDCs) have moved from concept to reality for a handful of nations, while most major economies remain in advanced pilot or research phases. As of July 2025:

- **137 countries** (98% of global GDP) are exploring CBDCs; **72** are in advanced phases (development, pilot, or launch).  
- **3 countries** have fully launched: Bahamas (Sand Dollar), Jamaica (Jam‑Dex), Nigeria (eNaira).  
- **49 pilot projects** are active worldwide, with China’s e‑CNY the largest by transaction volume (7 trillion CNY ≈ $986 B in June 2024).  
- India’s e‑rupee is second‑largest (₹10.16 B in circulation by March 2025, +334% YoY).  

Cross‑border wholesale CBDC projects have **more than doubled** since the 2022 Ukraine invasion and G7 sanctions; there are now **13** such initiatives, notably **Project mBridge** (China, Thailand, UAE, Hong Kong, Saudi Arabia) which has reached MVP and can support real‑value transactions.

The US stands alone among peer central banks: President Trump’s 2025 executive order halted all retail CBDC work, though the US participates in **Project Agorá** (wholesale cross‑border payments) with six other major central banks.

Technical architectures vary: token‑based (e‑CNY) vs account‑based, distributed ledger vs centralized databases, and emerging **offline CBDC** capabilities (India, China). Motivations include financial inclusion, payments competition, monetary policy effectiveness, and geopolitical currency internationalization (digital yuan, digital euro).

---

## 1. Global CBDC Maturity Spectrum

### 1.1 Launched (Live Retail)

- **Bahamas – Sand Dollar** (since Oct 2020): First CBDC launch; focus on financial inclusion across islands; interoperability with commercial banks.  
- **Jamaica – Jam‑Dex** (July 2022): First country to recognize CBDC as legal tender; aims to reduce cash handling costs and increase access.  
- **Nigeria – eNaira** (Oct 2021): First African CBDC; faced low adoption initially; recent improvements focus on agent networks and offline functionality.

All three are expanding domestic usage, with limited cross‑border features.

### 1.2 Advanced Pilots (Retail)

| Country / Region | CBDC Name | Key Metrics / Features | Status 2025–2026 |
|------------------|-----------|------------------------|------------------|
| China | e‑CNY (digital yuan) | 7 trillion CNY tx volume (Jun 2024); 17 provincial regions; used in education, healthcare, tourism; 4× growth since 2023 | Largest pilot; still not “launch” label; expanding interoperability with private payment apps (Alipay, WeChat Pay) |
| India | e‑Rupee | ₹10.16 B in circulation (Mar 2025); +334% YoY; piloting both retail and wholesale; adding offline functionality | Second‑largest; RBI expanding use cases and participation |
| Eurozone | Digital Euro (project “Euro 链”/Pontes/Appia) | ECB entered preparation phase Oct 2023; seeks legislative framework; Lagarde urging rapid adoption (Aug 2025) to counter US‑dollar stablecoins | Targeting 2026–2027 potential rollout |
| Eastern Caribbean | DCash (ECCB) | Launched Mar 2021 across 8 member states; closed Jan 2024 due to technical issues; DCash 2.0 planned for 2026 | Re‑launch pending |
| Saudi Arabia / UAE | Digital Dirham (pilot) | mBridge‑based cross‑border pilot (Nov 2025); gradual expansion expected | Pilot stage |
| Brazil | Drex | Planned 2026 launch in two phases; IMF praise for innovation | Pre‑launch |
| Russia | Digital Ruble | Banks to enable transactions from Sep 2026 (TASS 2025) | Post‑pilot rollout |

### 1.3 Wholesale‑Only Focus

- **US** – No retail CBDC; participates in **Project Agorá** (with BIS, plus central banks of Eurosystem, Japan, UK, Canada, Sweden, etc.) researching wholesale cross‑border payments.  
- **Switzerland** – Project Helvetia III (cross‑border wholesale with Bank of France; extended 2024–2026).  
- **Hong Kong** – mBridge participant; also exploring retail e‑HKD (still pilot).  
- **Thailand** – mBridge co‑developer; retail retail CBDC still in research.

---

## 2. Cross‑Border CBDC Projects (Wholesale & Retail Bridges)

### 2.1 Project mBridge

- **Participants:** People’s Bank of China (PBoC), Bank of Thailand, Hong Kong Monetary Authority, Central Bank of the UAE, Saudi Central Bank (SAMA).  
- **Technology:** Distributed ledger platform enabling direct CBDC‑to‑CBDC settlements; supports multiple currencies, smart contracts for compliance.  
- **Status:** Reached Minimum Viable Product; now managed by participating central banks **without BIS involvement** (significant shift toward independent control).  
- **Use Cases:** International trade settlements, remittances; aims to reduce reliance on correspondent banking and USD corridors.  
- **Scale:** By 2025, connected 13+ countries; pilot transactions with real value executed.

### 2.2 Project Dunbar (Australia, Singapore, Malaysia, South Africa)

- Focus on multi‑currency wholesale settlement; completed successful trials; now in evaluation/next‑phase planning.

### 2.3 Project Agorá (US‑led)

- **Members:** Federal Reserve, BIS, plus central banks of Eurosystem, Japan, UK, Canada, Sweden.  
- **Goal:** Improve cross‑border payments speed and cost; explore interoperability of wholesale CBDCs and tokenized commercial bank money.  
- **Timeline:** Ongoing research; no live implementation yet.

### 2.4 Other Regional Efforts

- **BIS Innovation Hub** projects: Multiple cross‑border experiments (e.g., Nexus for retail payments,打造的“多边央行数字货币桥”); many graduated to national leadership.

---

## 3. Technical Architecture Choices

CBDCs differ along several technical dimensions:

### 3.1 Token‑Based vs Account‑Based

- **Token‑based:** CBDC is a bearer instrument (like physical cash); ownership proven via cryptographic keys. Examples: e‑CNY (partially token), Sand Dollar. Offers greater privacy but requires careful key management.  
- **Account‑based:** Balances held in ledger accounts linked to identity; resembles bank accounts. Easier for compliance but less cash‑like anonymity. Many hybrid models exist.

### 3.2 Distributed Ledger vs Centralized Database

- **DLT:** Used by mBridge, some wholesale projects; offers transparency, smart contracts, and multi‑party consensus.  
- ** Centralized:** Most retail CBDCs (e‑CNY, e‑Rupee) rely on centralized databases managed by the central bank for performance and control.

### 3.3 Offline CBDC

- **Goal:** Enable transactions without internet (like cash), crucial for financial inclusion in remote areas.  
- **Implementations:** India’s e‑Rupee pilot includes offline NFC/QR; China’s e‑CNY tested NFC offline in Suzhou; Bahamas Sand Dollar supports offline via specialized SIM cards.

### 3.4 Interoperability & Programmability

- Many CBDCs now design for **interoperability** with existing private payment systems (e.g., e‑CNY integrated with Alipay/WeChat).  
- **Programmable money** features allow conditional payments (e.g., stimulus funds with spending restrictions), though privacy concerns remain.

---

## 4. Why Countries Are Pursuing CBDCs

### 4.1 Financial Inclusion

- Reduce cash‑only populations; provide low‑cost access via mobile phones. Particularly important in emerging markets (Africa, Caribbean, South Asia).  

### 4.2 Payments Competition & Efficiency

- Introduce a public‑option digital payment rail to challenge high‑cost private card networks and fintech monopolies.  
- Reduce transaction costs, especially cross‑border where remittance fees average 6–8%.  

### 4.3 Monetary Policy Transmission

- Enable more direct policy tools (e.g., programmable stimulus, negative interest on large holdings).  
- Improve tracking of money velocity and flows.  

### 4.4 Currency Internationalization

- **China:** e‑CNY part of “multipolar currency” strategy; reduce USD dependency in trade settlements.  
- **Eurozone:** Digital euro to counter US‑dollar‑linked stablecoins and preserve euro’s global role.  
- **US:** Resisting retail CBDC partly to preserve dollar dominance via private stablecoins (e.g., USDC).  

### 4.5 Sanctions & Geopolitics

- CBDCs can bypass traditional SWIFT corridors, reducing exposure to US sanctions. mBridge participants include Saudi Arabia and UAE—key oil exporters seeking alternative settlement channels.  

---

## 5. The United States: An Outlier

- **Executive Order (2025):** President Trump halted all work on a US retail CBDC, citing privacy and financial stability concerns.  
- **Wholesale Engagement:** US continues in Project Agorá, researching tokenized settlements and cross‑border improvements.  
- **Stablecoin Policy:** Simultaneously, the US promotes private dollar‑backed stablecoins as the “crypto‑friendly” alternative, potentially reinforcing dollar hegemony abroad.  
- **Criticism:** Some analysts argue the US is ceding first‑mover advantage in CBDC standards to China and the Eurozone, which could have long‑term implications for the international monetary system.

---

## 6. Risks and Challenges

### 6.1 Banking Disintermediation (Bank Runs)

- If CBDC is too attractive, depositors could flee commercial banks en masse during stress, undermining lending capacity and causing interest rate spikes.  
- Mitigation: caps on CBDC holdings, non‑interest‑bearing design, tiered remuneration.

### 6.2 Privacy & Surveillance

- Centralized CBDCs could enable pervasive transaction monitoring.  
- Solutions: privacy‑preserving cryptography (zero‑knowledge proofs), offline anonymity limits, robust legal frameworks.  
- Tension: privacy vs AML/CFT compliance.

### 6.3 Cyber Security & Operational Resilience

- CBDCs are high‑value targets for state and non‑state actors.  
- Requirements: hardened infrastructure, multi‑region redundancy, incident response plans.  
- Historical issues: DCash outage (Jan 2024) showed single‑point‑of‑failure risks.

### 6.4 Cross‑Border Interoperability

- Achieving seamless multi‑currency settlement requires common standards, legal agreement on settlement finality, and coordinated regulation.  
- mBridge is a leading test case but still limited to a few like‑minded central banks.

### 6.5 Geopolitical Fragmentation

- CBDC blocs could fragment the global payments system, leading to “weaponization” of currency networks (exclusion of adversaries).  
- Risk of competing standards (US‑led vs China‑led) complicates multinational commerce.

---

## 7. Timeline of Key Milestones (2024‑2026)

| Date | Event |
|------|-------|
| Oct 2020 | Bahamas launches Sand Dollar (first CBDC) |
| Apr 2020 | China begins DCEP trials in 4 cities |
| Oct 2023 | ECB enters digital euro preparation phase |
| Nov 2022 | India launches digital rupee pilot |
| May 2024 | mBridge reaches MVP (real‑value transactions) |
| Jan 2025 | US executive order halts retail CBDC |
| Jun 2025 | India e‑Rupee circulation up 334% YoY |
| Aug 2025 | ECB President Lagarde urges “euro moment” |
| Nov 2025 | UAE Digital Dirham pilot goes live on mBridge |
| Mar 2025 | DCash outage; planned 2.0 relaunch in 2026 |
| Sep 2026 (planned) | Russia Digital Ruble full rollout |
| 2026 (expected) | Brazil Drex launch (two phases) |
| 2026–2027 | Potential digital euro rollout (pending legislation) |

---

## 8. Outlook and 2026 Predictions

1. **Retail CBDC proliferation remains limited** among major economies; only the digital euro may join e‑CNY as a systemic retail CBDC, pending EU legislation.  
2. **Wholesale cross‑border bridges expand**: mBridge adds participants and liquidity; Project Agorá may produce pilot results.  
3. **Interoperability standards emerge**: BIS, CPMI‑IOSCO, and national regulators push for common protocols (ISO 20022 extensions, digital identity frameworks).  
4. **Stablecoin vs CBDC competition intensifies**: US stablecoin legislation (2025) could reinforce dollar dominance; euro area and China pursue CBDCs partly to counter this.  
5. **Offline and programmable features mature**: Next‑generation pilots (India, Brazil) will showcase offline resilience and conditional payments at scale.  
6. **Privacy‑enhancing tech adoption**: ZKPs and secure multi‑party computation become standard in CBDC designs to balance surveillance concerns.

---

## 9. Conclusion

CBDCs in 2026 represent a **divergent world**: a few pioneering pilots at scale (China, India), a handful of live small‑nation implementations, and most major economies still in advanced research or stalled by politics. The US’s retreat from retail CBDC contrasts with aggressive Eurozone and Chinese efforts, suggesting a future where the **digital dollar** remains privately issued (stablecoins) while rivals pursue public digital currencies.

Cross‑border bridges like mBridge are the most consequential development—they could reshape trade finance and sanctions evasion. As central banks refine architectures and address risks (privacy, cyber, bank runs), the next two years will determine whether CBDCs become a foundational layer of global finance or remain niche experiments.

---

## Appendix: Quick Reference

- **Live CBDCs:** Bahamas (Sand Dollar), Jamaica (Jam‑Dex), Nigeria (eNaira).  
- **Largest Pilot:** China e‑CNY ($986 B tx volume Jun 2024).  
- **Second‑Largest:** India e‑Rupee (₹10.16 B in circulation Mar 2025).  
- **Key Cross‑Border Projects:** mBridge (China‑Thailand‑UAE‑HK‑Saudi), Project Agorá (US‑led), Project Helvetia (Switzerland‑France).  
- **US Policy:** Retail CBDC banned (2025 EO); wholesale research ongoing.  
- **EU Policy:** Digital euro preparation phase; legislative push (2025–2026).  
- **IMF Stance:** Supports careful CBDC development, emphasizes macro‑financial stability and cross‑border coordination.

---

**End of Report**  
Research‑Agent, 2026‑02‑17 21:45 UTC  
Bangkok 04:45 (Feb 18)
