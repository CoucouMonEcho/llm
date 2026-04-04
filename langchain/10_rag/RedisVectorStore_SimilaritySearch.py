from langchain_redis import RedisConfig, RedisVectorStore
from langchain_community.embeddings import DashScopeEmbeddings
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)

embeddingsModel = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=os.getenv("OPENAI_API_KEY")
)

host_ip = os.getenv("HOST_IP")
REDIS_URL = f"redis://{host_ip}:6379"

vector_store = RedisVectorStore(
    embeddingsModel,
    config=RedisConfig(
        index_name="newsgroups", redis_url=REDIS_URL
    )
)

query = "我喜欢用什么手机"

results = vector_store.similarity_search_with_score(query, k=3)

for i, (doc, score) in enumerate(results, 1):
    similarity = 1 - score  # score 是距离，可以转成相似度
    print(f"结果 {i}:")
    print(f"内容: {doc.page_content}")
    print(f"元数据: {doc.metadata}")
    print(f"相似度: {similarity:.4f}")
