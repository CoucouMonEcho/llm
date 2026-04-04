import os

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
model = init_chat_model(
    "qwen-plus",
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

print(model)

resp = model.invoke("你是谁")
print(resp)
print()
print(resp.content)
print('*' * 50)
