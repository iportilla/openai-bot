import streamlit as st
import re

st.set_page_config(page_title="🍕 Pizza Shop Chatbot", page_icon="🍕")

# ---------------- Session State ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! Welcome to **PizzaTime** 🍕 What kind of pizza would you like today?"}
    ]

if "order_details" not in st.session_state:
    st.session_state.order_details = {
        "type": None,
        "size": None,
        "crust": None,
        "pickup_delivery": None,
        "time": None
    }

if "order_ready" not in st.session_state:
    st.session_state.order_ready = False

if "conversation_complete" not in st.session_state:
    st.session_state.conversation_complete = False


# ---------------- Receipt UI ----------------
def render_receipt(order):
    st.markdown("""
    <style>
    .receipt-box {
        border: 2px solid #444;
        padding: 14px;
        border-radius: 8px;
        width: 380px;
        background: #fafafa;
        font-family: monospace;
        margin-top: 10px;
    }
    .receipt-title {
        font-weight: bold;
        text-align: center;
        margin-bottom: 8px;
    }
    .receipt-line {
        border-bottom: 1px dashed #777;
        margin: 6px 0;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="receipt-box">
        <div class="receipt-title">🍕 PIZZA ORDER RECEIPT 🍕</div>
        <div>Pizza: <strong>{order['type']}</strong></div>
        <div>Size: <strong>{order['size'].title()}</strong></div>
        <div>Crust: <strong>{order['crust'].title()}</strong></div>
        <div class="receipt-line"></div>
        <div>Pickup/Delivery: <strong>{order['pickup_delivery'].title()}</strong></div>
        <div>Time: <strong>{order['time']}</strong></div>
        <div class="receipt-line"></div>
        <div style="text-align:center;">Thank you for your order! 😊</div>
    </div>
    """, unsafe_allow_html=True)


# ---------------- Order Logic ----------------
def fallback_answer(messages):
    last = messages[-1]["content"].lower()
    o = st.session_state.order_details

    # ✅ If order is finished, do not ask for pizza again
    if st.session_state.conversation_complete:
        return "If you need anything else later, I'm here! 🍕"

    # Pizza type
    if o["type"] is None:
        if "pepperoni" in last:
            o["type"] = "Classic Pepperoni"
        elif "veggie" in last or "vegetarian" in last:
            o["type"] = "Veggie Delight"
        elif "spicy" in last:
            o["type"] = "Spicy Diablo"
        elif "cheese" in last or "margherita" in last or "plain" in last:
            o["type"] = "Classic Cheese"

        if o["type"] is not None:
            return "Great! What size would you like? (Small / Medium / Large)"

    # Size
    if o["size"] is None:
        m = re.search(r"\b(small|medium|large|s|m|l)\b", last)
        if m:
            o["size"] = {"s": "small", "m": "medium", "l": "large"}.get(m.group(), m.group())
            return "Nice — and what crust would you like? (Thin / Regular / Pan)"

    # Crust
    if o["crust"] is None:
        m = re.search(r"\b(thin|regular|pan|deep dish|stuffed)\b", last)
        if m:
            o["crust"] = m.group()
            return "Got it — pickup or delivery?"

    # Pickup / Delivery
    if o["pickup_delivery"] is None:
        if "pickup" in last or "pick up" in last:
            o["pickup_delivery"] = "pickup"
            return "What time should it be ready?"
        if "delivery" in last:
            o["pickup_delivery"] = "delivery"
            return "What time should we deliver it?"

    # Time
    if o["time"] is None:
        m = re.search(r"\b(\d{1,2}(:\d{2})?\s*(am|pm)?)\b", last)
        if m:
            o["time"] = m.group()
            st.session_state.order_ready = True
            return "✅ I have everything I need! Say **confirm** to place your order."

    # Waiting for confirm
    if st.session_state.order_ready:
        return "Say **confirm** when you're ready to place your order 😊"

    # ✅ Improved fallback
    return "Got it — what kind of pizza would you like? (Pepperoni / Veggie / Spicy / Cheese)"


# ---------------- Confirmation & Closing ----------------
def check_close():
    last = st.session_state.messages[-1]["content"].lower()

    # Confirm order
    if st.session_state.order_ready and "confirm" in last:
        st.session_state.order_ready = False
        st.session_state.conversation_complete = True
        st.session_state.messages.append({
            "role": "assistant",
            "content": "🎉 Order confirmed! Would you like anything else?"
        })
        return

    # End conversation & show receipt
    if st.session_state.conversation_complete and last in ["no", "no thanks", "no thank you", "that's all", "done"]:
        o = st.session_state.order_details
        st.session_state.messages.append({"role": "assistant", "content": "😊 Thank you! Here's your order summary:"})
        with st.chat_message("assistant"):
            render_receipt(o)
        st.session_state.messages.append({"role": "assistant", "content": "Have a great day! 🍕"})


# ---------------- UI Rendering ----------------
st.title("🍕 PizzaTime Chatbot")

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

user_input = st.chat_input("Your message...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("assistant"):
        reply = fallback_answer(st.session_state.messages)
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})
    check_close()