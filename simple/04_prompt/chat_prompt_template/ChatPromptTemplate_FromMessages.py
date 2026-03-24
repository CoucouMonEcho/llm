import os
from langchain_core.prompts import ChatPromptTemplate
from langchain.chat_models import init_chat_model

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个AI开发工程师，你的名字是{name}"),
        ("human", "你能帮我做什么"),
        ("ai", "我能开发很多{thing}"),
        ("human", "{user_input}")
    ]
)

prompt_1 = chat_prompt.format_messages(
    **{"name": "深度求索", "thing": "AI", "user_input": "7+5=?"}
)
print(prompt_1)
print()

prompt_2 = chat_prompt.invoke(
    {"name": "深度求索", "thing": "AI", "user_input": "7+5=?"}
)
print(prompt_2.to_string())
print()

prompt_3 = chat_prompt.format(
    **{"name": "深度求索", "thing": "AI", "user_input": "7+5=?"}
)
print(prompt_3)
print()

# model = init_chat_model(
#     "deepseek-r1:14b",
#     model_provider="ollama",
#     base_url="http://localhost:11434",
#     reasoning=False
# )
#
# res = model.invoke(prompt_1)
# print(res)
# print(res.content)
