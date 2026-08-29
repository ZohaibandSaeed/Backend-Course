from dotenv import load_dotenv
load_dotenv()

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma

loader = PyPDFLoader("Zohaib'sResume.pdf")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500, 
    chunk_overlap=70,
    separators = ["\n\n","\n",".",""]
)

split_docs = splitter.split_documents(documents)

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vector_store = Chroma.from_documents(
    documents=split_docs,
    embedding=embeddings,
    collection_name="resume"
)

retriever = vector_store.as_retriever(
    search_kwargs={"k": 3}
)

query = "what is the name of person whome it's resume?"

results = retriever.invoke(query)

context = "\n".join([doc.page_content for doc in results])

client = Groq()
completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": f"Context data:\n{context}\n\nAnalyze this data and then tell me: what is the name of the person whose resume this is?"
      }
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
