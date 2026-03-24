import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

template = PromptTemplate.from_template("你是一个专业的{role}工程师，请根据我的问题给出回答，我的问题是：{question}")

# prompt = template.partial(role="Golang开发", question="冒泡排序怎么写，只要代码其他不要，简洁回答")
partial = template.partial(role="Golang开发")

# <class 'langchain_core.prompts.prompt.PromptTemplate'>
print(type(partial))
print(partial)

prompt = partial.format(question="冒泡排序怎么写，只要代码其他不要，简洁回答")

# <class 'str'>
print(type(prompt))
print(prompt)