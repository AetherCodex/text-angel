
import json
import os

# File to store user profiles
PROFILE_PATH = "data/user_profile.json"

# Default structure
default_profile = {
    "username": "Jagger",
    "guardian_name": "Seraphiel",
    "avatar": "🧒",
    "tone_default": "GRACE",
    "badges": [],
    "sensitivity": 5
}

# Load or initialize profile
def load_user_profile():
    if os.path.exists(PROFILE_PATH):
        with open(PROFILE_PATH, "r") as f:
            return json.load(f)
    else:
        save_user_profile(default_profile)
        return default_profile

# Save profile to file
def save_user_profile(profile):
    with open(PROFILE_PATH, "w") as f:
        json.dump(profile, f, indent=2)

# Update individual profile fields
def update_profile_field(field, value):
    profile = load_user_profile()
    profile[field] = value
    save_user_profile(profile)

# Add badge if not already present
def add_badge(badge):
    profile = load_user_profile()
    if badge not in profile["badges"]:
        profile["badges"].append(badge)
        save_user_profile(profile)

# Example: get tone default
def get_tone_default():
    profile = load_user_profile()
    return profile.get("tone_default", "GRACE")
