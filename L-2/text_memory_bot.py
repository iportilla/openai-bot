# app_text_chat.py
import streamlit as st
from utils import get_answer  # expects a function that accepts st.session_state.messages

# --- Session state ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! How may I assist you today?"}
    ]

st.set_page_config(page_title="Text Chatbot", page_icon="💬")
st.title("OpenAI Conversational Chatbot (Text Only)")

# Optional: clear chat
with st.sidebar:
    if st.button("🧹 Clear conversation"):
        st.session_state.messages = [
            {"role": "assistant", "content": "Chat cleared. How can I help?"}
        ]
        st.experimental_rerun()

# Render history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Input box (text only)
user_input = st.chat_input("Type your message…")

if user_input:
    # Append user message and render immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking…"):
            reply = get_answer(st.session_state.messages)
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})