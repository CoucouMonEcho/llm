import os

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from datetime import datetime

model = init_chat_model(
    "qwen2.5:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

template_a = PromptTemplate.from_template("用一句话介绍{topic}，通俗易懂\n")
template_b = PromptTemplate.from_template("不超过{length}token")
template = template_a + template_b

prompt = template.format(topic="LangChain", length=200)

print(prompt)

res = model.invoke(prompt)
print(res.content)
print("\n")
