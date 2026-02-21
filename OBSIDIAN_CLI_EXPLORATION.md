# Obsidian CLI Integration — Exploration

**Date:** 2026-02-21  
**Tool:** `notesmd-cli` (community) or official Obsidian CLI (v1.12.0+)

---

## What is Obsidian CLI?

Obsidian CLI lets you interact with Obsidian vaults from the terminal:
- Create, open, search, move, delete notes
- Manage daily notes
- Edit frontmatter
- Works without Obsidian running (direct file access)

**Install options:**
- Homebrew: `brew install yakitrak/yakitrak/notesmd-cli`
- npm: `npm install -g notesmd-cli`
- Build from Go source

---

## Why Connect OpenClaw to Obsidian?

OpenClaw produces **lots of markdown**:
- Research reports (`research/`)
- Content digests (`content/`)
- Daily logs (`memory/`)
- Agent summaries (`reports/`, `meta-report-latest.md`)

Obsidian is a **powerful knowledge base** with:
- Graph view (connections between notes)
- Backlinks
- Tags and properties
- Full-text search
- Dataview plugin (query your notes like a database)

Integrating them lets you:
1. **Sync OpenClaw output** → Obsidian vault for personal review
2. **Create daily notes** that link to today's reports
3. **Search across all research** with Obsidian's fuzzy search
4. **Build a personal knowledge graph** of AI/tech trends
5. **Use Dataview** to generate custom summaries (e.g., "show all anime streaming reports")

---

## Possible Integrations

### 1. Daily Digest → Obsidian Daily Note

Augment the daily digest to also create/update an Obsidian daily note that includes:
- Links to today's research reports
- Content summaries
- System health metrics
- Agent activity

```bash
# In daily-digest.sh (or a new agent step)
if command -v notesmd-cli &>/dev/null; then
  VAULT="/path/to/your/vault"
  DATE=$(date +%Y-%m-%d)
  NOTE="${DATE} - OpenClaw Summary"

  # Build content from today's files
  CONTENT="# ${DATE}\n\n## Research\n"
  for f in research/${DATE}-*.md; do
    [ -e "$f" ] && CONTENT+="- [[$(basename $f .md)]]\n"
  done
  CONTENT+="\n## Content\n"
  for f in content/${DATE}-*.md; do
    [ -e "$f" ] && CONTENT+="- [[$(basename $f .md)]]\n"
  done

  notesmd-cli create "$NOTE" --content "$CONTENT" --vault "$VAULT" --overwrite
fi
```

### 2. Research Index → Obsidian Dashboard

Create an Obsidian note that uses **Dataview** to list recent research by category:

```markdown
```dataview
TABLE file.mtime as Updated
FROM "research"
WHERE file.name =~ "2026-02"
SORT file.mtime DESC
```
```

### 3. Quick Command: `quick obsidian-open <note>`

Add to `quick` launcher to open notes in Obsidian from the terminal.

### 4. Search Integration

Add `quick obsidian-search <query>` that uses `notesmd-cli search-content` but also falls back to local memory search.

---

## Implementation Plan (if you want this)

1. **Install** `notesmd-cli` (Homebrew/npm)
2. **Configure** default vault: `notesmd-cli set-default "OpenClaw"`
3. **Create** an `obsidian-sync/` script that:
   - Creates daily notes linking to today's outputs
   - Indexes research by tags/categories
   - Updates a dashboard note with latest stats
4. **Add cron job** (or extend daily-digest) to run the sync
5. **Optional:** Use Obsidian's **Dataview** plugin for dynamic queries

---

## Experimental

If you're curious, we can:
- Try installing `notesmd-cli` now and test basic commands
- Create a sample Obsidian vault in the workspace (`obsidian-vault/`)
- Hook it into the daily digest to see results
- Add a quick command for manual triggering

Want to give it a shot? (◕‿◕)♡
