
import streamlit as st
import json
import re
from pathlib import Path

# Load shield words from JSON
shield_path = "shield_filter_words.json"
with open(shield_path, "r") as f:
    shield_words = json.load(f)

# Define censor logic
def censor_message(message, shield_list):
    blocked_count = 0
    censored_message = message
    for word in shield_list:
        word_pattern = re.compile(r'\b' + re.escape(word) + r'\b', flags=re.IGNORECASE)
        if word_pattern.search(censored_message):
            blocked_count += len(word_pattern.findall(censored_message))
            censored_message = word_pattern.sub("▆▆▆", censored_message)
    return censored_message, blocked_count

# Streamlit UI
st.set_page_config(page_title="TEXT ANGEL | Incoming Shield", layout="centered")
st.title("🛡️ TEXT ANGEL – Incoming Message Guardian")
st.markdown("Protecting your heart from harmful words.")

# Guardian identity (can later be part of profile config)
guardian = "Seraphiel"

# Input
incoming_message = st.text_area("📥 Paste the message you received:", height=200)

# Shield processing
if incoming_message:
    censored, blocked_count = censor_message(incoming_message, shield_words)

    if blocked_count > 0:
        st.error("⚠️ This message was shielded by TEXT ANGEL.")
        st.markdown(f'''
        <div style='background-color:#FFF0F0; padding:1em; border-radius:10px; border: 1px solid red;'>
            📯 <b>Shielded Message:</b><br>
            <i>{censored}</i><br><br>
            <b>{blocked_count} word{'s' if blocked_count > 1 else ''} were shielded.</b><br>
            <b>🕊️ Guardian: {guardian}</b>
        </div>
        ''', unsafe_allow_html=True)

    #    st.audio("assets/sounds/clang_and_wobble.ogg", format="audio/ogg")

    else:
        st.success("✅ This message contains no harmful words.")

