from typing import Annotated, TypedDict
from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)


class Animal(TypedDict):
    animal: Annotated[str, "动物"]
    emoji: Annotated[str, "表情"]

class AnimalList(TypedDict):
    animals: Annotated[list[Animal], "动物与表情列表"]


chat_prompt = ChatPromptTemplate.from_messages([
    ("human", "任意生成三种动物，以及他们的 emoji 表情"),
])

prompt = chat_prompt.invoke({})

llm_with_structured_output = model.with_structured_output(AnimalList)
res = llm_with_structured_output.invoke(prompt)
print(res)
