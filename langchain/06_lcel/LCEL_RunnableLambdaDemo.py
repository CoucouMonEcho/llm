from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)


def debug_print(x):
    logger.info(f"中间结果：{x}")
    return {"input": x}


prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，用中文简短回答"),
    ("human", "简短介绍什么是{topic}，不超过100字"),
])
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

prompt2 = ChatPromptTemplate.from_messages([
    ("human", "翻译这段话为英文：{input}"),
])
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

debug_node = RunnableLambda(debug_print)

full_chain = chain1 | debug_node | chain2

res = full_chain.invoke({"topic": "langchain"})
logger.info(res)
