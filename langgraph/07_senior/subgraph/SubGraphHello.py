from operator import add
from typing import TypedDict, Annotated
from langgraph.constants import END
from langgraph.graph import StateGraph, MessagesState, START
import operator


class BasicState(TypedDict):
    messages: Annotated[list[str], add]


def sub_node(state: BasicState) -> BasicState:
    return {"messages": ["response from subgraph"]}


subgraph_builder = StateGraph(BasicState)
subgraph_builder.add_node("sub_node", sub_node)

subgraph_builder.add_edge(START, "sub_node")
subgraph_builder.add_edge("sub_node", END)
subgraph = subgraph_builder.compile()

builder = StateGraph(BasicState)
builder.add_node("subgraph_node", subgraph)
builder.add_edge(START, "subgraph_node")
builder.add_edge("subgraph_node", END)

graph = builder.compile()

# {'messages': ['main-graph', 'main-graph', 'response from subgraph']}
print(graph.invoke({"messages": ["main-graph"]}))
print()

print(subgraph.get_graph().print_ascii())
# https://www.processon.com/mermaid
print(subgraph.get_graph().draw_mermaid())