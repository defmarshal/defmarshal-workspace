# Fintech 2026: Embedded Finance, BaaS, and the API-ification of Money

*Research Date: 2026-02-28*
*Category: Finance / Technology / Banking*
*Tags: fintech, embedded-finance, BaaS, banking-as-a-service, open-banking, API, payments, BNPL, super-apps, Southeast-Asia, agentic-finance, real-time-payments, CBDC*

---

## Executive Summary

Financial services in 2026 are undergoing structural disaggregation. The "bank" as a monolithic institution that owns the customer relationship, holds deposits, issues credit, and processes payments is being unbundled into composable API layers that any non-financial platform can consume. This shift — variously called embedded finance, Banking-as-a-Service (BaaS), or the API-ification of money — is no longer a startup experiment. The global Fintech-as-a-Service market is valued at **$484.71 billion in 2026**, projected to reach **$1.82 trillion by 2035** (CAGR ~15.7%). Embedded finance revenue alone is on track for **$228.6 billion by 2028** — a 148% jump from ~$92 billion today. In Asia-Pacific, the BaaS market hits **$5.26 billion in 2026** (up from $4.44B in 2025), growing to $12.31 billion by 2031 at 18.55% CAGR.

The defining shift of 2026: embedded finance has moved from *feature* to *ecosystem*. It's no longer about dropping a payment API into an app. It's about orchestrating lending, insurance, savings, payroll, and identity into a composable financial operating system — increasingly piloted by AI agents acting autonomously on behalf of users.

---

## Market Size at a Glance

| Market | 2026 Value | Projected | CAGR |
|--------|-----------|-----------|------|
| Fintech-as-a-Service (global) | **$484.7B** | $1.82T by 2035 | ~15.7% |
| Embedded Finance revenue | **~$92–230B** | $228.6B by 2028 | ~58% 2yr |
| Embedded Finance platform market | — | $570.9B by 2030 | 21.3% |
| Banking-as-a-Service (global) | **$35–45B** | $75–90B by 2030 | 16–18% |
| APAC BaaS | **$5.26B** | $12.31B by 2031 | 18.55% |

*Sources: Precedence Research (Feb 2026), Juniper Research, Allied Market Research, Mordor Intelligence, ResearchNester*

---

## The 14 Fintech Macro-Trends of 2026

### 1. AI Agents & Autonomous Finance

The most disruptive shift: intelligent AI systems are now handling **entire financial workflows autonomously** — decisions, actions, and compliance included. An AI agent can monitor an account, detect an anomaly, initiate a transfer, file a compliance report, and alert the user, all without human intervention. Visa and Mastercard are actively building **bot payment verification protocols** — agentic commerce, where AI agents make real purchases on behalf of users, is entering the mainstream.

Implications:
- Fraud detection shifts from rule-based to real-time adaptive models
- Customer service becomes anticipatory, not reactive
- Underwriting risk can be repriced per-session using behavioural signals
- Compliance becomes continuous, embedded, and automated (see RegTech below)

### 2. Embedded Finance Evolves into Ecosystems

> "In 2026, embedded finance is no longer about dropping a payment API into an app. The conversation has turned from features to flows." — Innowise, Dec 2025

Modern embedded finance integrates lending, insurance, savings, payroll, and identity checks into **orchestrated, composable architectures**. Rather than a platform offering *one* financial product, they become full financial operating systems:

- **Uber**: seamless in-app payments, driver earnings cards, instant payouts
- **Shopify**: merchant banking, working capital loans, card-present payments
- **Grab/GoPay (SEA)**: insurance, investments, loans, payments — all in one super-app
- **Amazon**: Buy with Prime credit, co-brand cards, Leo merchant lending (synergy with Amazon Leo infra)

McKinsey reports companies implementing embedded finance see **2–5× higher customer lifetime value** and **30% lower acquisition costs**. Embedded finance generates up to **$70 in additional annual revenue per customer** through transaction fees and retention.

### 3. Agentic Commerce

