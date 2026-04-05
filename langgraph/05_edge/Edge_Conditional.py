from typing import Optional
from langgraph.constants import START, END
from langgraph.graph import StateGraph
from pydantic import BaseModel


class BasicState(BaseModel):
    x: int
    result: Optional[str] = None


def check_x(state: BasicState) -> BasicState:
    print(f"[check_x] Received state: {state}")
    return state


def is_even(state: BasicState) -> bool:
    return state.x % 2 == 0


def handle_even(state: BasicState) -> BasicState:
    print("[handle_even] x 是偶数")
    return BasicState(x=state.x, result="even")


def handle_odd(state: BasicState) -> BasicState:
    print("[handle_odd] x 是奇数")
    return BasicState(x=state.x, result="odd")


builder = StateGraph(BasicState)

builder.add_node("check_x", check_x)
builder.add_node("handle_even", handle_even)
builder.add_node("handle_odd", handle_odd)

builder.add_conditional_edges("check_x", is_even, {
    True: "handle_even",
    False: "handle_odd"
})

builder.add_edge(START, "check_x")

builder.add_edge("handle_even", END)
builder.add_edge("handle_odd", END)

graph = builder.compile()

print(graph.get_graph().print_ascii())
# https://www.processon.com/mermaid
print(graph.get_graph().draw_mermaid())

print("输入 x=4（偶数）")
graph.invoke(BasicState(x=4))

# print("输入 x=3（奇数）")
# graph.invoke(MyState(x=3))
