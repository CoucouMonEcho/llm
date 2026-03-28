from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

prompt1 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，用中文简短回答"),
    ("human", "简短介绍什么是{topic}，不超过100字"),
])
parser1 = StrOutputParser()
chain1 = prompt1 | model | parser1

prompt2 = ChatPromptTemplate.from_messages([
    ("system", "你是一个知识渊博的计算机专家，用英文简短回答"),
    ("human", "简短介绍什么是{topic}，不超过100字"),
])
parser2 = StrOutputParser()
chain2 = prompt2 | model | parser2

parallel_chain = RunnableParallel({
    "chinese": chain1,
    "english": chain2,
})

res = parallel_chain.invoke({"topic": "langchain"})
logger.info(res)

parallel_chain.get_graph().print_ascii()