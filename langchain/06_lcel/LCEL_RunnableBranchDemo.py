from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableBranch
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

en_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个英语翻译专家，你叫小英。"),
    ("human", "请回答:{query}"),
])
jp_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个日语翻译专家，你叫小日。"),
    ("human", "请回答:{query}"),
])
kr_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个韩语翻译专家，你叫小韩。"),
    ("human", "请回答:{query}"),
])


def determine_language(inputs):
    query = inputs["query"]
    if "日语" in query:
        return "jp"
    elif "韩语" in query:
        return "kr"
    else:
        return "en"


parser = StrOutputParser()

chain = RunnableBranch(
    (lambda x: determine_language(x) == "jp", jp_prompt | model | parser),
    (lambda x: determine_language(x) == "kr", kr_prompt | model | parser),
    (en_prompt | model | parser)
)

test_queries = [
    {"query": "用韩语翻译这句话：'见到你很高兴'"},
    {"query": "用日语翻译这句话：'见到你很高兴'"},
    {"query": "用英语翻译这句话：'见到你很高兴'"},
]

for query_input in test_queries:
    lang = determine_language(query_input)
    logger.info(f"lang: {lang}")

    if lang == "jp":
        chatPromptTemplate = jp_prompt
    elif lang == "kr":
        chatPromptTemplate = kr_prompt
    else:
        chatPromptTemplate = en_prompt

    formatted_messages = chatPromptTemplate.format_messages(**query_input)
    for msg in formatted_messages:
        logger.info(f"[{msg.type}]: {msg.content}")

    res = chain.invoke(query_input)
    logger.info(f"res: {res}")
