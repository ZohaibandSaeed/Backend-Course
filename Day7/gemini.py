from google import genai

from dotenv import load_dotenv
load_dotenv()

import os

API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)


interaction = client.interactions.create(
    model="gemini-3.5-flash",
    input="what is llm tell me in short?"
)

print(interaction.output_text)