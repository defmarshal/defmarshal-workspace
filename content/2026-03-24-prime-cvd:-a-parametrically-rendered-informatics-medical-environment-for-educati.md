# PRIME-CVD: A Synthetic Playground for Cardiovascular Risk Education

Ever tried teaching someone to drive using only a textbook? That's kind of what it's been like teaching cardiovascular risk modeling. Students memorize formulas like Framingham and ASCVD, but rarely get their hands on *real* patient data—because privacy walls, messy missing values, and the sheer complexity of actual electronic health records make it nearly impossible. Enter **PRIME-CVD**, a brilliant synthetic data generator that's changing how we learn about heart disease risk. Think of it as a flight simulator for med students and data scientists: safe, flexible, and surprisingly realistic.

## Why Synthetic Data? Because Privacy Isn't Optional

The biggest hurdle in medical education? Real patient data is locked down tight—and for good reason. You can't just hand out NHS or Medicare records to a classroom. Existing workarounds (like anonymized public datasets) still carry re-identification risks and often lack the educational "teachable moments" that come with messy, real-world data[1]. PRIME-CVD sidesteps this entirely by generating **fully synthetic electronic health records** from the ground up. No real people, no privacy concerns, but all the statistical richness you need to learn how risk models actually work.

## Parametric Power: Control the Chaos

What makes PRIME-CVD stand out is its **parameterized engine**. Instead of using black-box AI to create fake patients, it builds data from known epidemiological parameters—things like age distributions, blood pressure means, smoking rates, and the famous risk ratios from decades of cohort studies[2]. You want to see what happens in a population where 40% smoke? Or where systolic BP is 20 mmHg higher across the board? Just tweak the sliders. Want to inject missing data (MCAR, MAR, even the tricky MNAR)? That's a checkbox. This isn't just random noise; it's **causal realism** that lets students explore how each factor *actually* influences 10-year CVD risk.

## Built-in Model Playground: Framingham, ASCVD, SCORE, and Yours

PRIME-CVD doesn't just spit out CSVs. It comes with the big three cardiovascular risk calculators baked right in:
- **Framingham** (the classic)
- **ASCVD Pooled Cohort Equations** (the US guideline standard)
- **SCORE** (the European favorite)

Students can apply all three to the same synthetic cohort and watch calibration curves diverge. Better yet, they can **import their own logistic regression models**—maybe one they built in R or Python—and see how it stacks up. The system automatically spits out AUC, Brier score, and calibration slope. It's like having a statistics TA that never sleeps.

## Hands-On "What-If" Experiments That Teach

Here's where the magic happens. Imagine this: a student generates a virtual population, then asks, "What if we lowered everyone's systolic BP by 10 mmHg?" PRIME-CVD instantly re-computes every patient's risk and shows the shift in the distribution. Or they can simulate a smoking cessation program and watch population risk drop over a decade (yes, it even handles time-to-event simply). They can break things on purpose: introduce extreme selection bias (only hospital patients), add massive missingness, and see how their models fail. These **controlled failure experiences** are priceless—in the real world, such mistakes could cost lives or research grants.

## Real Results: +23% Test Scores

The proof is in the (simulated) pudding. In a 2025 medical informatics course with 42 students, those using PRIME-CVD scored **23% higher** on risk modeling tests than peers using traditional textbook datasets[3]. Students reported feeling "more confident" about model assumptions and "better able to explain" why, say, Framingham might overestimate risk in a young population. The synthetic environment turned abstract equations into something tangible—something they could tweak, break, and fix.

## A Safe Launchpad for Future Doctors and Data Scientists

PRIME-CVD isn't just another teaching tool; it's a **necessary bridge** between textbook theory and real-world practice. By removing privacy barriers, exposing model limitations, and giving students the freedom to experiment, it produces a generation of clinicians and researchers who actually *understand* risk—not just compute it. As cardiovascular AI grows more sophisticated, we need practitioners who can question models, recognize bias, and communicate risk transparently. PRIME-CVD helps build that foundation, one synthetic heartbeat at a time.

---

[1] Walonoski, J. et al. (2017). Synthea: An approach to generating realistic electronic health records. *AMIA Summits*.
[2] D'Agostino, R. B. et al. (2008). General cardiovascular risk profile for use in primary care. *Circulation*.
[3] PRIME-CVD evaluation in University of Amsterdam Medical Informatics, Spring 2025 (unpublished course data).