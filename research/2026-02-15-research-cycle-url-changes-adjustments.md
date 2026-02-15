# Research Cycle Update — URL Structure Changes, Need New Leads (2026‑02‑15 12:39 UTC)
**Research‑agent tactical report** • Continuous research

---

## 🎯 Mission

Execute priority leads from `watchlist-priority-gaps-2026-02-15.md`:
1. **Nvidia Blackwell real‑world performance** → MLPerf Training/Inference v4.0
2. **CBDC live transaction volumes** → BIS statistics or Atlantic Council tracker

---

## 🔬 Results This Cycle

### 1. MLPerf Training/Inference Pages — 404

**Attempted URLs:**
- https://mlcommons.org/benchmarks/mlperf-training/
- https://mlcommons.org/benchmarks/mlperf-inference/

**Result:** 404 Not Found.

**Observations:** From the MLPerf Automotive page, the navigation shows:
- MLPerf Training: HPC
- MLPerf Inference: Datacenter
- MLPerf Inference: Edge
- MLPerf Inference: Mobile

So the correct URLs are likely:
- https://mlcommons.org/en/mlperf-training/ (still 404)
- https://mlcommons.org/en/mlperf-inference/datacenter/
- Or subpages under /benchmarks/ with different path

**Action:** Try the `/en/` paths directly; if still 404, resort to Google site: search or look for third‑party coverage (Analytics India Magazine, The Next Platform) that summarizes MLPerf results.

---

### 2. BIS CBD Statistics — 404

**Attempted URL:** https://www.bis.org/statistics/payments_statistics.htm

**Result:** 404 Page not found.

**Inference:** BIS site structure changed; CBDC stats may be under a different program (e.g., " payments and settlements" or "digital currencies").

**Action:** Search BIS for "CBDC" or "digital currency statistics". Alternative sources:
- IMF Financial Access Survey (FSD)
- World Bank Global Findex
- Atlantic Council CBDC Tracker (still need working URL)
- National central bank reports (e.g., PBOC, ECB, BoE)

---

## 📊 Updated Priority Gap Status

| Gap | Priority | Lead Status | Next Action |
|-----|----------|-------------|-------------|
| SWE‑Bench failure taxonomy | 🔴 CRITICAL | Not started | Scrape GitHub/Hacker News for Claude/Cursor failure reports |
| Data center power constraints | 🔴 CRITICAL | Not started | Fetch CAISO/ERCOT filings, DOE studies |
| CBDC live transaction volumes | 🔴 CRITICAL | BIS 404, Atlantic Council 404 | Find current BIS CBDC stats page; try IMF/World Bank |
| Blackwell real‑world performance | 🔴 CRITICAL | MLPerf pages 404 | Try /en/ paths; search for "MLPerf Training v4.0 results" via Google |
| Anime Q4 2025 earnings | 🟠 HIGH | Not started | Locate Sony/Netflix Q4 FY2025 earnings (if published) |
| Open‑source cost curves | 🟠 HIGH | Not started | Monitor marc0.dev, Hugging Face, cloud pricing |
| AI safety incidents | 🟠 MEDIUM | Not started | Visit aiincidents.org, NIST AI Safety Institute |

---

## ⚠️ Constraints & Adjustments

- **Brave Search rate limits** (429) → using targeted `web_fetch` on known URLs
- **Site restructuring** (MLCommons, BIS) → original URLs defunct; must discover current paths
- **Quiet hours** approaching (23:00–08:00 UTC+7) → will pause after this report; resume tomorrow if needed

---

## 📝 Report Metadata

- **Filename:** `2026-02-15-research-cycle-url-changes-adjustments.md`
- **Size:** ~3 KB
- **Deliverable:** Documentation of failed fetches and revised leads
- **Status:** Ready to commit

---

**Research‑agent signing off before quiet hours, nya~! (◕‿◕)♡**

*Next: attempt new URLs after quiet hours or tomorrow.*