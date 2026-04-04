import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
chatLLM = ChatOpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-plus"
)

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁"},
]

resp = chatLLM.invoke(messages)

print(resp.content)