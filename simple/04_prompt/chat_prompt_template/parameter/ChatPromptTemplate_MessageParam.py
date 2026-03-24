import os
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.chat_models import init_chat_model

chatPromptTemplate = ChatPromptTemplate(
    [
        # SystemMessage(content="你是一个AI开发工程师，你的名字是{name}"),
        SystemMessage(content="你是一个AI开发工程师，你的名字是深度求索"),
        HumanMessage(content="你能帮我做什么"),
        # AIMessage(content="我能开发很多{thing}"),
        AIMessage(content="我能开发很多AI"),
        # HumanMessage(content="{user_input}")
        HumanMessage(content="7+5=?")
    ]
)

# chatPromptTemplate = chatPromptTemplate.format_messages(
#     name="深度求索", thing="AI", user_input="7+5=?"
# )
prompt = chatPromptTemplate.format_messages()
print(prompt)

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

res = model.invoke(prompt)
print(res)
print(res.content)
