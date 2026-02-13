# Gapping Method in Banking Industry: Comprehensive Research Report

## Executive Summary

The gapping method (also known as gap analysis) is a fundamental tool in banking for measuring and managing interest rate risk within asset-liability management (ALM). While it has been largely supplemented by more sophisticated techniques, gap analysis remains a cornerstone of banking risk management frameworks worldwide and is subject to ongoing regulatory scrutiny, particularly in light of recent bank failures like Silicon Valley Bank.

---

## 1. Definition of Gapping Method

### Core Definition
**Gap** is defined as the difference between rate-sensitive assets (RSA) and rate-sensitive liabilities (RSL) that will reprice or mature within a specific time period:

**Gap = Rate-Sensitive Assets (RSA) - Rate-Sensitive Liabilities (RSL)**

This measures the mismatch between assets and liabilities that will be affected by interest rate changes within given time buckets (e.g., 0-3 months, 3-6 months, 6-12 months, etc.).

### Types of Gap Analysis

1. **Static Gap Analysis**
   - Provides a snapshot at a single point in time
   - Compares the amount of assets and liabilities that will reprice within specific time periods
   - Simple, uses readily available accounting data
   - Most basic form of gap analysis

2. **Dynamic Gap Analysis**
   - Tracks changes over time
   - Accounts for continuous inflow and outflow of funds (new deposits, loan originations, repayments)
   - More complex and requires ongoing data collection
   - Provides a more realistic view of actual exposure

3. **Duration Gap Analysis**
   - Uses weighted average duration of assets and liabilities
   - Considers the timing and magnitude of cash flows
   - More sophisticated measurement of interest rate risk
   - Captures the sensitivity of economic value to rate changes

---

## 2. Application in Banking (Use Cases)

### Primary Use: Interest Rate Risk Management

Gap analysis is primarily used to measure a bank's exposure to interest rate fluctuations in the **banking book** (not the trading book). The technique helps banks understand how changes in interest rates will affect their:

- **Net Interest Income (NII)**
- **Economic Value of Equity (EVE)**

### Key Applications:

1. **Asset-Liability Committee (ALCO) Reporting**
   - Gap reports are standard agenda items in ALCO meetings
   - Used to set risk limits and monitor compliance
   - Helps inform strategic balance sheet decisions

2. **Identifying Repricing Mismatches**
   - Banks group assets and liabilities into "repricing buckets"
   - Compare RSA vs. RSL within each bucket
   - Identify where mismatches create risk exposure

3. **Scenario Analysis and Stress Testing**
   - Project NII changes under different interest rate scenarios
   - Assess impact of sudden rate movements
   - Inform hedging strategies

4. **Balance Sheet Optimization**
   - Guide decisions about asset allocation
   - Inform liability management strategies
   - Help "ride the yield curve" when appropriate

### Gap Positioning:

- **Positive Gap (Asset-Sensitive)**: RSA > RSL in a time period
  - Bank benefits when rates rise (more assets reprice than liabilities)
  - Exposed to falling rates

- **Negative Gap (Liability-Sensitive)**: RSL > RSA in a time period
  - Bank benefits when rates fall
  - Exposed to rising rates
  - Common when yield curve has positive slope (borrow short, lend long)

---

## 3. Benefits and Risks

### Benefits of Gap Analysis:

1. **Simplicity and Transparency**
   - Easy to understand and explain to stakeholders
   - Uses straightforward accounting data
   - No complex mathematics or statistics required

2. **Effectiveness for Simple Balance Sheets**
   - Works well for portfolios dominated by basic instruments
   - Useful for community banks with straightforward operations

3. **Diagnostic Tool**
   - Helps identify *why* more sophisticated models produce certain results
   - Useful for finding strategies to change exposure
   - Provides intuitive understanding of repricing risk

4. **Regulatory Acceptance**
   - Well-established method recognized by regulators
   - Standard supervisory expectations
   - Required component of many regulatory reports (e.g., FSA017 in UK)

