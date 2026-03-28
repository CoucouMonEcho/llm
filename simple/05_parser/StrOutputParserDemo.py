from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个{role}，简短回答用户问题，结果返回json格式，q字段表示问题，a字段表示答案"),
    ("human", "请回答:{question}"),
])

prompt = chat_prompt.invoke({"role": "AI助手", "question": "什么是LangChain，简洁回答100字以内"})
logger.info(prompt)

res = model.invoke(prompt)
logger.info(res)

print('=' * 50)

parser = StrOutputParser()
resp = parser.invoke(res)

# <class 'dict'>
logger.info(type(resp))
# {'q': '什么是LangChain', 'a': 'LangChain 是一个用于构建和训练语言模型的开源工具链。'}
logger.info(resp)
