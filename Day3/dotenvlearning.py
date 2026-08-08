from dotenv import load_dotenv
import os

load_dotenv()

DATA = os.getenv("DATA", "not found")
print (DATA)

GPT_API = os.getenv("GPT_API")
print (GPT_API)