# OpenAI Bot Exercises - Project Index

This repository contains hands-on labs and demos exploring how to build chatbots and AI agents using the OpenAI API.

## Repository Structure

```
Lab-1/           # Basic OpenAI chat completion examples
Lab-2/           # Memory-enabled chatbots + utility helpers
Lab-3/           # Flower & voice chatbots
Lab-4/           # Pizza bot exercise
voice/           # Streamlit voice chatbot app
voice_code/      # Alternate implementation of voice chatbot
```

## How to Get Started

1. Clone the repository:

```bash
git clone https://github.com/iportilla/openai-bot.git
cd openai-bot
```

2. Create and activate a Python virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set your API key:

```bash
cp .env.example .env
# Edit .env and add OPENAI_API_KEY
```

---

## Labs

### **Lab 1 - Basic Chatbot**

Located in `Lab-1/`

- Demonstrates minimal OpenAI chat API usage.
- Builds a simple chatbot loop.

### **Lab 2 - Memory and State**

Located in `Lab-2/`

- Adds conversation memory and persistent context.
- Introduces helper utilities.

### **Lab 3 - Flower Bot**

Located in `Lab-3/`

- Task-specific chatbot integration.

---

### **Lab 4 - Pizza Bot exercise**

Located in `Lab-4/`

- Task-specific chatbot integration.

---

## Voice Chatbot Apps

### Streamlit Voice Bot (`voice/`)

```bash
streamlit run voice/app.py
```

### Alternate Voice App (`voice_code/`)

```bash
python voice_code/voice_app.py
```

---
