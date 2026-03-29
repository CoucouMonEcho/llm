
from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)

embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",  # 支持 v1 或 v2
    dashscope_api_key=os.getenv("OPENAI_API_KEY"),  # 从环境变量读取
)

texts = [
    "我喜欢吃苹果",
    "苹果是我最喜欢吃的水果",
    "我喜欢用苹果手机",
]
# query_result = embeddings.embed_query(texts)
# print(query_result)

embeddings = embeddingsModel.embed_documents(texts)

for i, vec in enumerate(embeddings, 1):
    print(f"文本 {i}: {texts[i-1]}")
    print(f"向量长度: {len(vec)}")
    print(f"前5个向量值: {vec[:10]}\n")

metadata = [{"segment_id": "1"}, {"segment_id": "2"}, {"segment_id": "3"}]

host_ip = os.getenv("HOST_IP")
REDIS_URL = f"redis://{host_ip}:6379"

config = RedisConfig(
    index_name="newsgroups",
    redis_url=REDIS_URL,
)

vector_store = RedisVectorStore(embeddingsModel, config=config)

ids = vector_store.add_texts(texts, metadata)

print(ids[0:5])