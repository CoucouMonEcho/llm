from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, field_validator
from typing_extensions import Self

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)


class Product(BaseModel):
    name: str = Field(description="产品名称")
    category: str = Field(description="产品类别")
    description: str = Field(description="产品简介")

    @field_validator("description")
    def validate_description(cls, value):
        if len(value) < 10:
            raise ValueError("产品简介长度必须大于等于10")
        return value


parser = PydanticOutputParser(pydantic_object=Product)

format_instructions = parser.get_format_instructions()

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个AI助手，只输出结构化JSON数据\n{format_instructions}"),
    ("human", "输出标题为：{topic}的新闻内容"),
])

prompt = prompt_template.format_messages(topic="华为Mate X7", format_instructions=format_instructions)
print(prompt)

res = model.invoke(prompt)
print(res)

resp = parser.invoke(res)
# <class '__main__.Product'>
print(type(resp))
print(resp)
