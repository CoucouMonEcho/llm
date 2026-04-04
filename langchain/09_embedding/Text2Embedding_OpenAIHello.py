# https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2842587

import os
from openai import OpenAI
from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

input_text = "衣服的质量很好"

completion = client.embeddings.create(
    model="text-embedding-v4",
    input=input_text,
)

print(completion.model_dump_json())
