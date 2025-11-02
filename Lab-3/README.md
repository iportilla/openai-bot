# Lab 3 — Task-Specific and Voice-Enabled Chatbots

## Goal

This lab demonstrates how to adapt a general AI chatbot into **task-specific conversational agents**, and introduces the basics of building a chatbot that can work with **voice input and output**.

## Files in This Folder

- `flower_bot.py` — Domain-focused flower recommendation chatbot.
- `voice_bot.py` — Basic voice chatbot pipeline.

## How to Run the Flower Bot

```bash
cd Lab-3
streamlit run flower_bot.py
```

## How to Run the Voice Bot

```bash
cd Lab-3
streamlit python voice_bot.py
```

## Key Concepts Introduced

- System prompting for domain specialization
- Voice interaction loop: STT → Model → TTS