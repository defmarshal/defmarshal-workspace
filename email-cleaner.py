#!/usr/bin/env python3
"""
Email Auto-Cleaner for Gmail via Maton API.
Fetches inbox messages, applies rules to detect useless emails, and archives them.
Also can apply labels (e.g., group welcome emails).
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
    "label_rules": [
        {"keyword": "welcome", "label": "WELCOME"}
    ],
    "max_age_days": 30,
    "skip_starred": True,
    "skip_important": True
}

def list_messages(max_results=100, query=None):
    params = {"maxResults": max_results}
    if query:
        params["q"] = query
    url = f"{GATEWAY}/gmail/v1/users/me/messages"
    resp = requests.get(url, headers=HEADERS, params=params)
    resp.raise_for_status()
    data = resp.json()
    return [m["id"] for m in data.get("messages", [])]

def get_message_details(msg_id):
    url = f"{GATEWAY}/gmail/v1/users/me/messages/{msg_id}?format=metadata&metadataHeaders=From&metadataHeaders=Subject&metadataHeaders=Date&metadataHeaders=LabelIds"
    resp = requests.get(url, headers=HEADERS)
    resp.raise_for_status()
    return resp.json()

def should_archive(msg: Dict) -> bool:
    labels = msg.get("labelIds", [])
    snippet = msg.get("snippet", "").lower()
    headers = msg.get("payload", {}).get("headers", [])

    if RULES["skip_starred"] and "STARRED" in labels:
        return False
    if RULES["skip_important"] and "IMPORTANT" in labels:
        return False

    # Category labels
    for cat in RULES["gmail_labels"]:
        if cat in labels:
            return True

    # Sender patterns
    from_hdr = next((h["value"] for h in headers if h["name"].lower() == "from"), "")
    if from_hdr:
        for pattern in RULES["promotional_senders"]:
            if pattern in from_hdr.lower():
                return True

    # Spammy keywords in snippet
    for kw in RULES["spammy_keywords"]:
        if kw in snippet:
            return True

    return False

def should_label(msg: Dict) -> str or None:
    """Return label to apply if any, else None."""
    headers = msg.get("payload", {}).get("headers", [])
    subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "").lower()
    snippet = msg.get("snippet", "").lower()
    for rule in RULES.get("label_rules", []):
        kw = rule["keyword"].lower()
        label = rule["label"]
        if kw in subject or kw in snippet:
            return label
    return None

def modify_message(msg_id, remove_inbox=False, add_label=None):
    url = f"{GATEWAY}/gmail/v1/users/me/messages/{msg_id}/modify"
    payload = {}
    if remove_inbox:
        payload["removeLabelIds"] = ["INBOX"]
    if add_label:
        payload["addLabelIds"] = [add_label]
    if not payload:
        return False
    resp = requests.post(url, headers=HEADERS, json=payload)
    return resp.status_code == 200

def main():
    parser = argparse.ArgumentParser(description="Auto-clean Gmail inbox by archiving promotional emails and applying labels.")
    parser.add_argument("--execute", action="store_true", help="Actually modify messages (dry-run by default)")
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
    to_label = {}  # msg_id -> label
    skipped = []

    for msg_id in ids:
        try:
            msg = get_message_details(msg_id)
            acted = False
            if should_archive(msg):
                to_archive.append(msg_id)
                acted = True
            label = should_label(msg)
            if label:
                to_label[msg_id] = label
                acted = True
            if not acted:
                skipped.append(msg_id)
        except Exception as e:
            print(f"Error processing {msg_id}: {e}")
            skipped.append(msg_id)

    print(f"\nDry-run results:")
    print(f"  Would archive: {len(to_archive)}")
    print(f"  Would label: {len(to_label)}")
    print(f"  Would keep untouched: {len(skipped)}")

    if args.execute and (to_archive or to_label):
        confirm = input("Proceed with modifications? (yes/no): ").strip().lower()
        if confirm != "yes":
            print("Aborted.")
            sys.exit(0)
        archived = 0
        labeled = 0
        # Process archive+label combined
        all_msg_ids = set(to_archive) | set(to_label.keys())
        for msg_id in all_msg_ids:
            try:
                remove_inbox = msg_id in to_archive
                add_label = to_label.get(msg_id)
                if modify_message(msg_id, remove_inbox=remove_inbox, add_label=add_label):
                    if remove_inbox:
                        archived += 1
                    if add_label:
                        labeled += 1
            except Exception as e:
                print(f"Error modifying {msg_id}: {e}")
        print(f"\nModifications complete:")
        if archived:
            print(f"  Archived: {archived}")
        if labeled:
            print(f"  Labeled: {labeled}")
        # Log summary
        log_entry = f"[{datetime.datetime.utcnow().isoformat()}] Cleaned: archived={archived}, labeled={labeled}, examined={len(ids)}"
        with open("memory/email-cleaner.log", "a") as f:
            f.write(log_entry + "\n")
    elif args.execute:
        print("No messages to modify.")

if __name__ == "__main__":
    main()