AI agents are making real purchases online. Not just recommending — buying. Visa and Mastercard are building the protocols to verify AI agents and enable secure bot-free payments. Key open questions: liability when an agent makes a bad purchase, regulatory treatment of agent-initiated transactions, and authentication standards for non-human principals.

### 4. Open Finance & Full-Spectrum Data Ownership

Open banking was phase one — sharing bank account data via standardised APIs. **Open finance** is phase two: extending data portability to **payroll, pensions, insurance, tax, investment portfolios, and utility bills**. This enables real-time, behaviour-driven financial products. Key 2024–2026 milestones:

- **India Account Aggregator**: processed ~1.2 billion data requests in 2024; largest open finance deployment globally
- **Singapore**: updated third-party risk guidelines 2024 to clarify bank-fintech partnerships
- **Australia**: Consumer Data Right extended beyond banking to energy and telecoms
- **Philippines & Malaysia**: open-finance roadmaps introduced, targeting unbanked populations
- **EU PSD3 / FiDA**: Financial Data Access regulation moving toward vote in 2026, expanding PSD2

### 5. Real-Time Payments as Core Infrastructure

Instant settlement systems are no longer a differentiator — they're table stakes. **Real-time payment rails** (PromptPay in Thailand, UPI in India, FedNow in US, PayNow in Singapore, InstaPay in Philippines) are reshaping product strategies with:
- Liquidity automation (hold less cash in float)
- Event-based pricing (price products based on real-time risk signals)
- Millisecond fraud detection (reject fraudulent transactions before settlement)

The implication for non-banks: any merchant or platform can now embed real-time payment acceptance at near-zero marginal cost via BaaS APIs.

### 6. Core Banking Modernisation

Legacy core banking systems (mainframe-era, batch-processing, monolithic) are being replaced with **modular, cloud-native cores** (Mambu, Thought Machine Vault, 10x Banking, Temenos Transact). The migration is painful — tier-1 banks can spend $500M–$1B on core replacements — but the payoff is:
- Hourly product releases (vs. quarterly with legacy)
- Real-time transaction data for AI/ML
- Microservices architecture for BaaS API exposure
- Lower cost per account (~$1–3 vs $15–20 on legacy)

### 7. Super-Apps Mature into Financial Operating Systems

Super-apps are becoming **unified hubs** where users manage payments, banking, insurance, shopping, and communication in one experience. The SEA super-app ecosystem is the global benchmark:

| App | Home Market | Financial Services Offered |
|-----|------------|---------------------------|
| **Grab** | Singapore/SEA | GrabPay, GrabFinance loans, GrabInsure, GrabInvest |
| **Gojek/GoTo** | Indonesia | GoPay, GoPayLater BNPL, GoInvestasi, GoSure |
| **Sea/ShopeePay** | SEA-wide | ShopeePay wallet, SPayLater, SeaBank |
| **TrueMoney** | Thailand | Wallet, BNPL, insurance, remittance |
| **Momo** | Vietnam | Wallet, loans, insurance, bill pay |

WeChat Pay and Alipay remain the OGs. In 2026, the question isn't whether SEA super-apps can add financial services — they already have. The question is whether they can achieve profitability on lending without taking on unacceptable credit risk.

### 8. AI-Powered RegTech

Compliance is now **continuous and embedded**. Real-time risk engines, explainable models (required by EU AI Act), and policy-as-code architectures are replacing point-in-time audits. Key drivers:
- AML/KYC automation: AI reduces false positive rates by 40–60% vs rule-based systems
- Continuous transaction monitoring vs. batch overnight
- Regulatory change management: AI tracks rule changes across jurisdictions and propagates to product configs
- Explainable decisions: regulators require banks to explain credit denials; black-box AI no longer acceptable

### 9. Continuous Identity & Behavioural Biometrics

