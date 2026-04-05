import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

chatPromptTemplate = ChatPromptTemplate(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}"),
        ("human", "你能帮我做什么"),
        ("ai", "我能开发很多{thing}"),
        ("human", "{user_input}")
    ]
)

prompt = chatPromptTemplate.format_messages(
    name="深度求索", thing="AI", user_input="7+5=?"
)
print(prompt)

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

res = model.invoke(prompt)
print(res)
print(res.content)