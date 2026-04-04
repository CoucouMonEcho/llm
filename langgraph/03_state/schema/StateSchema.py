from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict


class InputState(TypedDict):
    question: str


class OutputState(TypedDict):
    answer: str


class OverallState(InputState, OutputState):
    pass


def answer_node(state: InputState):
    """
    处理输入并生成答案的节点
    Args:
        state: 输入状态
    Returns:
        dict: 包含答案的字典
    """
    print(f"执行 answer_node 节点:")
    print(f"  输入: {state}")

    answer = "再见" if "bye" in state["question"].lower() else "你好"
    result = {"answer": answer, "question": state["question"]}

    print(f"  输出: {result}")
    return result


def demo_input_output_schema():
    builder = StateGraph(OverallState, input_schema=InputState, output_schema=OutputState)
    builder.add_edge(START, "answer_node")
    builder.add_node("answer_node", answer_node)
    builder.add_edge("answer_node", END)
    graph = builder.compile()

    result = graph.invoke({"question": "Hi"})
    print(f"图调用结果: {result}")
    print(graph.get_graph().print_ascii())
    # https://www.processon.com/mermaid
    print(graph.get_graph().draw_mermaid())
    print()


def main():
    """主函数"""
    print("=== LangGraph 图输入输出模式===\n")

    demo_input_output_schema()


if __name__ == "__main__":
    main()
