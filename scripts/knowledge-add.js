#!/usr/bin/env node
// knowledge-add — fetch URL or raw text and append to memory/knowledge/<date>-<slug>.md with source attribution

const fs = require('fs');
const path = require('path');
const { pipeline } = require('@xenova/transformers');
const https = require('https');

const ROOT = process.env.WORKSPACE || '/home/ubuntu/.openclaw/workspace';
const KNOW_DIR = path.join(ROOT, 'memory', 'knowledge');
const INDEX_PATH = path.join(ROOT, 'memory', '.semantic_index.json');

if (!fs.existsSync(KNOW_DIR)) fs.mkdirSync(KNOW_DIR, { recursive: true });

async function fetchUrl(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { timeout: 10000 }, res => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => resolve(data));
      res.on('error', reject);
    }).on('error', reject);
  });
}

async function summarize(text) {
  // Very lightweight: take first 3 sentences or 300 chars
  const sentences = text.split(/(?<=[.!?])\s+/).filter(Boolean);
  return sentences.length > 3 ? sentences.slice(0, 3).join(' ') + '...' : text.slice(0, 300) + (text.length>300?'...':'');
}

async function main() {
  const [, , ...args] = process.argv;
  if (args.length < 1) {
    console.error('Usage: knowledge-add <url|text> [--title "My Note"]');
    process.exit(1);
  }

  let title;
  const titleIdx = args.indexOf('--title');
  if (titleIdx !== -1) {
    title = args[titleIdx + 1];
    args.splice(titleIdx, 2);
  }

  const input = args[0];
  let content, source;
  if (input.startsWith('http://') || input.startsWith('https://')) {
    source = input;
    console.log('Fetching URL...');
    content = await fetchUrl(input);
  } else {
    source = 'manual';
    content = input;
  }

  if (!title) {
    title = source !== 'manual' ? new URL(source).hostname : 'Manual Note';
  }

  const date = new Date().toISOString().slice(0, 10);
  const slug = title.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const filename = `${date}-${slug}.md`;
  const filepath = path.join(KNOW_DIR, filename);

  const summary = await summarize(content);
  const markdown = `# ${title}\n\n**Source:** ${source}\n**Date:** ${date}\n\n${summary}\n\n\`\`\`\n${content.slice(0, 2000)}\n\`\`\`\n`;

  fs.writeFileSync(filepath, markdown, 'utf8');
  console.log(`Saved: memory/knowledge/${filename}`);

  // Append to global semantic index (simple chunk + embed later)
  // For now, just note that user should re-run semantic-index to include this file.
  console.log('Note: Run `quick semantic-index` to include this in semantic search.');
}

main().catch(err => {
  console.error('Error:', err.message);
  process.exit(1);
});
