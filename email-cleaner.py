#!/usr/bin/env python3
"""
Email Auto-Cleaner for Gmail via Maton API.
Fetches inbox messages, applies rules to detect useless emails, and archives them.
Dry-run by default. Use --execute to actually modify.
"""

import os, sys, json, requests, argparse, datetime
from typing import List, Dict

# Config
MATON_API_KEY = os.getenv("MATON_API_KEY")
CONNECTION_ID = os.getenv("MATON_CONNECTION")  # optional
GATEWAY = "https://gateway.maton.ai/google-mail"

HEADERS = {
    "Authorization": f"Bearer {MATON_API_KEY}",
    "Content-Type": "application/json"
}
if CONNECTION_ID:
    HEADERS["Maton-Connection"] = CONNECTION_ID

# Rules: customize these
RULES = {
    "promotional_senders": [
        "@promotions.", "@news.", "@mail.", "@newsletter", "@digest", "@updates", "@noreply", "@no-reply"
    ],
    "spammy_keywords": [
        "sale", "discount", "offer", "deal", "limited time", "act now", "free trial",
        "subscribe", "unsubscribe", "newsletter", "promotion", "marketing", "advert",
        "earn money", "make money", "get rich", "click here", "congratulations", "winner"
    ],
    "gmail_labels": ["CATEGORY_PROMOTIONS", "CATEGORY_UPDATES"],
    "max_age_days": 30,  # older than this get archived even if not matching other rules
    "skip_starred": True,
    "skip_important": True  # emails with 'important' label
}

def list_messages(max_results=100, query=None):
    """Return list of message IDs from inbox."""
    params = {"maxResults": max_results}
    if query:
        params["q"] = query
    url = f"{GATEWAY}/gmail/v1/users/me/messages"
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    return [m["id"] for m in data.get("messages", [])]

def get_message_details(msg_id):
    """Return message details (headers, labels, snippet)."""
    url = f"{GATEWAY}/gmail/v1/users/me/messages/{msg_id}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def should_archive(msg: Dict) -> bool:
    """Apply rules to decide if message should be archived."""
    labels = msg.get("labelIds", [])
    snippet = msg.get("snippet", "").lower()
    headers = msg.get("payload", {}).get("headers", [])

    # Skip starred/important
    if RULES["skip_starred"] and "STARRED" in labels:
        return False
    if RULES["skip_important"] and "IMPORTANT" in labels:
        return False

    # Check Gmail category labels
    for cat in RULES["gmail_labels"]:
        if cat in labels:
            return True

    # Check sender domain
    from_hdr = next((h["value"] for h in headers if h["name"].lower() == "from"), "")
    if from_hdr:
        for pattern in RULES["promotional_senders"]:
            if pattern in from_hdr.lower():
                return True

    # Check subject/snippet keywords (avoid false positives on important words)
    for kw in RULES["spammy_keywords"]:
        if kw in snippet:
            return True

    # Age-based: if older than max_age_days and not in inbox? Actually we only fetch inbox, so age check is optional.
    # We could fetch internalDate and compare, but skip for now to keep rule simple.

    return False

def archive_message(msg_id):
    """Delete (archive) a message from inbox (move to trash or use modify to remove INBOX)."""
    # Option 1: trash (moves to Trash label)
    # url = f"{GATEWAY}/gmail/v1/users/me/messages/{msg_id}/trash"
    # resp = requests.post(url, headers=HEADERS)

    # Option 2: modify to remove INBOX label (archive)
    url = f"{GATEWAY}/gmail/v1/users/me/messages/{msg_id}/modify"
    payload = {"removeLabelIds": ["INBOX"]}
    resp = requests.post(url, headers=HEADERS, json=payload)
    if resp.status_code == 200:
        return True
    else:
        print(f"Failed to archive {msg_id}: {resp.status_code} {resp.text}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Auto-clean Gmail inbox by archiving promotional emails.")
    parser.add_argument("--execute", action="store_true", help="Actually archive messages (default is dry-run)")
    parser.add_argument("--max", type=int, default=100, help="Maximum number of messages to process")
    parser.add_argument("--query", type=str, default=None, help="Additional Gmail query filter")
    args = parser.parse_args()

    if not MATON_API_KEY:
        print("Error: MATON_API_KEY environment variable not set.")
        sys.exit(1)

    print(f"Fetching up to {args.max} messages from inbox...")
    try:
        ids = list_messages(max_results=args.max, query=args.query)
    except requests.HTTPError as e:
        print(f"Failed to fetch messages: {e}")
        sys.exit(1)

    print(f"Found {len(ids)} messages.")
    to_archive = []
    skipped = []

    for msg_id in ids:
        try:
            msg = get_message_details(msg_id)
            if should_archive(msg):
                to_archive.append(msg_id)
            else:
                skipped.append(msg_id)
        except Exception as e:
            print(f"Error processing {msg_id}: {e}")
            skipped.append(msg_id)  # don't risk it

    print(f"\nDry-run results:")
    print(f"  Would archive: {len(to_archive)}")
    print(f"  Would keep: {len(skipped)}")

    if args.execute and to_archive:
        confirm = input("Proceed with archiving? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Aborted.")
            sys.exit(0)
        archived = 0
        for msg_id in to_archive:
            try:
                if archive_message(msg_id):
                    archived += 1
            except Exception as e:
                print(f"Error archiving {msg_id}: {e}")
        print(f"\nArchived {archived}/{len(to_archive)} messages.")
        # Log summary
        log_entry = f"[{datetime.datetime.utcnow().isoformat()}] Archived {archived} emails (total examined: {len(ids)})"
        with open("memory/email-cleaner.log", "a") as f:
            f.write(log_entry + "\n")
    elif args.execute:
        print("No messages to archive.")

if __name__ == "__main__":
    main()
