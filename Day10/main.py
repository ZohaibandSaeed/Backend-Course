import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(api_key=os.getenv("GEMINI_API_KEY"), model="gemini-2.5-flash")

query = str(input("Enter your question: "))

response = llm.invoke(query)

print(response.content)

