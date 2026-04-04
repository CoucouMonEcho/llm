# https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2842587
import json
import os
from http import HTTPStatus

import dashscope
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)

resp = dashscope.MultiModalEmbedding.call(
    model="tongyi-embedding-vision-plus",
    api_key=os.getenv("OPENAI_API_KEY"),
    input=[{"text": "langchain"}]
)

res = ""

if resp.status_code == HTTPStatus.OK:
    res = {
        "status_code": resp.status_code,
        "request_id": getattr(resp, "request_id", ""),
        "code": getattr(resp, "code", ""),
        "message": getattr(resp, "message", ""),
        "output": resp.output,
        "usage": resp.usage,
    }
    print(json.dumps(res, ensure_ascii=False, indent=4))
