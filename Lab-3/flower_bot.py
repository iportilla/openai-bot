# app_flower_shop_v2.py
import streamlit as st

# Try to import your LLM helper, otherwise fallback mode is used
try:
    from utils import get_answer as llm_get_answer
except Exception:
    llm_get_answer = None

# ---- Page Setup ----
st.set_page_config(page_title="Flower Shop Chatbot", page_icon="🌸")

# ---- System Prompt for BloomBot ----
SYSTEM_PROMPT = """You are BloomBot, a helpful florist assistant for a local flower shop.
Your goal: recommend bouquets/arrangements for occasions (birthday, anniversary, sympathy, wedding, graduation, Valentine's Day, Mother's Day),
respecting budget, flower allergies, color palette, and delivery/pickup timing.
Ask follow-up questions briefly only when necessary.
Offer 2–3 options with short descriptions and approximate prices.
Be warm, concise, and helpful.
"""

# ---- Fallback Answer (used if no LLM available) ----
def fallback_answer(messages):
    user_text = messages[-1]["content"].lower()
    if "birthday" in user_text:
        return "Try a **Bright & Cheerful** bouquet (~$45) with sunflowers and gerbera daisies!"
    elif "anniversary" in user_text:
        return "A **Classic Romance** bouquet (~$65) with 12 red roses is perfect for anniversaries."
    elif "sympathy" in user_text:
        return "A **Peaceful Whites** arrangement (~$60) with lilies and roses conveys sympathy beautifully."
    return "I’d love to help! What’s the **occasion**, **budget**, and **delivery date/zip**?"

def generate_reply(messages):
    # Ensure system prompt is the first message
    if messages[0]["role"] != "system":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages

    if llm_get_answer:
        return llm_get_answer(messages)  # uses your actual LLM
    return fallback_answer(messages)

# ---- Initialize Session State ----
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hi! I’m **BloomBot** 🌸 What’s the occasion and budget?"}
    ]

# ---- Reusable chat send function ----
def send_message(text):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": text})

    # Generate response
    reply = generate_reply(st.session_state.messages)

    # Save assistant response (but do NOT display here)
    st.session_state.messages.append({"role": "assistant", "content": reply})

    # Re-render UI so messages only display once (in the history loop)
    st.rerun()


# ---- UI: Title ----
st.title("🌸 BloomBot — Flower Shop Chatbot")

# ---- UI: Sidebar quick suggestions ----
with st.sidebar:
    st.subheader("Quick Ask")
    if st.button("🎉 Birthday under $50"):
        send_message("I need a birthday bouquet under $50. Bright colors.")
    if st.button("❤️ Anniversary (classic red)"):
        send_message("Anniversary bouquet, classic red roses. Delivery Friday to 80302.")
    if st.button("🕊️ Sympathy whites"):
        send_message("Sympathy arrangement in whites. Service on Tuesday.")
    st.markdown("---")
    st.caption("Tip: Mention occasion, budget, colors, allergies, delivery date & zip.")

# ---- Render chat history (skip system message) ----
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message(m["role"]):
        st.write(m["content"])

# ---- User chat input ----
user_text = st.chat_input("Tell me the occasion & budget…")
if user_text:
    send_message(user_text)