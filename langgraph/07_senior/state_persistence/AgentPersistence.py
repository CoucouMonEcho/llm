import os
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

checkpointer = InMemorySaver()
agent = create_agent(model=model, checkpointer=checkpointer)
config = {"configurable": {"thread_id": "user-001"}}

msg1 = agent.invoke({"messages": [("user", "你好，我叫张三，喜欢足球，60字内简洁回复")]}, config)
msg1["messages"][-1].pretty_print()
print()

msg2 = agent.invoke({"messages": [("user", "我叫什么？我喜欢做什么？")]}, config)
msg2["messages"][-1].pretty_print()
print()
