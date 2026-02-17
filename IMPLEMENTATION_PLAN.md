# Implementation Plan — Ultimate Autonomous System

## Phase 1: Meta‑Agent Core

### Step 1.1: Create agents/meta-agent.sh
- Accepts `--once` (one-shot) and `--daemon` modes
- In `--once`:
  - Reads recent supervisor logs (last 24h) and agent‑manager logs
  - Queries system status via `./quick health` and `./quick agent-status`
  - Checks memory reindex status
  - Evaluates if any automatic actions are needed (e.g., reindex, cleanup)
  - If actions required: spawns appropriate agents for those tasks
  - Generates `meta-report-latest.md` in workspace root
- In `--daemon`: loops hourly with quiet‑hour respect

### Step 1.2: Add meta-agent-cron
- Schedule: `0 * * * *` (every hour) in Asia/Bangkok
- Payload: `./agents/meta-agent.sh --once`
- Delivery: `announce` (Telegram summary of actions taken)

### Step 1.3: Extend quick launcher
- `quick meta` — run meta‑agent once
- `quick meta-report` — show latest meta‑report
- `quick meta-logs` — tail meta‑agent logs (`memory/meta-agent.log`)

### Step 1.4: Document
- Update `CRON_JOBS.md` with meta‑agent‑cron entry
- Update `active-tasks.md` when meta‑agent first runs

### Step 1.5: Checkpoint
- Create `autonomous-checkpoints.json` with phase 1 completion marker

---

## Phase 2: Goal‑Driven Planning (post‑Phase 1 validation)

### Step 2.1: Enhance meta-agent planning
- Parse logs to detect patterns:
  - Frequent disk usage spikes → schedule more frequent cleanups
  - Repeated agent timeouts → adjust timeouts or split tasks
  - Missing content/research on certain days → adjust schedules or triggers
- Create `meta‑plan.md` with proposed changes (cron schedule edits, new agents, threshold adjustments)

### Step 2.2: Execution via sub‑agents
- For each plan item, spawn a temporary agent using `sessions_spawn` with specific instructions
- Examples:
  - "Modify agent‑manager to also check for orphaned aria2 downloads"
  - "Add a new cron job to refresh content index daily at 06:00 ICT"
- Capture results; on success, apply changes (edit files, update cron)
- On failure, log to `memory/meta‑failures.md` and propose alternative

### Step 2.3: Validation & commit
- After implementing changes, run validation (`./quick validate` or subset)
- If all OK, commit with `meta:` prefix and push
- Update `active-tasks.md` with meta cycle validation

### Step 2.4: Checkpoint
- Mark phase 2 complete; store last plan and outcome in `autonomous-checkpoints.json`

---

## Phase 3: Self‑Extension (later)

- Meta can create new agent templates by copying existing ones and modifying prompts
- Meta can add new quick commands dynamically (by appending to `quick` and re‑sourcing)
- Meta can register new cron jobs via `openclaw cron add`

---

## Phase 4: Learning Loop (later)

- Store success rates of different strategies in `memory/meta‑learning.md`
- Use embeddings to find similar past situations and apply known good fixes

---

## Execution Start

Begin Phase 1 immediately.
