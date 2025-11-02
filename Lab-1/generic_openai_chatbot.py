# simple_openai_chat_env.py
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os

# Installation reminders:
# pip install openai python-dotenv streamlit

# --- Load environment variables ---
load_dotenv()
API_KEY = os.getenv("openai_api_key")

# --- Setup client ---
if not API_KEY:
    st.error("Missing openai_api_key in .env file.")
else:
    client = OpenAI(api_key=API_KEY)

SYSTEM_PROMPT = "You are a concise and friendly assistant."

# --- Streamlit UI ---
st.set_page_config(page_title="Simple Chat (OpenAI + .env)", page_icon="💬")
st.title("💬 Simple OpenAI Chatbot")

# --- Input ---
user_input = st.chat_input("Type your message...")

if user_input and API_KEY:
    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_input},
                    ],
                    temperature=0.7,
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"Error: {e}"
        st.write(reply)