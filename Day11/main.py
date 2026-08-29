import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

from langchain_chroma import Chroma
from pydantic import BaseModel
from typing import List


load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# embeddings
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=API_KEY
)

# llms
memory_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.1,
    google_api_key=API_KEY
)

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    temperature=0.5,
    google_api_key=API_KEY
)

memory_extractor_llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.2,
    google_api_key=API_KEY
)

# database (chromadb)

chroma_db = Chroma(
    collection_name="memory_bot",
    embedding_function=embeddings,
    persist_directory="./.chroma_db"
)

user_query = input("Enter your query:  ")

class MemoryData(BaseModel):
    query: str 
    responose: str = ""
    search_query: str = ""
    memory: List[str] = []
    db_prompt: str = ""

data = MemoryData(query=user_query)

#search from chroma db
prompt =f"""You are a memory retrieval query generator.
Convert the user's current question into a concise semantic
search query for retrieving relevant long-term memories.
Rules:
- Preserve important names, facts, preferences and context.
- Do not answer the question.
- Do not explain anything.
- Return ONLY the search query.
- Keep it short and meaningful.

User question:
{data.query}
"""


serach_db_query = memory_llm.invoke(prompt)
data.search_query = serach_db_query.content


# print("this is search query: ")
# print(data.search_query)
# print("end")

# print(data.search_query)
# print(type(data.search_query))

results = chroma_db.similarity_search(data.search_query, k=5)

# print("this is results from chroma db: ")
# print(results)
# print("end")


# if not results: 
#     memory_text = "No memories found"
# else:
#     memory_text = "\n\n".join([doc.page_content for doc in results])

if results:
    memory_text = "\n\n".join(
        [
            f"Previous Memory {i + 1}:\n{doc.page_content}"
            for i, doc in enumerate(results)
        ]
    )
else:
    memory_text = "No relevant previous memory was found."

data.memory = memory_text

custome_prompt = f"""
You are a helpful AI assistant with access to relevant long-term
memories.
Answer the user's current question using the memories only when
they are relevant.
Rules:
- Do not mention the memory system or database.
- Ignore irrelevant memories.
- Do not invent information.
- Answer directly and naturally.
- Keep the answer concise unless the user asks for detail.
Previous relevant memories:
{data.memory}
Current user question:
{data.query}
Provide the best answer.

"""
response = llm.invoke(custome_prompt)

data.responose = response.content[0]["text"]

print(data.responose)

db_prompt = f"""
You are a long-term memory extraction system.
Analyze the user's message and the assistant's response.
Your job is to extract ONLY information that could be useful in
future conversations.
Store things such as:
- User's name
- Age
- Location
- Profession
- Education
- Skills
- Hobbies
- Preferences
- Goals
- Projects
- Important personal facts
- Stable user preferences
- Important ongoing context
DO NOT store:
- Greetings
- Casual conversation
- Temporary information
- Questions that contain no useful personal information
- Generic assistant responses
- Unimportant details
- Information that is only useful for the current question
IMPORTANT:
- Do not guess or invent information.
- Only extract information explicitly supported by the conversation.
- If there is no useful long-term information, return exactly:
NO_MEMORY
Return ONLY the useful memory.
Do not explain your decision.
User message:
{data.query}
Assistant response:
{data.responose}
"""

data_for_db = memory_extractor_llm.invoke(db_prompt)

data.db_prompt = data_for_db.content.strip()

if data.db_prompt != "NO_MEMORY":
    chroma_db.add_texts(
        texts=["User question: " + data.query + "Answer: " + data.responose]
    )

