#!/usr/bin/env node
// Add check-quick-commands to quick launcher
const fs = require('fs');
const path = '/home/ubuntu/.openclaw/workspace/quick';

let s = fs.readFileSync(path, 'utf8');

// 1) Add to help: after 'gateway-fix' line
s = s.replace(/^(  gateway-fix\s+Fix gateway issues.*)$/m, `$1\n  check-quick-commands  Sanity-check core quick commands (dry-run)`);

// 2) Add case: after 'gateway-fix)' case block
s = s.replace(/(  gateway-fix\)\n[\s\S]*?;;\n)/, `$1  check-quick-commands)\n    bash "$WORKSPACE/scripts/quick-check-commands.sh"\n    ;;\n`);

fs.writeFileSync(path, s, 'utf8');
console.log('Updated quick with check-quick-commands');
