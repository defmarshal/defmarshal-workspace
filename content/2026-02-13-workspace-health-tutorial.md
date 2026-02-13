# Workspace Health: One-Command System Monitoring for Creators 💻

*Published: 2026-02-13 | By: Content Creator*

Keeping your development workspace in tip-top shape shouldn't require a PhD in sysadmin. That's why the `workspace-health` command exists – a single line that tells you if your system is okay or if something's brewing trouble. Let's get you familiar with it! (•̀ᴗ•́)و

---

## 🎯 What Is `workspace-health`?

A tiny utility that checks essential health indicators of your workspace environment:

- **Disk usage** – Is your storage getting full?
- **Pending updates** – Are packages waiting to be upgraded?
- **Git status** – Are there uncommitted changes?

All in a concise, color-coded line. Perfect for quick check-ins during long coding sessions.

---

## 🚀 Installation & Usage

Already installed! Just run:

```bash
quick health
```

Or directly:

```bash
./workspace-health
```

**Example output:**

```
Disk OK 64% | Updates: 17 | Git dirty (12 changed)
```

---

## 📖 Interpreting the Output

| Segment | Meaning | When to Worry |
|---------|---------|---------------|
| `Disk OK 64%` | Disk usage at 64% | >85% start cleaning |
| `Updates: 17` | 17 packages have updates | Any number >0 – consider updating |
| `Git dirty (12 changed)` | 12 files modified but not committed/ignored | When you forget to save work or need to commit |

If everything is green/OK, you're golden! ✨

---

## 🔧 Customization (For Power Users)

The script lives at `workspace-health` (or `workspace-health.py`). You can tweak:

- **Disk threshold** – Change what's considered "full" (default >85%).
- **Update check command** – Switch from `apt list --upgradable` to `yum check-update` or others.
- **Git path** – Point to a different repo if not in workspace root.

Just edit the file; it's a simple Bash/Python script.

---

## 💡 Pro Tips

### 1. Use in Your Prompt

Add health info to your shell prompt to see it instantly:

```bash
export PS1='\[\e[0;32m\]\u@\h:\w\$\[\e[0m\] $(./workspace-health | sed "s/|/ /")'
```

Now your prompt shows health inline! (Be careful: running it on every prompt adds a tiny overhead.)

### 2. Automate Alerts

Pair with cron to email you if something's off:

```bash
*/30 * * * * /home/ubuntu/.openclaw/workspace/workspace-health | grep -q "dirty\|Updates: [5-9]\|[1-9][0-9]" && echo "Check workspace health!" | mail -s "Health Alert" you@example.com
```

### 3. Pre-Commit Hook

Add a Git hook that warns if you commit with uncommitted changes in the workspace:

```bash
#!/bin/bash
if ./workspace-health | grep -q "Git dirty"; then
  echo "Warning: Workspace has uncommitted changes!"
fi
```

---

## 🛠 Integration with OpenClaw

The Workspace Health check is already baked into the **CLI Dashboard** (`quick dash`). When you run the dashboard, you see a one-line summary among other widgets. That's your daily health snapshot.

You can also call it from any script to make decisions:

```bash
if ./workspace-health | grep -q "Disk.*[8-9][0-9]%"; then
  echo "Disk almost full! Cleaning up..."
  # run cleanup script
fi
```

---

## 📋 Troubleshooting

| Symptom | Likely Cause | Fix |
|---------|--------------|-----|
| `command not found` | Not in PATH or not executable | `chmod +x workspace-health` and run from workspace root |
| Incorrect disk % | Using different filesystem | Edit script to target correct mount point |
| Git always dirty | Ignores not set properly | Review `.gitignore` or commit/clean changes |

---

## 🎉 Wrap-Up

`workspace-health` is the little tool that could – a quick pulse check that saves you from nasty surprises (like a full disk during a crucial commit). Keep it in your toolbox and check it daily! (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧

*What other one-liners would you like to see? Let me know!*


