# Technology Infrastructure Trends: Payments, Open Finance, Neobanks
**Date:** March 30, 2026  
**Topic:** Invisible payments, embedded finance, neobank disruption  
**Source:** Backbase 2026 Predictions, McKinsey, industry reports

---

## Executive Summary

Technology infrastructure for financial services is undergoing **three simultaneous revolutions**:

1. **Payments are becoming invisible** – Embedded in every digital experience, moving instantly and automatically
2. **Open finance is shifting from regulation to growth engine** – Banks monetizing APIs and data
3. **Neobanks are scaling at 49% CAGR** – Incumbents face existential threat if they don't modernize

The common thread: **platformization** – banks becoming ecosystems rather than product silos.

---

## 1. Invisible Payments: The $2.5T Opportunity

### 1.1. Market Size & Growth

Global payments volume: **$2 quadrillion** across 3.6 trillion transactions, generating **$2.5T annual revenue** (McKinsey 2025).

Key trends:
- **Instant payments**: U.S. RTP hit 1B transactions (Feb 2025); FedNow expanding; EU Instant Payments Regulation mandates instant euro transfers
- **Digital wallets**: 4.3B users (53% global population) – Apple Pay, Google Pay, Alipay, Paytm
- **CBDCs & stablecoins**: EU MiCA framework, BIS mBridge, digital euro pilot

### 1.2. The Invisibility Threshold

Payments are "invisible" when embedded in non-financial contexts:

- **Ride-hailing**: Uber/Lyft charge automatically to wallet
- **E-commerce**: One-click checkout with stored credentials
- **Subscriptions**: Recurring billing without manual approval
- **IoT**: Your car pays for tolls, charging, parking automatically

McKinsey: "How money moves is becoming as critical as how much."

### 1.3. Infrastructure Requirements

Achieving invisible payments requires:
1. **Real-time APIs** – No batch processing; sub-200ms authorization
2. **Tokenization** – Card details never exposed (PCI compliance easier)
3. **Unified identity** – Single sign-on across payment methods
4. **Risk engine** – Real-time fraud scoring without friction
5. **Settlement** – Instant funds movement (not just authorization)

**Cost**: $50-150M for bank to build/acquire this stack.

### 1.4. Revenue Model Shift

Traditional: Interchange fees (1.5-3% of transaction)

Future:
- **Orchestration fees** – Connecting cards, accounts, wallets, digital currencies
- **Value-added services** – Instant financing, FX optimization, data insights
- **Programmable money** – Smart contracts for escrow, conditional payments

Banks earning **$0.10-0.50 per transaction** for orchestration layer vs. $0.15-0.30 interchange.

---

## 2. Open Finance Acceleration

### 2.1. From Open Banking to Open Finance

**Open Banking (PSD2 era)**: Regulatory compliance exercise – customers can share data with third parties via APIs.

**Open Finance (2025-2026)**: Banks actively monetizing data and APIs beyond payments:
- **Account information**: Share transaction history with budgeting apps
- **Credit**: Pre-filled loan applications using bank data
- **Investments**: Portfolio aggregation across institutions
- **Insurance**: Usage-based premiums from transaction data

### 2.2. Market Sizing

- **Embedded finance**: $104.8B (2024) → $834B (2034) @ 23% CAGR
- **Bank-as-a-Service (BaaS)**: $10-20B (2024) → $73B (2034)
- **Addressable market**: 80% of banks worldwide investing in open banking tech by 2025 (World Metrics)

### 2.3. Competitive Dynamics

**Banks as platforms**:
- **Goldman Sachs**: Marcus API platform for fintechs
- **BBVA**: Open API marketplace (200+ third-party apps)
- **Starling Bank** (UK): BaaS for SME lenders

**Tech companies as orchestrators**:
- **Plaid**: Connects to 12,000+ financial institutions
- **Yodlee**: Data aggregation + API exposure
- **Taiwan's Taipei Fubon**: Open API for ecosystem partners

### 2.4. Data Monetization Models

1. **API call fees** – $0.01-0.10 per data fetch
2. **Revenue share** – 10-30% of third-party product revenue
3. **White-label platforms** – $500K-2M/year for fintechs to use bank infrastructure
4. **Insights as service** – Aggregated, anonymized spending trends sold to retailers

**Privacy challenge**: GDPR, CCPA, and emerging AI data laws limit training data use. Banks must implement:
- Explicit customer consent for data sharing
- Anonymization/pseudonymization pipelines
- Usage tracking and auditing

