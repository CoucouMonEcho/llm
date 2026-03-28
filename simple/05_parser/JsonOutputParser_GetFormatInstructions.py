from pydoc_data.topics import topics

from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Person(BaseModel):
    time: str = Field(dercription="时间")
    person: str = Field(dercription="人物")
    event: str = Field(dercription="事件")

parser = JsonOutputParser(pydantic_object=Person)

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

format_instructions = parser.get_format_instructions()

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，只输出结构化JSON数据"),
    ("human", "生成一个关于{topic}的新闻，{format_instructions}"),
])

prompt = chat_prompt.format_messages(topic="小米su7跑车", format_instructions=format_instructions)
logger.info(prompt)

res = model.invoke(prompt)
logger.info(res)

resp = parser.invoke(res)
logger.info(resp)