from groq import Groq
from dotenv import load_dotenv
load_dotenv()

import os

from pydantic import BaseModel
from typing import List

class LLM_Response(BaseModel):
    title: str
    response:str
    desciption:List[str]

API_KEY = os.getenv("GROQ_API_KEY")

client = Groq(api_key=API_KEY)

custom_promtp = """
you are a senior llm and give me answer in short and to the point. and the answer must be in json formate. like as
{
"title" : string,
"response" : string,
"desciption": [string, string]
}
"""

completion = client.chat.completions.create(
    model="openai/gpt-oss-120b",
    messages=[
      {
        "role": "user",
        "content": f"{custom_promtp }what is java language"
      }
    ],
    temperature=1,
    max_completion_tokens=2048,
    top_p=1,
    reasoning_effort="medium",
    response_format={ "type": "json_object" },
    stream=True,
    stop=None
)
complete_respose = ""

for chunk in completion:
    data = chunk.choices[0].delta.content or ""
    complete_respose = complete_respose + data

obj = LLM_Response.model_validate_json(complete_respose)

print(type(obj))