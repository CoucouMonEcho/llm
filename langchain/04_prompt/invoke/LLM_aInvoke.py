import asyncio
import os

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv(encoding='utf-8', override=True)
model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)


async def main():
    resp = await model.ainvoke("解释一下LangChain是什么，简洁回答100字以内")
    # 响应类型: <class 'langchain_core.messages.ai.AIMessage'>
    print(f'响应类型: {type(resp)}')
    print(resp.content_blocks)


if __name__ == '__main__':
    asyncio.run(main())
