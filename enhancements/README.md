# Enhancement Bot System

The **Enhancement Bot** is an automation system for processing and implementing small improvement proposals within the workspace. It enables self-directed refinement of tools, scripts, and workflows.

## How It Works

1. **Propose** an enhancement using `quick enhancement-propose`
2. **Queue**: Proposal saved as JSON in `enhancements/` with status `proposed`
3. **Daemon**: The `enhancement-bot-daemon.sh` polls the queue, picks highest-priority ready items
4. **Execute**: Runs the associated script, captures output
5. **Update**: Proposal status set to `implemented` (success) or `failed` (error)
6. **Log**: All actions logged to `memory/enhancement-bot.log`

## Workflow

### Submitting a Proposal

Use `quick enhancement-propose`:

```bash
quick enhancement-propose "Title" "Description" priority /path/to/script.sh
```

**Parameters:**
- `title`: Short descriptive title (used in filename)
- `description`: Detailed explanation of the improvement
- `priority`: 1 (highest) to 5 (lowest)
- `script`: Path to executable script that implements the enhancement

**Example:**
```bash
quick enhancement-propose "Fix quick launcher typo" "Correct misspelled command in help text" 5 scripts/fix-quick-typo.sh
```

This creates a file like `enhancements/fix-quick-typo-20260226-170000.json`.

### Viewing the Queue

```bash
quick enhancement-list
```

Shows all proposals with their status, priority, title, and creation timestamp.

### Starting/Stopping the Daemon

```bash
quick enhancement-bot-start   # Start daemon (runs in background)
quick enhancement-bot-stop    # Stop daemon
```

The daemon:
- Runs continuously, polling every 30 seconds
- Uses PID file: `memory/enhancement-bot.pid`
- Logs to: `memory/enhancement-bot.log`
- Processes `proposed` and `ready` items in priority order

### Proposal JSON Format

```json
{
  "title": "Short title",
  "description": "What this enhancement does and why it's valuable",
  "priority": 3,
  "script": "/absolute/path/to/script.sh",
  "status": "proposed",  // or "ready", "implemented", "failed"
  "created_at": "2026-02-26T17:00:00Z",
  "updated_at": "2026-02-26T17:00:00Z",
  "implemented_at": null,
  "failed_at": null,
  "result": ""
}
```

## Best Practices

- **Scripts should be idempotent**: Safe to run multiple times
- **Include validation**: Scripts should verify changes worked and exit non-zero on failure
- **Keep proposals small**: One improvement per proposal
- **Test manually first**: Before submitting, run the script manually to ensure it works
- **Use descriptive titles**: Helps with queue management
- **Respect priority**: 1 = critical, 5 = nice-to-have

## Example Proposals

See `example-proposal-fix-quick-typo.json` for a minimal working example.

## Troubleshooting

**Daemon won't start:**
- Check PID file exists and is not stale: `cat memory/enhancement-bot.pid`
- Ensure script paths in proposals are executable
- Check log: `tail -n 50 memory/enhancement-bot.log`

**Proposal stuck in `proposed`:**
- Daemon might not be running: `quick enhancement-bot-start`
- Check script exists and is executable
- Verify JSON format is valid: `jq . enhancements/your-proposal.json`

**Script fails:**
- Status changes to `failed`
- Error output captured in `result` field of JSON
- Check log for details

## Development

To modify the enhancement-bot itself:
- Daemon logic: `scripts/enhancement-bot-daemon.sh`
- Start/stop wrappers: `scripts/enhancement-bot-start.sh`, `scripts/enhancement-bot-stop.sh`
- Queue management: `scripts/enhancement-list.sh`
- Proposal creation: `scripts/enhancement-propose.sh`

The system is designed to be simple, robust, and easy to extend.

## Philosophical Note

This bot embodies the principle of **continuous, automated improvement**. Small, well-scoped enhancements can be proposed and executed without manual intervention, allowing the workspace to evolve organically while maintaining stability through validation and logging.

Use responsibly. Not every improvement needs automation—reserve this for changes that are safe, repeatable, and clearly beneficial.