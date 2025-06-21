import streamlit as st
import json
import re
import os
import openai

from log_scroll_and_badge_engine import log_to_scroll
from profile_system import (
    load_user_profile,
    update_profile_field,
    get_tone_default,
    add_badge
)

# --- CONFIG ---
st.set_page_config(page_title="TEXT ANGEL Unified", layout="centered")
openai.api_key = st.secrets["OPENAI_API_KEY"]  # ✅ Loads API key from .streamlit/secrets.toml

# --- Load Profile ---
user_profile = load_user_profile()
username = user_profile["username"]
guardian = user_profile["guardian_name"]
avatar = user_profile["avatar"]
tone_default = get_tone_default()

# --- Sidebar Profile UI ---
st.sidebar.header(f"{avatar} Welcome, {username}!")
st.sidebar.markdown(f"**Guardian Angel:** {guardian}")
selected_default = st.sidebar.selectbox(
    "Choose your default tone",
    ["GRACE", "TRUTH", "CALM"],
    index=["GRACE", "TRUTH", "CALM"].index(tone_default),
    key="tone_selector"
)

# --- Load Shield Words ---
shield_path = "shield_filter_words.json"
with open(shield_path, "r") as f:
    shield_words = json.load(f)

# --- Helper: Shield/Censor ---
def censor_message(message, shield_list):
    blocked_count = 0
    censored_message = message
    for word in shield_list:
        word_pattern = re.compile(r'\b' + re.escape(word) + r'\b', flags=re.IGNORECASE)
        if word_pattern.search(censored_message):
            blocked_count += len(word_pattern.findall(censored_message))
            censored_message = word_pattern.sub("▆▆▆", censored_message)
    return censored_message, blocked_count

# --- Helper: Rewrite with Tone via GPT ---
def rewrite_with_tone(message, tone):
    prompt_map = {
        "GRACE": "Rewrite this to be kind, nurturing, and soft:",
        "TRUTH": "Rewrite this to be honest and respectful:",
        "CALM": "Rewrite this to be peaceful, grounded, and emotionally safe:"
    }
    prompt_text = prompt_map.get(tone, "Rewrite this message with empathy.")
    full_prompt = f"{prompt_text}\n\nOriginal: {message}"

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a message tone transformer."},
            {"role": "user", "content": full_prompt}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

# === STREAMLIT MAIN INTERFACE ===

st.title("😇 TEXT ANGEL – Unified Guardian Mode")

# --- Outgoing Rewrite ---
st.header("📝 Rewrite a Message")
tone = st.selectbox("Choose a tone:", ["GRACE", "TRUTH", "CALM"], index=["GRACE", "TRUTH", "CALM"].index(tone_default))
user_message = st.text_area("What do you want to say?", key="rewrite")

if user_message:
    rewritten = rewrite_with_tone(user_message, tone)
    st.success(f"✅ Message rewritten with {tone}:")
    st.markdown(f"**Output:**\n\n{rewritten}")
    log_to_scroll(user=username, tone=tone, original=user_message, rewritten=rewritten, shielded_count=0)

st.divider()

# --- Incoming Message Shield ---
st.header("🛡️ Shield an Incoming Message")
incoming_message = st.text_area("📥 Paste the message you received:", height=200, key="incoming")

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
    else:
        st.success("✅ This message contains no harmful words.")

    log_to_scroll(user=username, tone="SHIELD", original=incoming_message, rewritten=censored, shielded_count=blocked_count)
