import os

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv(encoding='utf-8', override=True)
model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

messages = [
    SystemMessage(content="你叫DeepSeek-R1，是一个人工助手。"),
    HumanMessage(content="你是谁"),
]

resp = model.stream(messages)

# 响应类型: <class 'generator'>
print(f'响应类型: {type(resp)}')
for chunk in resp:
    print(chunk.content, end='', flush=True)
print('\n')
