# Lab 2 — Chatbot with Memory

## Goal

This lab expands the basic chatbot by adding **conversation memory**, allowing the bot to reference earlier parts of the dialogue. You will explore both:

- **Short-term memory:** conversation history stored during the session.
- **Context-aware modeling:** how the model uses previous messages as part of the prompt.

## Files in This Folder

- `text_memory_bot.py` — Main chatbot with memory.
- `utils.py` — Helper functions for message formatting and conversation history.

## How to Run

```bash
cd Lab-2
streamlit run text_memory_bot.py
```

## Key Concepts Introduced

- Maintaining conversation state client-side
- Token cost growth as memory increases
- Practical context window limits