# Findings: Need for Systemd Linger Validation

**Workspace Analysis (2026-03-02 07:10 UTC)**
- Overall health: green
- Disk: 78% (stable)
- Git: clean
- Memory: 29/37 files indexed, reindex 1.9d fresh
- Cron: all jobs ok
- active-tasks size: 714 bytes (<2KB)
- MEMORY.md: 32 lines (≤35)
- Constraints: all 8 checks passing

**Identified Gap**
The current constraint set does not verify that systemd lingering is enabled for the `ubuntu` user. According to MEMORY.md and lessons learned:

> "Systemd linger required — Enable with `sudo loginctl enable-linger $USER` so user services survive logout/reboot. Without it, openclaw-gateway.service stops, killing all agents."

This is a critical reliability factor for 24/7 operation. If lingering is disabled, the gateway and all agents will terminate when the user logs out or the session ends, requiring manual restart until watchdog notices.

**Why Add a Check Now?**
- The system currently has lingering enabled (`/var/lib/systemd/linger/ubuntu` exists). But there is no automated guard against accidental disabling (e.g., via `loginctl disable-linger` or system reconfiguration).
- Adding a validation constraint ensures immediate alerting if this setting is ever lost.
- It aligns with the documented best practice and completes the health envelope.

**Impact**
- Minimal code change: one new conditional block in `scripts/validate-constraints.sh`.
- Help text update in `quick` for consistency.
- No performance impact.
- Maintains all existing passing constraints.

**Conclusion**
Adding a dedicated check for systemd linger strengthens the workspace's self-monitoring capabilities and supports the 24/7 operational goal.
