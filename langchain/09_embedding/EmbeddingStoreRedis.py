# https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2842587

import os
from importlib.metadata import metadata

from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Redis
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
host_ip = os.getenv("HOST_IP")
REDIS_URL = f"redis://{host_ip}:6379"

embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("OPENAI_API_KEY"),
)

texts = [
    "通义千问是阿里巴巴研发的大语言模型。",
    "Redis 是一个高性能的键值存储系统，支持向量检索。",
    "LangChain 可以轻松集成各种大模型和向量数据库。"
]
documents = [Document(page_content=text, metadata={"source": "manual"}) for text in texts]

vector_store = Redis.from_documents(
    documents=documents,
    embedding=embeddings,
    redis_url=REDIS_URL,
    index_name="my_index"
)

retriever = vector_store.as_retriever(search_kwargs={"k": 2})
res = retriever.invoke("Langchain 和 Redis 怎么结合？")
for res1 in res:
    print(res1.page_content)
