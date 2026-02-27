#!/usr/bin/env node
// semantic-index — Build local semantic search index over memory/*.md, research/*.md, content/*.md
// Uses @xenova/transformers (all-MiniLM-L6-v2). First run downloads ~80MB model.
// Output: memory/.semantic_index.json

const fs = require('fs');
const path = require('path');
const { pipeline } = require('@xenova/transformers');

const ROOT = process.env.WORKSPACE || '/home/ubuntu/.openclaw/workspace';
const MEM_DIR = path.join(ROOT, 'memory');
const KNOW_DIR = path.join(MEM_DIR, 'knowledge');
const RESEARCH_DIR = path.join(ROOT, 'research');
const CONTENT_DIR = path.join(ROOT, 'content');
const INDEX_PATH = path.join(MEM_DIR, '.semantic_index.json');

async function chunkText(text, maxChars = 2000) {
  if (text.length <= maxChars) return [text];
  const chunks = [];
  for (let i = 0; i < text.length; i += maxChars) {
    chunks.push(text.slice(i, i + maxChars));
  }
  return chunks;
}

async function collectFiles() {
  const files = [];
  for (const dir of [MEM_DIR, KNOW_DIR, RESEARCH_DIR, CONTENT_DIR]) {
    if (!fs.existsSync(dir)) continue;
    for (const f of fs.readdirSync(dir)) {
      if (f.endsWith('.md') && !f.startsWith('.') && f !== 'INDEX.md') {
        files.push(path.join(dir, f));
      }
    }
  }
  return files;
}

async function buildIndex() {
  console.log('Loading embedding model...');
  const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');
  const files = await collectFiles();
  console.log(`Indexing ${files.length} files...`);
  const index = [];
  for (const file of files) {
    try {
      const text = fs.readFileSync(file, 'utf8');
      const chunks = await chunkText(text);
      for (const chunk of chunks) {
        const output = await extractor(chunk, { pooling: 'mean', normalize: true });
        const embedding = Array.from(output.data); // Float32Array -> array
        index.push({ file: path.relative(ROOT, file), chunk, embedding });
      }
    } catch (err) {
      console.error(`Error indexing ${file}:`, err.message);
    }
  }
  fs.writeFileSync(INDEX_PATH, JSON.stringify(index));
  console.log(`Index built: ${INDEX_PATH} (${index.length} chunks)`);
}

buildIndex().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
