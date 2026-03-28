import asyncio
import os

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv(encoding='utf-8', override=True)
model = init_chat_model(
    "qwen2.5:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

questions = [
    '什么是redis?简洁回答，token控制在80以内',
    'Python生成器的作用是?简洁回答，token控制在80以内',
    '解释一下Docker和Kubernetes的关系?简洁回答，token控制在80以内',
]


async def async_batch_call():
    resp = await model.abatch(questions)
    # 响应类型: <class 'list'>
    print(f'响应类型: {type(resp)}')
    for q, r in zip(questions, resp):
        print(f'{q}:\n {r.content}\n')


if __name__ == '__main__':
    asyncio.run(async_batch_call())