5. **Cost-Effective**
   - Less expensive to implement than advanced simulation models
   - Requires fewer computational resources
   - Can be done with spreadsheet tools initially

### Risks and Limitations:

1. **Incomplete Risk Capture**
   - **Does NOT measure magnitude** of rate changes (only directional exposure)
   - **Fails to capture basis risk** (different rates moving differently)
   - **Cannot account for yield curve risk** (e.g., steepening/flattening)
   - **Excludes foreign exchange risk** and correlation risk between currencies
   - **Doesn't capture optionality** embedded in financial instruments (prepayment options, call features)

2. **Static Nature**
   - Snapshot approach doesn't reflect ongoing balance sheet changes
   - Ignores impact of new business originations
   - Cannot model rollover behavior accurately

3. **Bucket Issues**
   - Large discontinuities when positions cross time buckets
   - Example: A 194-day asset in 7-12 month bucket moves to 3-6 month bucket in 2 weeks, creating artificial mismatches
   - Cannot offset mismatches across different time periods

4. **Book Value vs. Market Value**
   - Uses accounting (book) values, not market values
   - Can significantly bias risk measurement when interest rates change
   - Doesn't reflect true economic exposure

5. **Ignores Interest Flows**
   - Doesn't account for reinvestment risk from coupon payments
   - Misses interim cash flow effects

6. **Limited Time Horizon**
   - Traditionally focuses on 12-month horizon
   - Does not capture long-term structural risks
   - Earnings-at-Risk (EaR) models now preferred for short-term measurement

---

## 4. Notable Examples and Case Studies

### Silicon Valley Bank (SVB) Collapse - March 2023

**The Failure Case Study:**

Silicon Valley Bank's collapse represents a textbook example of **duration gap mismanagement** and how gap analysis (when properly applied) could have identified critical vulnerabilities.

**Key Issues:**
1. **Massive Positive Duration Gap**: SVB's assets had much longer duration than liabilities
   - Assets: Heavy concentration in long-term fixed-income securities (held-to-maturity and available-for-sale portfolios)
   - Liabilities: Predominantly short-term, rate-sensitive deposits from tech startups and venture capital firms

2. **Failed to Adjust Position**: Despite rapid interest rate hikes by the Federal Reserve (2022-2023), SVB did not reduce its duration gap through hedging or balance sheet adjustments

3. **Unrealized Losses**: As rates rose, the market value of long-term bonds fell dramatically. When SVB was forced to sell assets to meet deposit withdrawals, they realized massive losses

4. **Liquidity Crisis**: The negative equity triggered a bank run, as depositors realized the bank's vulnerability

**Regulatory Findings** (Federal Reserve Review, April 2023):
- "Textbook case of mismanagement" (Michael Barr, Fed Vice Chair for Supervision)
- Supervisors did not fully appreciate the extent of vulnerabilities
- Bank failed to implement controls to effectively mitigate interest rate risk
- Deficiencies in governance, liquidity risk management, and interest rate risk management

**Post-SVB Regulatory Response:**
- Stricter examination of bank interest rate risk management
- Increased focus on duration gap disclosure requirements
- Enhanced stress testing expectations
- Proposals for mandatory duration gap disclosure (MIT Sloan research paper)

### Historical Context: 1980s Banking Crisis

Gap analysis became widely adopted in the 1980s when:
- Interest rates became highly volatile
- Regulatory changes (Depository Institutions Deregulation and Monetary Control Act) allowed more flexibility in pricing
- Many savings and loan institutions failed due to negative gaps when rates rose (short-term liabilities repriced faster than long-term fixed-rate assets)

---

## 5. Current Regulatory Stance

### United States Regulatory Framework

**Federal Reserve, FDIC, OCC Requirements:**

