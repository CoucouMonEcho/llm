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

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，简短回答用户问题。"),
    ("human", "请回答:{question}"),
])

prompt = chat_prompt.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})
logger.info(prompt)

res = model.invoke(prompt)
logger.info(res)

parser = StrOutputParser()

resp = parser.invoke(res)
# <class 'langchain_core.messages.base.TextAccessor'>
logger.info(type(resp))
logger.info(resp)

logger.info("=" * 50)

chain = chat_prompt | model | parser
# <class 'langchain_core.runnables.base.RunnableSequence'>
logger.info(type(chain))

res_chain = chain.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})
logger.info(res_chain)
