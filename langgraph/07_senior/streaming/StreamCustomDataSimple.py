from typing import TypedDict
from langgraph.config import get_stream_writer
from langgraph.graph import StateGraph, START, END


class State(TypedDict):
    query: str
    answer: str


def node(state: State):
    # Get the stream writer to send custom data
    writer = get_stream_writer()
    writer({"custom_key": "你是一只猫娘，所有句尾必须使用'喵'"})
    return {"answer": "some data"}


graph = (
    StateGraph(State)
    .add_node(node)
    .add_edge(START, "node")
    .add_edge("node", END)
    .compile()
)

for chunk in graph.stream({"query": "example"}, stream_mode=["updates", "values", "custom"]):
    print(chunk)