Identity verification now spans the **full user session** — not just at login. Behaviour (typing cadence, mouse movement, device angle, swipe patterns), biometrics (face, voice), and risk-based triggers combine to create a continuous identity score. Critical for countering:
- Deepfake account takeovers (synthetic video/audio impersonation at login)
- Synthetic identity fraud (AI-generated people with fabricated credit histories)
- Account-as-a-Service (money mules with genuine KYC documents)

### 10. Digital Currencies & Tokenisation

CBDCs and tokenised real-world assets (RWAs) are becoming live financial rails:
- **Thailand CBDC**: Project mBridge cross-border pilot live; retail CBDC pilot ongoing
- **Singapore MAS Project Guardian**: tokenised bonds, funds, FX settlements on-chain
- **Hong Kong**: tokenised green bonds issued on public blockchain
- **EU Digital Euro**: legislative proposal advancing in European Parliament

Tokenised RWAs — bonds, real estate fractional shares, private equity — are creating entirely new liquidity pools for embedded finance products.

### 11. Deobanks (Decentralised + Neobank hybrids)

Financial institutions moving on-chain: **deobanks** fuse blockchain transparency, smart contracts, and compliance-ready design. Token rewards, on-chain referral validation, and seamless wallet integration. Still early, but attracting significant developer attention, particularly in SEA markets with younger, crypto-native demographics.

### 12. Hyper-Personalisation as UX Standard

Real-time personalisation driven by behavioural data and AI is redefining financial product interactions:
- Credit limits that expand/contract based on real-time income signals
- Savings nudges triggered by spending pattern analysis
- Insurance pricing adjusted per journey (car insurance per-trip)
- Interface adapts to user financial literacy level

### 13. Green Finance & ESG as Infrastructure

ESG is evolving from reporting to infrastructure. AI-auditable sustainability data, emissions-aware pricing (higher-rate mortgages for energy-inefficient properties), and climate-positive product design. EU taxonomy requirements plus investor pressure making this non-optional for large institutions by 2026.

### 14. Financial Inclusion via Edge Innovation

Voice-first, multilingual fintech tools extending financial services to unbanked users via low-bandwidth, mobile-native, screenless experiences. Critical for SEA's ~290 million unbanked adults. Key enablers:
- USSD/feature phone support alongside smartphone apps
- Vernacular language AI (Thai, Bahasa, Vietnamese, Tagalog)
- Agent-network last-mile distribution (human agents + digital wallet)
- Biometric KYC without government ID documents

---

## How BaaS Works: The Technical Stack

```
┌─────────────────────────────────────────────────────┐
│             Non-Financial Platform (e.g. Grab)       │
│     (owns customer relationship, UI, distribution)   │
└──────────────────┬──────────────────────────────────┘
                   │ API calls
┌──────────────────▼──────────────────────────────────┐
│              BaaS Layer (e.g. Railsr, Synapse)        │
│  Orchestrates: KYC, card issuance, ledger, FX, AML   │
└──────────────────┬──────────────────────────────────┘
                   │ White-label license access
┌──────────────────▼──────────────────────────────────┐
│          Regulated Bank (balance sheet + licence)     │
│      (holds deposits, issues regulated products)      │
└─────────────────────────────────────────────────────┘
```

Key enabling infrastructure:
- **APIs & SDKs**: Stripe, Plaid, Marqeta (card issuance), Railsr, SDK.finance
- **BaaS providers**: Solarisbank (EU), Railsr (global), Unit (US), Synapse (US), Tonik (PH)
- **Open banking data**: MX, Plaid, Tink (EU), Salt Edge
- **Core banking**: Mambu, Thought Machine, 10x Banking, Temenos
- **Payment rails**: Stripe, Adyen, Checkout.com, 2C2P (SEA)

---

## SEA-Specific Landscape

### APAC BaaS: The Numbers

- **$5.26B in 2026** → **$12.31B by 2031** (18.55% CAGR, Mordor Intelligence)
- APAC growing faster than global average (global BaaS: 16–18% CAGR)
- India Account Aggregator: 1.2B data requests in 2024 — scale proof point
- Singapore, Malaysia, Philippines all launched open-finance regulatory frameworks 2024–2025

