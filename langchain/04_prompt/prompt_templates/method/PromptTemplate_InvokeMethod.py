import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

template = PromptTemplate.from_template("你是一个专业的{role}工程师，请根据我的问题给出回答，我的问题是：{question}")

prompt = template.invoke({"role": "Golang开发", "question": "冒泡排序怎么写，只要代码其他不要，简洁回答"})

# <class 'langchain_core.prompt_values.StringPromptValue'>
print(type(prompt))
print(prompt)

# <class 'str'>
print(type(prompt.to_string()))
print(prompt.to_string())

# <class 'list'>
print(type(prompt.to_messages()))
print(prompt.to_messages())
