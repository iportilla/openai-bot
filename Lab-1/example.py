# chat_client_simple.py
import os
from dotenv import load_dotenv
from openai import OpenAI



# Installation reminders:
# pip install openai python-dotenv


#Load environment variables from .env (expects OPENAI_API_KEY)
load_dotenv()
api_key = os.getenv("openai_api_key")  # must match variable name in .env file
if not api_key:
    raise SystemExit("Missing openai_api_key. Put it in a .env file or export it.")

#Initialize OpenAI client
client = OpenAI(api_key=api_key)

#Conversation history (system message defines assistant behavior)
messages = [
    {"role": "system", "content": "You are a helpful, concise assistant."}
]

#https://platform.openai.com/chat
#Themes for system messages:
# {“role”: “system”, “content”: “You are a helpful assistant.”}
# {“role”: “system”, “content”: “You are a cynical robot. You answer correctly but with a sarcastic and world-weary tone.”}
# {“role”: “system”, “content”: “You are a helpful pirate captain. You answer all questions with pirate slang, calling the user ‘matey’ and ending with ‘Yarrr!'”}
# {“role”: “system”, “content”: “You are a Shakespearean assistant. You answer all questions in the style of Shakespearean English.”}
# {“role”: “system”, “content”: “You are a friendly assistant that always responds in rhyme.”}
# {“role”: “system”, “content”: “You are a technical assistant that provides detailed explanations and code examples.”}
# {“role”: “system”, “content”: “You are a minimalist assistant that provides brief, to-the-point answers.”}
# {“role”: “system”, “content”: “You are a humorous assistant that adds a joke to every response.”}
# {“role”: “system”, “content”: “You are a motivational coach that encourages and inspires the user.”}
# {“role”: “system”, “content”: “You are a travel guide that provides recommendations and tips for various destinations.”}
# {“role”: “system”, “content”: “You are a fitness trainer that offers workout routines and health advice.”}
# {“role”: “system”, “content”: “You are a British chef who responds with sarcastic and annoyed wit.”}


print("Your AI assistant is ready. Type 'quit' to exit.\n")

#Conversation loop
try:
    while True:
        #Get user input
        user_input = input("You: ").strip()
        if user_input.lower() == "quit":
            break

        # Add the user message to history
        messages.append({"role": "user", "content": user_input})

        # Call OpenAI for a response
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # lightweight, cost-efficient model
                messages=messages,
                temperature=0.7,
            )
            assistant_msg = response.choices[0].message.content
        except Exception as e:
            # Roll back last user message if the call fails
            messages.pop()
            print(f"Assistant (error): {e}")
            continue

        #Print and store assistant reply
        print(f"Assistant: {assistant_msg}\n")
        messages.append({"role": "assistant", "content": assistant_msg})

#Graceful exit
except (KeyboardInterrupt, EOFError):
    print("\n Goodbye!")