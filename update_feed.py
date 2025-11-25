#!/usr/bin/env python3
"""
update_feed.py — Daily Weaver for Eternal Ledger
Daniel H. Fingal — Open-Source MIT — November 25 2025
Pulls last 5 ideas from local vault → Updates public feed.
Graceful: mkdir VAULT, seed holds if empty, deterministic append (no false deltas).
"""

import json
import os
from datetime import datetime
from pathlib import Path

REPO_DIR = Path(__file__).parent
FEED = REPO_DIR / "ETERNAL_FEED.txt"
VAULT = Path.home() / ".eternal_write" / "public_vault"

# Graceful: Ensure VAULT exists — like ew.py mkdir (deterministic, no fail)
VAULT.mkdir(parents=True, exist_ok=True)

def update():
    now = datetime.utcnow()
    entries = sorted(VAULT.glob("*.json"))[-5:]  # Last 5 for preview — deterministic glob

    lines = [
        "ETERNAL WRITE — PUBLIC FIRST-THOUGHT LEDGER",
        "Daniel H. Fingal (@danielhfingal)",
        f"Started: 2024-11-23 | First entry Bitcoin-timestamped",
        f"Last update: {now.strftime('%Y-%m-%d %H:%M')} UTC",
        "",
        "=== 2024-11-23 19:42:11Z ===",
        "First thought provenance must be public, automatic, and cryptographically unbreakable.",
        "",
        "=== 2025-11-25 03:35:00Z ===",
        "The silence before the world notices. The ledger is complete. It is beautiful. It is mine.",
        "",
    ]

    # Append recent entries if any (graceful json.load — skip invalid)
    new_threads = 0
    for entry_path in entries:
        try:
            with open(entry_path) as ef:
                data = json.load(ef)
            lines.extend([
                f"=== {data['timestamp_utc']} ===",
                f"{data['idea']}",
                ""
            ])
            new_threads += 1
        except (json.JSONDecodeError, KeyError, IOError) as e:
            print(f"Skip invalid entry {entry_path}: {e}")  # Log graceful, no crash
            continue

    lines.extend([
        f"\nMore entries appear daily at 03:35 UTC — forever.",
        f"Raw feed: https://raw.githubusercontent.com/danielhfingal/eternal-proofs/main/ETERNAL_FEED.txt"
    ])

    # Deterministic write — like orjson in tesla-powerwall-fingal (no false deltas)
    new_feed = "\n".join(lines)
    try:
        if FEED.read_text() != new_feed:  # Diff check pre-write
            with open(FEED, "w") as f:
                f.write(new_feed)
            print(f"ETERNAL_FEED.txt updated — {new_threads} new threads woven")
        else:
            print("No weave needed — ledger unchanged")
    except IOError as e:
        print(f"Write failed: {e}")  # Graceful log

if __name__ == "__main__":
    update()
