import warnings
warnings.filterwarnings("ignore")

import os
from dotenv import load_dotenv

load_dotenv()

os.getenv("GEMINI_API_KEY")
from groq import Groq
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma


pdf = PyPDFLoader("abc.pdf")
my_pdf = pdf.load()


text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=80
)

pdf_docs = text_splitter.split_documents(my_pdf)

custom_embedding = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

vector_store = Chroma.from_documents(
    documents=pdf_docs,
    embedding=custom_embedding,
    collection_name="cv_faiss",
    persist_directory="../vectordb"
)

query = "share the work experience"

retriver = vector_store.as_retriever(
    search_kwargs={
        "k": 5
    }
)

result = retriver.invoke(query)


context = "\n".join([docs.page_content for docs in result])


API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": f"give me shortest answer of {query} based on this context {context}"
      }
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    stream=True,
    stop=None
)
complete_respose = ""

for chunk in completion:
    print(chunk.choices[0].delta.content or "", end="")
