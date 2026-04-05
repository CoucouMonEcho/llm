from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，简短回答用户问题。"),
    ("human", "简短介绍什么是{topic}，不超过100字"),
])
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1
res1 = chain1.invoke({"topic": "langchain"})
logger.info(res1)

prompt2 = ChatPromptTemplate.from_messages([
    ("human", "翻译这段话为英文：{input}"),
])
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2
res2 = chain2.invoke({"input": res1})
logger.info(res2)

full_chain = chain1 | (lambda content: {"input": content}) | chain2
res3 = full_chain.invoke({"topic": "langchain"})
logger.info(res3)
