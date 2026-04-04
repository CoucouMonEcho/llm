import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

resp = client.chat.completions.create(
    model="qwen-plus",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "你是谁"},
    ],
    stream=False
)

print(resp.choices[0].message.content)
