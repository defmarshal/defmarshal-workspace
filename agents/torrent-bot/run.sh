#!/usr/bin/env bash
# Torrent-bot script - DEPRECATED (2026-02-19)
# The 'openclaw agents spawn' command is no longer supported.
# Torrent management is now handled by:
#  - aria2 skill (automatic handling of magnet/torrent files)
#  - random-torrent-downloader cron job (automated additions)
#  - quick commands: torrent-add, nyaa-search, nyaa-top, downloads
#
# This script is kept for reference but will not function.

echo "ERROR: torrent-bot is deprecated and non-functional."
echo "Use aria2 skill for manual torrent additions or wait for automated cron."
echo "To manually add a torrent: ./quick torrent-add <magnet>"
exit 1
