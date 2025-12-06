# Project Structure

## Directory Organization

```
openai-bot/
├── Lab-1/                    # Basic OpenAI API fundamentals
│   ├── example.py           # Minimal API usage example
│   ├── generic_openai_chatbot.py
│   ├── azure_chatbot.py     # Azure OpenAI variant
│   ├── watsonx_chatbot.py   # IBM WatsonX variant
│   └── .env                 # Lab-specific credentials
│
├── Lab-2/                    # Conversation memory & state
│   ├── text_memory_bot.py   # Main chatbot with memory
│   ├── utils.py             # Helper functions (get_answer, etc.)
│   └── __pycache__/
│
├── Lab-3/                    # Domain-specific & voice bots
│   ├── flower_bot.py        # Flower recommendation chatbot
│   ├── voice_bot.py         # Voice interaction pipeline
│   ├── utils.py             # Audio and API helpers
│   └── __pycache__/
│
├── Lab-4/                    # Pizza ordering chatbot exercise
│   ├── pizza-bot-starter/   # Student starter template
│   │   └── app_pizza_bot.py
│   └── pizza-bot-complete/  # Reference solution
│       ├── app_pizza_bot.py
│       └── menu.json        # Pizza menu data
│
├── voice/                    # Streamlit voice chatbot app
│   ├── app.py               # Main Streamlit app
│   ├── voice_bot.py         # Voice bot implementation
│   ├── utils.py             # Audio processing & API calls
│   ├── requirements.txt
│   └── image.png
│
├── voice_code/              # Alternate voice implementation
│   ├── app.py
│   ├── utils.py
│   └── requirements.txt
│
├── .env.sample              # Template for environment variables
├── requirements.txt         # Root-level dependencies
└── README.md               # Project overview
```

## Key Patterns

### Lab Structure
Each lab is self-contained with:
- Main application file(s)
- Optional `utils.py` for shared helpers
- Optional `.env` for lab-specific credentials
- `README.md` with learning goals and instructions

### Utility Modules
`utils.py` files typically contain:
- `get_answer()` — Call OpenAI API with message history
- `text_to_speech()` — Convert text to audio
- `speech_to_text()` — Transcribe audio to text
- Message formatting helpers

### Streamlit Apps
Interactive apps follow this pattern:
- Initialize session state for message history
- Render chat history with `st.chat_message()`
- Accept user input with `st.chat_input()` or `audio_recorder()`
- Call API and append responses to session state

### Configuration
- Environment variables stored in `.env` files
- Loaded with `dotenv.load_dotenv()`
- API keys, endpoints, and deployment names configured per lab

## File Naming Conventions

- Main app files: `app_*.py` or `*_bot.py`
- Utilities: `utils.py`
- Notebooks: `*.ipynb`
- Configuration: `.env`, `menu.json`
- Compressed archives: `*.zip`

## Dependencies Management

- Root `requirements.txt` — Global dependencies
- Lab-specific `requirements.txt` — Additional lab dependencies
- Virtual environment: `.venv/` (not committed)
