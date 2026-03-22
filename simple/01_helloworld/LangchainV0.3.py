import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
llm = ChatOpenAI(
    model="deepseek-v3.2",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

resp = llm.invoke("你是谁")

print(resp)
print()
print(resp.content)