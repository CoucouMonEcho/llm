from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END


class BasicState(TypedDict):
    value: int
    step: str


def node_a(state: BasicState) -> dict:
    print("执行节点A")
    print("state[value]:" + str(state["value"]))
    print("state[step]:" + str(state["step"]))
    return {"value": state["value"] + 1, "step": "A执行完毕"}


def node_b(state: BasicState) -> dict:
    print("执行节点B")
    return {"value": state["value"] * 2, "step": "B执行完毕"}


def main():
    builder = StateGraph(BasicState)

    builder.add_node("node_a", node_a)
    builder.add_node("node_b", node_b)

    builder.set_entry_point("node_a")
    builder.add_edge("node_a", "node_b")
    builder.set_finish_point("node_b")

    app = builder.compile()
    result = app.invoke({"value": 0, "step": "hello"})
    print(f"执行结果: {result}\n")

    print()
    print(app.get_graph().print_ascii())
    # https://www.processon.com/mermaid
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