1. **Interest Rate Risk in the Banking Book (IRRBB)**
   - Federal banking agencies require comprehensive IRRBB management
   - Gap analysis is a foundational component, though not sufficient alone
   - Expected to be part of a broader risk measurement system

2. **Examination Manuals (FDIC)**
   - Section 7.1 (Sensitivity to Market Risk) addresses gap analysis
   - Recognizes gap analysis as having "several advantages" including simplicity
   - However, expects supplementary measurements: Economic Value of Equity (EVE) and Earnings-at-Risk (EaR)

3. **Comprehensive Capital Analysis and Review (CCAR)**
   - Large banks must project NII and capital under stress scenarios
   - Gap methodology informs these projections
   - Requires both static and dynamic analysis

4. **Basel III Endgame (Proposed 2023)**
   - While focused on capital requirements, indirectly affects gap management
   - Stricter capital buffers require more sophisticated risk measurement
   - Banks may need advanced models beyond simple gap analysis

### International Regulatory Standards

**Basel Committee on Banking Supervision:**
- IRRBB standards (2016) acknowledge gap analysis as a traditional approach
- Recommend multiple measurement techniques
- Emphasize need for validation of gap assumptions
- Particularly stress behavioral assumptions for prepayable assets and non-maturity deposits

**Bank of England / Prudential Regulation Authority (PRA):**
- FSA017 regulatory reporting requires interest rate gap data
- Allows firms to report after taking account of "behavioral assumptions"
- Requires adjusted expected repricing dates for products with behavioral characteristics different from contractual terms

**Reserve Bank of India (RBI):**
- Detailed guidelines for Asset-Liability Management systems
- Requires gap reports grouping rate-sensitive assets, liabilities, and off-balance sheet items
- Specific classification criteria for rate sensitivity (cash flows, repricing, prepayment options, RBI rate dependence)

### Current Best Practices

Regulators expect banks to use **multiple complementary approaches**:

1. **Short-term (12-24 months)**: Static gap + Earnings-at-Risk (EaR) simulations
2. **Long-term (economic value)**: Duration gap + Economic Value of Equity (EVE) analysis
3. **Stress testing**: Severe but plausible scenarios
4. **Behavioral modeling**: For non-maturity deposits and prepayable loans
5. **Validation**: Regular back-testing of gap assumptions and limits

---

## Conclusion

The gapping method remains an essential, though not sufficient, tool for banking interest rate risk management. Its simplicity provides intuitive insights into repricing mismatches, making it valuable for board reporting and initial risk identification. However, its limitations—particularly inability to capture magnitude of rate changes, basis risk, and optionality—mean regulators and sophisticated banks now supplement gap analysis with earnings simulations, duration analysis, and economic value calculations.

The SVB failure demonstrated that even in 2023, fundamental gap management mistakes can be catastrophic. Post-crisis, regulators are likely to increase scrutiny of gap methodology, particularly behavioral assumptions and integration with stress testing frameworks. Banks should maintain robust gap analysis as part of a multi-faceted IRRBB management system rather than relying on it exclusively.

---

## Sources Consulted

- Northland BancPath - ALM Basics: GAP Reports (2011)
- LinkedIn - Gap Analysis by Mohammad Salman Khan (2019)
- Federal Reserve - Supervision Review of Silicon Valley Bank (2023)
- FDIC - Examination Policies Manual Section 7.1
- Bank of England - FSA017 Instructions (2022)
- MIT Sloan - Duration Gap Disclosure Proposal (2024)
- SUERF Policy Brief - Duration Gap and Bank Lending (2024)
- Corporate Finance Institute - Negative Gap Analysis
- Accounting Insights - Managing Gaps in Banking (2024)
- Investopedia - Static Gap and Dynamic Gap definitions
- Various peer-reviewed academic papers on banking risk management

---

*Research completed: February 13, 2026*
*Subagent session: agent:main:subagent:9751d90f-9268-4200-8dd6-cdaa78ec4d76*
