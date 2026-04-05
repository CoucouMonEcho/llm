from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class BasicState(TypedDict):
    value: int
    step: str


def node_a(state: BasicState) -> dict:
    """节点A"""
    print("执行节点A")
    return {"value": state["value"] + 1, "step": "A执行完毕"}


def node_b(state: BasicState) -> dict:
    """节点B"""
    print("执行节点B")
    return {"value": state["value"] * 2, "step": "B执行完毕"}


def node_c(state: BasicState) -> dict:
    """节点C"""
    print("执行节点C")
    return {"value": state["value"] - 1, "step": "C执行完毕"}


def main():
    builder = StateGraph(BasicState)

    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)
    builder.add_node("node_c", node_c)

    builder.add_edge(START, "node_a")
    builder.add_edge("node_a", "node_b")
    builder.add_edge("node_b", "node_c")
    builder.add_edge("node_c", END)

    app = builder.compile()

    result = app.invoke({"value": 1})
    print(f"执行结果: {result}\n")

    print(builder.edges)
    print(builder.nodes)

    print(app.get_graph().print_ascii())
    # https://www.processon.com/mermaid
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