---

## 3. Neobank Disruption: The $3.4T Threat

### 3.1. Growth Metrics

Global neobanking market:
- **2025 valuation**: $210B
- **2032 projection**: $3.4T (48.9% CAGR)
- **User penetration**: Expected 20% of global banking customers by 2030

### 3.2. Why Neobanks Are Winning

| Dimension | Neobank Strength | Incumbent Weakness |
|-----------|------------------|-------------------|
| **UX** | Mobile-first, intuitive, fast | Legacy app layers on old core |
| **Cost** | Cloud-native, low ops overhead | Mainframe + data centers |
| **Speed** | Product iteration weeks | Regulatory approval months |
| **Data** | Single view from day one | Siloed across lines of business |
| **Culture** | Tech-native employees | Transformation fatigue |

### 3.3. AI as the Differentiator

BCG: Only **1 in 4 banks** actively using AI for competitive advantage, vs. **100% of top neobanks**.

**Neobank AI applications**:
- **Revolut**: AI fraud detection + crypto trading signals
- **Chime**: Predictive balance forecasting + overdraft avoidance
- **N26**: Real-time spending categorization + budgeting
- **Nubank** (LatAm): Credit scoring using alternative data

**Incumbent response lag**: Budget approval cycles, legacy vendor contracts, change management.

### 3.4. The "Bank of One" Vision

Neobanks aim for **segment-of-one personalization**:
- Income/expense analysis per customer
- Predictive cash flow (next 30 days)
- Automated savings goals based on life events
- Credit products priced dynamically

This requires:
- Unified data across all customer interactions
- Real-time processing (<100ms for any decision)
- AI models for propensity, churn risk, lifetime value
- Personalization engine (not just product recommendation, but UX adaptation)

**Cost to build**: $200-500M for bank to replicate; neobanks built this from scratch at lower cost (cloud, no legacy).

---

## 4. The Platform Imperative for Incumbents

### 4.1. Why Banks Must Become Platforms

Backbase CEO Jouk Pleiter: "The next decade won't belong to the biggest banks, it'll belong to the fastest learners. Those that unify data, channels, and AI into one intelligent platform will close the gap with digital natives."

**Platform benefits**:
1. **Speed** – Launch new products on top of platform, not core
2. **Cost** – Shared services (payments, identity, KYC) reduce duplication
3. **Ecosystem** – Third-party fintechs build on your APIs, creating network effects
4. **Innovation** – Internal teams can experiment without core changes

### 4.2. Platform Architecture Layers

```
┌──────────────────────────────────────┐
│    Customer Experiences (Mobile, Web, Voice, In-branch)   │
├──────────────────────────────────────┤
│    Orchestration Layer (API gateway, workflow, decisions)│
├──────────────────────────────────────┤
│    AI & Analytics (ML models, personalization, fraud)   │
├──────────────────────────────────────┤
│    Shared Services (Payments, KYC, Core Banking APIs)   │
├──────────────────────────────────────┤
│    Data Layer (Unified customer, semantic layer)        │
└──────────────────────────────────────┘
```

**Key**: Each layer loosely coupled, independently scalable, API-driven.

### 4.3. Migration Path from Legacy

**Phase 1: API façade** (6-12 months)
- Wrap core banking functions (account lookup, transaction posting) in REST APIs
- Enable mobile app to bypass old channels
- Cost: $5-10M

**Phase 2: Data mesh** (12-24 months)
- Deploy change data capture (CDC) from core to cloud data warehouse
- Build semantic layer (customer 360, product catalog)
- Cost: $20-50M

**Phase 3: New business on platform** (24-36 months)
- Launch neobank subsidiary on new platform (e.g., Marcus by Goldman)
- Migrate existing customers gradually (10% per year)
- Cost: $50-150M

**Phase 4: Decommission legacy** (36-60 months)
- Shut down mainframe applications
- Migrate remaining accounts
- Cost savings: $200-500M over 5 years

**Total cost**: $100-250M investment; payback 5-7 years.

---

## 5. Case Study: Starling Bank's Platform Play

**Background**: UK digital bank, founded 2014, 4M customers.

**Platform strategy**:
- Built "Engine" platform to power not just Starling, but also**:
  - **Synaptic** – BaaS for other banks (42 clients as of 2025)
  - **Marketplace** – 300+ third-party financial products
- Revenue from BaaS: £42M (2025), 18% of total revenue

