# https://bailian.console.aliyun.com/cn-beijing?tab=doc#/doc/?type=model&url=2842587

import os
import dashscope
from langchain_community.embeddings import DashScopeEmbeddings
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)

embeddings = DashScopeEmbeddings(
    model="text-embedding-v4",
    dashscope_api_key=os.getenv("OPENAI_API_KEY"),
)

text = "This is a test document."
query_res = embeddings.embed_query(text)
print("文本向量长度：", len(query_res), sep='')

doc_res = embeddings.embed_documents([
    "Hi there!",
    "Oh, hello!",
    "What's your name?",
    "My friends call me World",
    "Hello World!",
])
print(doc_res)
print("文本向量数量：", len(doc_res), "，文本向量长度：", len(doc_res[0]), sep='')
