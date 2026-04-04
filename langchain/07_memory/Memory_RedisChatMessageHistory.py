import os

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain_community.chat_message_histories import RedisChatMessageHistory
from dotenv import load_dotenv
import logging
import redis

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv(encoding='utf-8', override=True)

# 5.3.1
logger.info(redis.__version__)

host_ip = os.getenv("HOST_IP")
REDIS_URL = f"redis://{host_ip}:6379"

# decode_responses=False 字节
# decode_responses=True 字符串
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

print(redis_client.ping())

model = init_chat_model(
    "qwen2.5:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder("history"),
    ("human", "{question}"),
])


def get_session_history(session_id: str) -> RedisChatMessageHistory:
    history = RedisChatMessageHistory(
        session_id=session_id,
        url=REDIS_URL,
        ttl=300,
    )
    return history


chain = RunnableWithMessageHistory(
    prompt | model,
    get_session_history,
    input_messages_key="question",
    history_messages_key="history",
)

config = RunnableConfig(configurable={"session_id": "user-001"})

print("开始对话，输入'q'退出")
while True:
    question = input("\ninput:")
    if question.lower() in ["quit", "exit", "q"]:
        break

    resp = chain.invoke({"question": question}, config)
    logger.info(f"output: {resp.content}")

    # redis_client.save()
