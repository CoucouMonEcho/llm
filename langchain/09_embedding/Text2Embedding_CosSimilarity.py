# https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2842587

import os
import dashscope
import numpy as np
from http import HTTPStatus
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)

texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机"
]

embeddings = []

for text in texts:
    input_data = [{"text": text}]
    resp = dashscope.MultiModalEmbedding.call(
        model="multimodal-embedding-v1",
        api_key=os.getenv("OPENAI_API_KEY"),
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        input=input_data,
    )

    if resp.status_code == HTTPStatus.OK:
        embedding = resp.output['embeddings'][0]['embedding']
        embeddings.append(embedding)


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    return dot_product / (norm1 * norm2)


print("文本相似度比较结果：")
print("=" * 50)

for i in range(len(texts)):
    for j in range(i + 1, len(texts)):
        similarity = cosine_similarity(embeddings[i], embeddings[j])
        print(f"文本{i + 1} vs 文本{j + 1}：")
        print(f"文本{i + 1}：{texts[i]}：")
        print(f"文本{j + 1}：{texts[j]}：")
        print(f"余弦相似度：{similarity:.4f}：")
        print("-" * 50)
