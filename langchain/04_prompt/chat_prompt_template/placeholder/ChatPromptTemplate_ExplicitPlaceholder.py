import os
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "你是一个资深Python开发工程师，认真回答用户提出的Python相关的问题。"),
    MessagesPlaceholder("memory"),
    ("human", "{question}")
])

prompt = prompt_template.invoke({
    "memory": [
        HumanMessage("我的名字叫不死川梨华，是一名程序员"),
        AIMessage("好的，不死川梨华你好")
    ],
    "question": "请问我的名字叫什么"
})
print(prompt)

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

res = model.invoke(prompt.to_messages())
print(res)
print(res.content)
