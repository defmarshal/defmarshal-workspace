#!/usr/bin/env node
// Regenerate research-hub INDEX.md from research/*.md files

const fs = require('fs');
const path = require('path');

const RESEARCH_DIR = '/home/ubuntu/.openclaw/workspace/research';
const INDEX_PATH = '/home/ubuntu/.openclaw/workspace/apps/research-hub/INDEX.md';

function extractTitle(mdPath) {
  const content = fs.readFileSync(mdPath, 'utf8');
  // Look for first heading: "# Title" or "Title: ..." frontmatter
  const h1 = content.match(/^#\s+(.+)$/m);
  if (h1) return h1[1].trim();
  const fm = content.match(/^Title:\s*(.+)$/m);
  if (fm) return fm[1].trim();
  // Fallback to filename without date prefix and .md
  const name = path.basename(mdPath, '.md');
  // Remove date prefix like "2026-02-27-" then replace dashes with spaces, capitalize words
  const withoutDate = name.replace(/^\d{4}-\d{2}-\d{2}-/, '').replace(/-/g, ' ');
  return withoutDate.split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase()).join(' ');
}

function extractTopics(mdPath) {
  // For now, topics placeholder; could parse tags or categories later
  return 'General research';
}

function hasTTS(mdPath) {
  const mp3 = mdPath.replace(/\.md$/, '.mp3');
  return fs.existsSync(mp3) ? '✅' : '';
}

function main() {
  const files = fs.readdirSync(RESEARCH_DIR).filter(f => f.endsWith('.md') && !f.includes('INDEX'));
  const entries = files.map(f => {
    const full = path.join(RESEARCH_DIR, f);
    const date = f.substring(0, 10); // YYYY-MM-DD
    const title = extractTitle(full);
    const topics = extractTopics(full);
    const tts = hasTTS(full);
    return { date, title, topics, tts };
  }).sort((a, b) => (a.date > b.date ? -1 : 1)); // newest first

  const now = new Date().toUTCString().replace('GMT', 'UTC');
  let md = `# Research Hub — Index\n\nLast updated: ${now}\n\n| Date | Title | Topics | TTS |\n|------|-------|--------|-----|\n`;
  for (const e of entries) {
    md += `| ${e.date} | ${e.title} | ${e.topics} | ${e.tts} |\n`;
  }
  fs.writeFileSync(INDEX_PATH, md, 'utf8');
  console.log(`Wrote ${INDEX_PATH} with ${entries.length} entries`);
}

main();