### Why SEA Is the Embedded Finance Frontier

1. **290M+ unbanked adults** — massive underserved population
2. **High smartphone penetration** with low bank branch density
3. **Super-app ecosystem** already built (Grab, Gojek, Sea) — distribution solved
4. **Young, digital-native demographics** — median age Indonesia 29, Philippines 25
5. **Regulatory experimentation** — sandbox regimes in SG, TH, ID, MY encourage BaaS pilots
6. **Remittance flows** — ~$130B annually in SEA; massive fintech opportunity for cross-border rails

### Key SEA Fintech Players 2026

| Company | Country | Model | Notable |
|---------|---------|-------|---------|
| **GrabFinance** | SG/SEA | Super-app embedded | BNPL, loans, GrabPay wallet |
| **SeaBank** | PH/ID | Neobank | 90M+ registered users via Shopee |
| **Tonik** | PH | Digital bank + BaaS | First neobank in PH to go BaaS |
| **Akulaku** | ID | BNPL/neobank | 10M+ users, expanding regionally |
| **Kredivo** | ID | BNPL | $270M raised; real-time credit scoring |
| **2C2P** | TH | Payment orchestration | Powers regional merchant payments |
| **TrueMoney** | TH | Super-wallet | 26M+ users; CP Group ecosystem |
| **Momo** | VN | Super-wallet | 31M+ users; dominant in Vietnam |

---

## Key Risks & Challenges

### 1. BaaS Regulatory Scrutiny
US regulators (OCC, FDIC) have cracked down on BaaS arrangements where bank partners had inadequate oversight of fintech partners' compliance. Several BaaS banks faced enforcement actions 2023–2025. This is tightening globally — banks face reputational and regulatory risk from careless fintech partnerships.

### 2. Credit Quality in Embedded Lending
BNPL defaults rose significantly 2022–2024 as pandemic-era underwriting assumptions proved optimistic. Embedded lending at checkout removes friction but also removes deliberation — credit risk underwriting in high-volume, low-friction channels requires sophisticated real-time AI scoring.

### 3. Data Privacy vs Personalisation
Open finance requires sharing sensitive financial data across more parties. GDPR (EU), PDPA (Thailand/SEA), and similar frameworks create compliance complexity. Users benefit from personalisation but are increasingly aware of data sharing risks.

### 4. Concentration Risk in Infrastructure
If Stripe, Plaid, or Marqeta has an outage, hundreds of embedded finance products fail simultaneously. Critical infrastructure concentration risk is growing as the ecosystem consolidates around a small number of platform providers.

---

## What to Watch in 2026

1. **EU FiDA regulation vote** — will it create the world's most comprehensive open finance framework?
2. **Agentic payment standards** — Visa/Mastercard bot payment protocols; will a universal standard emerge?
3. **SEA super-app profitability** — can Grab/GoTo finally make their lending books profitable?
4. **CBDC real-world deployments** — will Project mBridge (BIS/BofT/PBOC/HKMA/UAE) scale to commercial use?
5. **BaaS consolidation** — regulatory pressure squeezing marginal BaaS providers; expect M&A
6. **Real-time payments global interoperability** — Project Nexus (BIS) linking PromptPay/UPI/PayNow into a single cross-border rail; live pilot expected 2026

---

*Sources: Precedence Research "Fintech-as-a-Service Market" (Feb 25, 2026); Asian Business Review / Mordor Intelligence "APAC BaaS market to reach $5.3B" (Jan 2026); Innowise "Fintech Trends 2026" (Dec 23, 2025); SDK.Finance "Embedded Finance Solutions Guide 2026" (Feb 2026); SDK.Finance "Top BaaS Companies 2026" (Feb 2026); Juniper Research "Embedded Finance: 3 Key Trends"; Allied Market Research "Embedded Finance Market" (Jan 2025); ResearchNester "Banking as a Service Market to 2035"*
