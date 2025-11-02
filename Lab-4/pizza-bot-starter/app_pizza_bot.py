import streamlit as st

# TODO: Replace this system prompt to define PizzaBot's personality
SYSTEM_PROMPT = """You are PizzaBot. (You will customize this.)"""

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hi! I'm PizzaBot 🍕 How can I help you today?"}
    ]

st.title("🍕 PizzaBot (Starter Version)")

# TODO: Add quick action sidebar buttons for pizza suggestions
with st.sidebar:
    st.subheader("Quick Ask (To Implement)")
    st.caption("Example: Pepperoni, Veggie, Spicy, Party Order")

# TODO: Add fallback or LLM call here
def generate_reply(messages):
    return "TODO: Add pizza recommendations here!"

# Render conversation history
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.write(m["content"])

# Chat input
user_text = st.chat_input("What kind of pizza are you thinking about?")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    reply = generate_reply(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.experimental_rerun()