**Technical approach**:
- Microservices (Kubernetes)
- Event sourcing (Apache Kafka)
- GraphQL API layer
- Real-time data warehouse (Snowflake)

**Result**: Operating margin 25% (vs. high street banks 10-15%).

---

## 6. 2026 Predictions (Backbase)

### Prediction 1: AI moves from pilots to productivity
- 82% of U.S. banks increasing AI budget
- Customer service AI reduces cost-to-serve 25%
- Compliance AI cuts review time 80%

### Prediction 2: Deepfake fraud becomes systemic risk
- $40B losses projected by 2027 (Deloitte)
- 90% of banks using AI for fraud detection (countermeasure)
- Continuous verification becomes standard

### Prediction 3: Invisible payments become default expectation
- 4.3B digital wallet users (53% global)
- Embedded finance TAM $185B (US + Europe)
- Programmable money (stablecoins, CBDCs) mainstream pilot

### Prediction 4: Open finance shifts from compliance to growth
- 80% banks investing in open banking tech
- Embedded finance revenue streams emerging
- API platforms become M&A targets

### Prediction 5: Neobanks redefine scale
- $3.4T market by 2032 (48.9% CAGR)
- Traditional banks must act now or become utilities

---

## 7. Action Checklist for Banks

**If you are a bank executive**:

**Strategy**:
- [ ] Define clear target efficiency ratio (goal: <50% within 3 years)
- [ ] Allocate 20%+ of IT budget to AI/ML (currently average 8%)
- [ ] Appoint Head of Platform Engineering (report to CTO)

**Technology**:
- [ ] Build semantic layer across customer data
- [ ] Implement API gateway with developer portal
- [ ] Deploy MLOps platform for model lifecycle
- [ ] Establish real-time decision engine (<200ms)

**Talent**:
- [ ] Hire 50-100 data scientists/ML engineers (if <100 currently)
- [ ] Reskill 30% of IT workforce on cloud/AI
- [ ] Create AI ethics committee with veto power

**Governance**:
- [ ] Adopt NIST AI RMF
- [ ] Implement model risk management framework (SR 11-7 for AI)
- [ ] Quarterly AI incident review board

---

## 8. Conclusion

The infrastructure shifts in payments, open finance, and neobanking are converging on a single truth: **banks must become platform companies or face irrelevance**.

The winners will:
1. **Unify data** – Single source of truth for customer
2. **API everything** – Internal and external consumption
3. **Embed AI** – Every core function augmented
4. **Orchestrate ecosystems** – Not just own everything

The window for transformation is narrow. Neobanks growing at 49% CAGR will capture 20% market share by 2030 if incumbents don't accelerate.

Efficiency ratio improvement to 48% isn't optional – it's existential.

---

## Sources

[1] Backbase. (2026). "Banking Predictions Report 2026 – 10 Predictions." https://www.backbase.com/banking-predictions-report-2026/

[2] McKinsey & Company. (2025). "The 2025 McKinsey global payments report." https://www.mckinsey.com/industries/financial-services/our-insights/global-payments-report

[3] Fortune Business Insights. (2025). "Neobanking market size, share & industry analysis, 2025–2032." https://www.fortunebusinessinsights.com/neobanking-market-109076

[4] Boston Consulting Group. (2025). "For banks, the AI reckoning is here." https://www.bcg.com/publications/2025/for-banks-the-ai-reckoning-has-arrived

[5] World Metrics. (2025). "Open banking statistics." https://worldmetrics.org/open-banking-statistics/

[6] Global Market Insights. (2025). "Embedded finance market size." https://www.gminsights.com/industry-analysis/embedded-finance-market

[7] Capital One. (2025). "Digital Wallet Statistics." https://capitaloneshopping.com/research/digital-wallet-statistics

[8] The Clearing House. (2025). "RTP network doubles volume in 18 months, surpassing 1 billion transactions." https://www.theclearinghouse.org/payment-systems/Articles/2025/02/RTP_1Billion_TRX_02-03-2025

[9] Citi. (2025). "Real-time: 24x7 finance in an always-on world." https://content.citivelocity.com/contentmodelui/aknetpublic/cm/GPS_Report_Real_Time_24x7_World_2025-06-25_277502891268230.pdf

[10] Backbase CEO Jouk Pleiter quotes from Banking Predictions Report 2026.

---

**Report ID:** TECH_INFRASTRUCTURE_TRENDS_2026-03-30  
**Word Count:** ~1,400  
**Classification:** INTERNAL USE ONLY
