# Tech Stack & Build System

## Core Technologies

- **Python 3.x** — Primary language
- **OpenAI API** — Chat completions, embeddings, and model interactions
- **Streamlit** — Web UI framework for interactive chatbot apps
- **python-dotenv** — Environment variable management

## Key Libraries

- `openai` — Official OpenAI Python client
- `streamlit` — Interactive web app framework
- `audio_recorder_streamlit` — Audio input component
- `streamlit-float` — UI positioning utilities
- `azure-openai` — Azure OpenAI client (Lab-1 examples)

## Environment Setup

### Virtual Environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Dependencies
```bash
pip install -r requirements.txt
```

### Configuration
- Copy `.env.sample` to `.env`
- Set `OPENAI_API_KEY` or Azure credentials as needed
- Each lab may have its own `.env` file

## Common Commands

### Running Labs
```bash
# Lab 1 - Basic chatbot
python Lab-1/example.py
streamlit run Lab-1/generic_openai_chatbot.py

# Lab 2 - Memory chatbot
streamlit run Lab-2/text_memory_bot.py

# Lab 3 - Flower bot
streamlit run Lab-3/flower_bot.py

# Lab 4 - Pizza bot
streamlit run Lab-4/pizza-bot-starter/app_pizza_bot.py

# Voice apps
streamlit run voice/app.py
python voice_code/app.py
```

## Code Patterns

- **Session State**: Streamlit apps use `st.session_state` for conversation history
- **Message Format**: Standard OpenAI format with `role` (system/user/assistant) and `content`
- **System Prompts**: Define chatbot behavior and personality
- **Utility Functions**: Helper modules (`utils.py`) for common operations like API calls and audio processing

## API Integration

- Direct OpenAI client initialization with API key
- Chat completion calls with temperature and model parameters
- Message history maintained client-side for context
- Support for both OpenAI and Azure OpenAI endpoints
