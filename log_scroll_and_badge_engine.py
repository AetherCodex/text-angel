
from datetime import datetime
import json
import os

# Badge thresholds
BADGE_RULES = {
    "kindness_10": {"count": 10, "badge": "🌈 Kindness Flame Lv.1"},
    "shielded_25": {"count": 25, "badge": "🛡️ Guardian Angel Lv.2"}
}

# User badge tracker (can be persisted later)
user_stats = {
    "rewrites": 0,
    "shielded_words": 0,
    "badges": []
}

# Create data directory if missing
if not os.path.exists("data"):
    os.makedirs("data")

# === Function: Log to Scroll ===
def log_to_scroll(user, tone, original, rewritten, shielded_count=0):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp} | {user} | Tone: {tone}\nOriginal: {original}\nRewritten: {rewritten}\nShielded Words: {shielded_count}\n\n"

    with open("data/message_log.txt", "a") as f:
        f.write(log_entry)

    # Update user stats
    user_stats["rewrites"] += 1
    user_stats["shielded_words"] += shielded_count
    check_badges()

# === Function: Check and Assign Badges ===
def check_badges():
    for key, rule in BADGE_RULES.items():
        if key not in user_stats["badges"]:
            if key.startswith("kindness") and user_stats["rewrites"] >= rule["count"]:
                user_stats["badges"].append(key)
                print(f"Awarded: {rule['badge']}")
            if key.startswith("shielded") and user_stats["shielded_words"] >= rule["count"]:
                user_stats["badges"].append(key)
                print(f"Awarded: {rule['badge']}")
