#!/bin/bash
# Re-enable all OpenClaw cron jobs except notifier-cron
# Called by scheduled re-enablement after housekeeping

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORKSPACE="$(dirname "$SCRIPT_DIR")"
cd "$WORKSPACE" || exit 1

echo "[$(date -Iseconds)] Re-enabling cron jobs (except notifier)..." >> memory/auto-reenable.log

# All OpenClaw cron job IDs to re-enable (27 total, excluding notifier-cron)
ALL_IDS="
e26c12bd-635a-48cf-bc8d-1707bc4ffd59
48a38fe2-9691-4bea-bed1-0f3313534fcd
e345525c-f289-4eab-bf25-6d6fa065e4b0
f69140f6-7341-4217-bad3-f4a9615b0b94
9112eca8-0ccb-4db4-b016-e5841fa9ef30
4e9eb829-fcfd-4cb4-8139-44c299f7679a
3291b8d1-cf95-4fed-8292-8dc724c38ae3
aadf040b-60d2-48ee-9825-0db68bb6c13b
23788edb-575a-4593-a60e-7f94b9c95db6
86722825-c37c-4b96-a838-15cf224328e7
a27a9b33-e501-4ad2-97f5-2c02b05a743a
5d3597fc-6376-4cda-881a-0a1df677df87
6a1b4266-2a3d-4645-90a1-e07cde656b41
65f0d1f3-548c-4c4e-9215-241df8c67b95
23dad379-21ad-4f7a-8c68-528f98203a33
6e5621c3-783a-416c-93c7-56ea2cb4e920
16af6af1-b6e0-4435-91ba-15f7d04c0207
483e96ab-0837-4e5c-9086-a560635188af
dada350a-4508-4358-8ac6-35f10e91cdd0
c6976c90-df08-4ac2-997a-a4a53be6c23c
b84b1f5c-7027-49f3-b9da-799721ecec21
c6bca31f-9459-4cc7-a8dd-d35b268506e0
fb670b4f-717a-4a14-85e6-6ece389c8b61
d5c6f526-52d7-4786-8dc0-4efff1f4e36b
6e4f5697-c2cc-48cb-91bb-0c4edcc19c46
db19ad80-e15c-46d6-af15-8815366d638c
6e07b8d1-c443-4a9f-a95e-665e47f29e52
"

for id in $ALL_IDS; do
  openclaw cron enable "$id" && echo "Enabled: $id" || echo "Failed: $id"
done >> memory/auto-reenable.log 2>&1

# Restart systems
echo "Restarting meta-supervisor daemon..." >> memory/auto-reenable.log
nohup bash -c 'cd "$WORKSPACE" && agents/meta-supervisor/meta-supervisor-daemon.sh > agents/meta-supervisor/meta-supervisor.nohup 2>&1' &
sleep 2
echo "Daemon started" >> memory/auto-reenable.log

echo "[$(date -Iseconds)] Re-enable complete." >> memory/auto-reenable.log
echo "NOTIFIER_CRON_STILL_DISABLED=true" >> memory/auto-reenable.log
