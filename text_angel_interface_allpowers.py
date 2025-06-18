import streamlit as st
import openai
import os
import json
from datetime import datetime
import re
import uuid

# --- CONFIG --- #
SOUND_FILE = "https://actions.google.com/sounds/v1/cartoon/clang_and_wobble.ogg"
LOG_PATH = "user_interface/data/message_log.txt"
SHIELD_WORDS_PATH = os.path.join(os.path.dirname(__file__), "..", "shield_filter", "shield_filter_words.json")

# --- SETUP --- #
st.set_page_config(page_title="TEXT ANGEL", page_icon="😇")
st.title("😇 TEXT ANGEL")
st.subheader("Fix your message with Grace, Truth, or Calm.")

# --- Load Shield Words --- #
try:
    with open(SHIELD_WORDS_PATH) as f:
        shield_words = json.load(f)
except FileNotFoundError:
    shield_words = []
    st.warning("Shield words file not found. Running without filter.")

# --- Tone Prompts --- #
tone_prompts = {
    "GRACE": "Rewrite the following message with kindness, care, and gentleness.",
    "TRUTH": "Rewrite the following message to be honest, clear, and respectful.",
    "CALM": "Rewrite the following message in a peaceful and soft tone, with no harshness."
}
tone_styles = {
    "GRACE": {"color": "#FFF9E6", "emoji": "💛"},
    "TRUTH": {"color": "#E6F0FF", "emoji": "💙"},
    "CALM": {"color": "#E6FFF0", "emoji": "💚"}
}

# --- User Profile --- #
st.markdown("### 👤 Your Profile")
username = st.text_input("Name your Guardian Angel (just for fun):", value="Seraphiel")
reminder = st.text_input("Reminder before sending:", value="Speak like an angel")
sensitivity = st.slider("Auto-Filter Sensitivity", 0, 10, value=7)

st.markdown("---")

# --- Input UI --- #
message = st.text_area("📨 Type your message:")
tone = st.selectbox("🧭 Choose an Angel Tone for this message:", ["GRACE", "TRUTH", "CALM"])
submit = st.button("🕊️ Angel Edit")

# --- Censorship Filter --- #
def censor_message(message, blocked_words):
    count = 0
    censored = message
    for word in blocked_words:
        pattern = r"\b" + re.escape(word) + r"\b"
        matches = re.findall(pattern, censored, flags=re.IGNORECASE)
        if matches:
            count += len(matches)
            censored = re.sub(pattern, "▆▆▆", censored, flags=re.IGNORECASE)
    return censored, count

# --- Logging --- #
def log_message(user, tone, original, rewritten):
    os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(f"[{datetime.now()}] {user} | Tone: {tone}\nOriginal: {original}\nRewritten: {rewritten}\n\n")

# --- PROCESSING --- #
if submit and message:
    st.caption(f"🧘 {reminder}")
    censored_message, shield_count = censor_message(message, shield_words)

    with st.spinner("Calling your angel..."):
        try:
            prompt = f"{tone_prompts[tone]} {censored_message}"
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a kind and emotionally intelligent assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            rewritten = response["choices"][0]["message"]["content"]
            style = tone_styles[tone]

            st.success("✅ Your message has been filtered!")
            st.audio(SOUND_FILE)

            # Rewritten Output
            st.markdown(f"""
                <div style='background-color: {style["color"]}; padding: 1em; border-radius: 10px;'>
                    <b>{style["emoji"]} Here's your message rewritten with {tone.title()}:</b><br><br>
                    <i>{rewritten}</i>
                </div>
            """, unsafe_allow_html=True)

            # Shield Alert
            if shield_count > 0:
                st.markdown(f"⚠️ <i>{shield_count} word{'s' if shield_count > 1 else ''} were shielded by TEXT ANGEL.</i>", unsafe_allow_html=True)

            # Log
            log_message(username, tone, message, rewritten)

        except Exception as e:
            st.error(f"Error: {e}")
