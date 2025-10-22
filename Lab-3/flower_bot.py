# app_flower_shop_v2.py
import streamlit as st

# Optional: use your LLM util if available
try:
    from utils import get_answer as llm_get_answer
except Exception:
    llm_get_answer = None

st.set_page_config(page_title="Flower Shop Chatbot", page_icon="🌸")

# ---------------- System prompt specialized for a florist ----------------
SYSTEM_PROMPT = """You are BloomBot, a helpful florist assistant for a local flower shop.
Your goal: recommend bouquets/arrangements for occasions (birthday, anniversary, sympathy, wedding, graduation, Valentine's Day, Mother's Day),
respecting budget, color palette, flower preferences, allergies (e.g., pollen-sensitive), and delivery/pickup timing.
Ask brief, targeted follow-ups ONLY when needed: occasion, recipient relationship, budget range, color/theme, size, delivery date/time, address/zip.
Offer 2–3 options at different price points with short descriptions and stems (e.g., roses, lilies) and care tips if asked.
Be warm, concise, and practical. If out of scope, redirect kindly. Prices are estimates unless provided.
Format: bullets for options; bold key items; keep replies under ~8 sentences unless the user asks for details."""

# ---------------- Minimal fallback if no LLM is wired ----------------
def fallback_answer(messages):
    """Very tiny rule-based demo so the app runs without external APIs."""
    last = next((m["content"] for m in reversed(messages) if m["role"] == "user"), "").lower()
    occasion = "anniversary" if "anniversary" in last else \
               "birthday" if "birthday" in last else \
               "sympathy" if "sympathy" in last else \
               "wedding" if "wedding" in last else \
               "graduation" if "graduation" in last else \
               "valentine" if "valentine" in last else "special occasion"

    recs = {
        "anniversary": [
            ("**Classic Romance** (~$65)", "12 red roses, eucalyptus, baby’s breath"),
            ("**Soft Pastels** (~$55)", "peach roses, pink lilies, white alstroemeria"),
            ("**Modern Whites** (~$75)", "white roses, orchids (seasonal), ruscus"),
        ],
        "birthday": [
            ("**Bright & Cheerful** (~$45)", "sunflowers, gerbera daisies, statice"),
            ("**Garden Mix** (~$55)", "spray roses, mums, snapdragons"),
            ("**Tropical Pop** (~$70)", "anthurium, lilies, monstera greens"),
        ],
        "sympathy": [
            ("**Peaceful Whites** (~$60)", "white lilies, roses, greenery"),
            ("**Soft Comfort** (~$55)", "pale roses, stock, eucalyptus"),
            ("**Classic Wreath** (~$120)", "seasonal whites/greens (funeral service)"),
        ],
        "wedding": [
            ("**Bridal Bouquet** (~$120)", "white/ivory roses, ranunculus, greenery"),
            ("**Bridesmaid Posy** (~$65)", "soft pink palette, spray roses, eucalyptus"),
            ("**Boutonnières** (~$18 each)", "mini rose, greenery"),
        ],
        "graduation": [
            ("**School Colors** (~$45)", "daisies, mums matched to colors"),
            ("**Sunny Congrats** (~$50)", "sunflowers, solidago, greens"),
            ("**Orchid Lei** (~$75)", "purple dendrobium orchid lei"),
        ],
        "valentine": [
            ("**Dozen Reds** (~$70)", "12 red roses, filler, greens"),
            ("**Pink Mix** (~$55)", "pink roses, alstroemeria, waxflower"),
            ("**Rose & Lily Duo** (~$65)", "red roses + white lilies"),
        ],
        "special occasion": [
            ("**Designer’s Choice** (~$50)", "seasonal best blooms, custom palette"),
            ("**Pastel Garden** (~$60)", "roses, stock, lisianthus"),
            ("**Bold & Bright** (~$55)", "gerberas, roses, carnations"),
        ],
    }
    lines = [f"Here are a few {occasion} ideas:"]
    for name, stems in recs.get(occasion, recs["special occasion"]):
        lines.append(f"- {name}: {stems}")
    lines.append("Would you like to share **budget**, **colors**, **allergies**, and **delivery date/zip** so I can refine?")
    return "\n".join(lines)

def get_answer(messages):
    # Compose with system prompt at position 0 if not already present
    if not messages or messages[0].get("role") != "system":
        messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    if llm_get_answer:
        return llm_get_answer(messages)  # your existing LLM pipeline
    return fallback_answer(messages)

# ---------------- Session state ----------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "assistant", "content": "Hi! I’m **BloomBot** 🌸 What’s the occasion and budget?"}
    ]

st.title("🌸 BloomBot — Flower Shop Chatbot")

# Sidebar quick starters
with st.sidebar:
    st.subheader("Quick Ask")
    if st.button("Birthday under $50"):
        st.session_state.messages.append({"role": "user", "content": "I need a birthday bouquet under $50. Bright colors."})
    if st.button("Anniversary (classic red)"):
        st.session_state.messages.append({"role": "user", "content": "Anniversary bouquet, classic red roses. Delivery Friday to 80302."})
    if st.button("Sympathy whites"):
        st.session_state.messages.append({"role": "user", "content": "Sympathy arrangement in whites. Service on Tuesday."})
    st.markdown("---")
    st.caption("Tip: Tell me occasion, budget, colors, allergies, delivery date & zip.")

# Render history (skip showing system prompt)
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    with st.chat_message(m["role"]):
        st.write(m["content"])

# User input
user_text = st.chat_input("Tell me the occasion, budget, colors, and delivery date…")
if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.write(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Designing bouquet ideas…"):
            reply = get_answer(st.session_state.messages)
        st.write(reply)
    st.session_state.messages.append({"role": "assistant", "content": reply})