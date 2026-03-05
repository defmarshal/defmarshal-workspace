#!/usr/bin/env bash
# Log-only version for debugging
echo "$(date -u '+%Y-%m-%d %H:%M:%S UTC') - supervisor.sh invoked by $$" >> /tmp/supervisor_invocations.log
exit 0
