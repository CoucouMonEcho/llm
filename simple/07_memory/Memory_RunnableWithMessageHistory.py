from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableWithMessageHistory, RunnableConfig
from langchain_core.chat_history import InMemoryChatMessageHistory
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = init_chat_model(
    "qwen2.5:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])
parser = StrOutputParser()
chain = prompt | model | parser

history = InMemoryChatMessageHistory()
runnable = RunnableWithMessageHistory(
    chain,
    get_session_history=lambda session_id: history,
    input_messages_key="input",
    history_messages_key="history",
)
history.clear()
config = RunnableConfig(configurable={"session_id": "user-001"})

logger.info(runnable.invoke({"input": "我叫张三，我爱好学习。"}, config))
logger.info(runnable.invoke({"input": "我叫什么？我的爱好是什么？"}, config))
