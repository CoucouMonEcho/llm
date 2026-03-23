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
    SystemMessage(content="你是一个法律助手，只回答法律问题，超出法律范围的统一回答：非法律问题无可奉告。"),
    HumanMessage(content="简单介绍下广告法，50字以内一句话。"),
    # HumanMessage(content="2+3=?"),
]

resp = model.invoke(messages)
print(f'响应类型: {type(resp)}')
print()
print(resp.content)
print(resp.content_blocks)
