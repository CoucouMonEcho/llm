from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage


class GraphState(TypedDict):
    # add_messages 自动追加消息
    messages: Annotated[List, add_messages]


model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)


def model_node(state: GraphState):
    reply = model.invoke(state["messages"])
    # 自动追加消息
    return {"messages": [reply]}


graph = StateGraph(GraphState)

graph.add_node("model", model_node)

graph.add_edge(START, "model")
graph.add_edge("model", END)

# print(graph.edges)
print()
# print(graph.nodes)

app = graph.compile()

# result = app.invoke({"messages": [HumanMessage(content="请用一句话解释什么是 LangGraph。")]})
result = app.invoke({"messages": "一句话解释什么是 LangGraph。"})

print("模型回答：", result["messages"][-1].content)

print()

print(app.get_graph().print_ascii())
# https://www.processon.com/mermaid
print(app.get_graph().draw_mermaid())