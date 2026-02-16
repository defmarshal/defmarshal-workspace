# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

### System Maintenance

- `quick updates-check`: List pending APT updates.
- `quick updates-apply [--dry-run|--execute]`: Apply updates (dry-run default; `--execute` to upgrade).
- `quick cleanup-agent-artifacts [--execute] [--force]`: Clean stale agent lock files and empty plan files. Respects quiet hours; use `--force` to run during quiet hours.
- `quick gateway-info`: Show gateway status and remote access setup instructions.
- `quick hygiene`: Run workspace hygiene check (CRLF line endings, executable bits, large untracked files, caches).
- `quick cleanup-downloads [--days N] [--execute] [--verbose]`: Clean old downloads in `workspace/downloads/` (default retention 30 days). Scheduled weekly Sun 06:00 Bangkok.
- `quick cleanup-backups [--keep N] [--execute] [--verbose]`: Clean old backup tarballs in `/home/ubuntu/`. Keeps most recent N (default 1). Scheduled weekly Sun 07:00 Bangkok.
- `quick memory-reindex-check`: Check if memory reindex is needed based on dirty flag and age.
- `quick memory-reindex`: Force reindex of memory files ( Voyage FTS+ ).

Add whatever helps you do your job. This is your cheat sheet.
