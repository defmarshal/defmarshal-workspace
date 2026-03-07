---
name: gmail-fast
description: |
  Fast Gmail integration using Maton API. Retrieves recent messages with headers (from, subject, date).
  Optimized for speed: uses parallel fetching with concurrency control.
usage:
  - Fetch 10 recent emails: gmailFast.recent(10)
  - Fetch 20: gmailFast.recent(20)
  - Returns JSON array: [{from, subject, date, snippet, messageId}]
requirements:
  env:
    - MATON_API_KEY
    - CONNECTION_ID
---