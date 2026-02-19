#!/bin/bash
# Torrent-bot-daemon - DEPRECATED (2026-02-19)
# This daemon is no longer needed. Torrent operations are handled by cron and skills.
# Exiting immediately.

echo "[$(TZ=Asia/Bangkok date +'%Y-%m-%d %H:%M')] torrent-bot daemon is deprecated; exiting."
echo "Use aria2 skill and random-torrent-downloader cron instead."
exit 0
