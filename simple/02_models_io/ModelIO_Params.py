import os

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
model = init_chat_model(
    "deepseek-v3.2",
    model_provider="openai",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    temperature=1.9,
    # temperature=0.0,
)

for x in range(3):
    print(model.invoke("写一句关于春天的词，14字以内").content)