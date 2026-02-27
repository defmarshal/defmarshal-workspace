#!/usr/bin/env node
// git-ys — friendly git status check
const { execSync } = require('child_process');
try {
  const out = execSync('git status --short', { encoding: 'utf8' });
  const files = out.trim().split('\n').filter(Boolean);
  if (files.length === 0) {
    console.log('✅ All clear! Git workspace clean.');
  } else {
    console.log(`⚠️  ${files.length} changes:`);
    files.forEach(f => console.log(`  ${f}`));
  }
} catch (e) {
  console.error('Error running git status:', e.message);
  process.exit(1);
}
