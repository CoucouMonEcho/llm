import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from datetime import datetime

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

template = PromptTemplate.from_template(
    "现在时间是：{time}，请根据我的问题给出回答，我的问题是：{question}",
    partial_variables={"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")},
)
template.partial(question="今天是几月几号")

prompt = template.format()

print(prompt)

res = model.invoke(prompt)
print(res.content)
print("\n")
