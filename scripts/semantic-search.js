#!/usr/bin/env node
// semantic-search — Query local semantic index (memory/.semantic_index.json)
// Usage: semantic-search <query> [--top N]

const fs = require('fs');
const path = require('path');
const { pipeline } = require('@xenova/transformers');

const ROOT = process.env.WORKSPACE || '/home/ubuntu/.openclaw/workspace';
const INDEX_PATH = path.join(ROOT, 'memory', '.semantic_index.json');

async function cosine(a, b) {
  let dot = 0, normA = 0, normB = 0;
  for (let i = 0; i < a.length; i++) {
    dot += a[i] * b[i];
    normA += a[i] * a[i];
    normB += b[i] * b[i];
  }
  return dot / (Math.sqrt(normA) * Math.sqrt(normB) + 1e-8);
}

async function main() {
  const [, , ...args] = process.argv;
  const query = args[0];
  const top = args.includes('--top') ? parseInt(args[args.indexOf('--top') + 1], 10) : 5;

  if (!query) {
    console.error('Usage: semantic-search <query> [--top N]');
    process.exit(1);
  }

  if (!fs.existsSync(INDEX_PATH)) {
    console.error('Index not found. Run semantic-index first.');
    process.exit(1);
  }

  console.log('Loading embedding model...');
  const extractor = await pipeline('feature-extraction', 'Xenova/all-MiniLM-L6-v2');

  console.log('Loading index...');
  const index = JSON.parse(fs.readFileSync(INDEX_PATH, 'utf8'));

  console.log('Embedding query...');
  const qOut = await extractor(query, { pooling: 'mean', normalize: true });
  const qEmb = Array.from(qOut.data);

  console.log(`Scoring ${index.length} chunks...`);
  const scores = index.map(item => ({ file: item.file, chunk: item.chunk, score: cosine(qEmb, item.embedding) }));
  scores.sort((a, b) => b.score - a.score);

  console.log(`\nTop ${top} results:\n`);
  for (let i = 0; i < Math.min(top, scores.length); i++) {
    const s = scores[i];
    console.log(`[${i+1}] ${s.file} (score: ${s.score.toFixed(4)})`);
    console.log(`    ${s.chunk.slice(0, 200)}${s.chunk.length>200?'...':''}\n`);
  }
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
