import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load env variables
load_dotenv()

endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT","gpt-4o-mini")

if not endpoint or not api_key or not deployment:
    raise SystemExit("Missing Azure OpenAI environment variables in .env")

# Create Azure OpenAI client
client = AzureOpenAI(
    api_key=api_key,
    api_version="2024-02-01",
    azure_endpoint=endpoint,
)

# Initialize conversation history with system prompt
messages = [
    {"role": "system", "content": "You are a friendly teaching assistant. Answer clearly and concisely."}
]

print("Azure OpenAI Chat Ready — type 'quit' to exit.\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "quit":
        break

    # Add user message
    messages.append({"role": "user", "content": user_input})

    # Call Azure OpenAI Chat Completion
    response = client.chat.completions.create(
        model=deployment,       # MUST match your deployment name
        messages=messages,
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    print(f"Assistant: {reply}\n")

    # Add response to history
    messages.append({"role": "assistant", "content": reply})
