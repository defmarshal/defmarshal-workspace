# Active Tasks Registry

This file tracks all currently running agents, their session keys, goals, and status. Used for "close the loop" verification and avoiding duplicate work.

**Rules:**
- Max size: 2KB (keep concise)
- Read at start of EVERY session
- Update immediately when spawning or killing agents
- Include session key, goal, started timestamp, and verification status

## Agent Lifecycle

1. **Spawning**: Add entry with `status: running`
2. **Validation**: After completion, update `status: validated` and add verification notes
3. **Cleanup**: Remove entry after verification (or archive to daily log)

## Format

```markdown
- [sessionKey] <agent-name> — <goal> (started: <time>, status: <running/validated/failed>)
  - Verification: <curl/test/check command outputs>
```

## Current Active Tasks

- [agent:main:subagent:9751d90f-9268-4200-8dd6-cdaa78ec4d76] gap-research — Search web for "gapping method in banking industry" (started: 2026-02-13 15:24, status: validated)
  - Verification: Comprehensive research report completed covering all deliverables: 1) Definition of gapping method (gap = RSA - RSL), 2) Banking applications (ALM, interest rate risk, gap reports), 3) Benefits (simplicity, transparency) and risks (limited scope, static nature), 4) Case studies (SVB 2023 failure as key example), 5) Regulatory stance (FDIC, Fed, Basel, PRA all require gap analysis but as part of broader IRRBB framework). Report saved as: gapping-method-banking-research-report.md (12KB, structured with 5 sections, executive summary, conclusion, and sources)

- [agent:main:subagent:3c36d597-6aa7-423b-9834-32670994fcd9] content-agent — Continuous content creation (anime, tech, summaries) (started: 2026-02-13 15:35, status: running)
  - Verification: pending (monitor output cycles)

- [agent:main:subagent:a43a9c2b-7a9c-49c2-983f-30be085c6d17] research-agent — Continuous research on anime, banking, tech, AI (started: 2026-02-13 15:36, status: running)
  - Verification: pending (review report quality and coverage)

- [agent:main:subagent:49b4130a-fc4c-4575-b988-427ff92e1866] dev-agent — Continuous development (tools, automations, infrastructure) (started: 2026-02-13 15:39, status: running)
  - Verification: Initial baseline commit (fix: .gitignore + added agent SOULs, outputs, pending changes). Pushed to GitHub. Workspace clean.
