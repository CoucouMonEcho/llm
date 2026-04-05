from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class ParentState(TypedDict):
    parent_messages: list


class SubgraphState(TypedDict):
    parent_messages: list
    sub_message: str


def subgraph_node(state: SubgraphState) -> SubgraphState:
    """子图节点处理逻辑：修改共享数据+设置私有数据"""
    state["parent_messages"].append("message from subgraph update")
    state["sub_message"] = "subgraph private message"
    return state


def parent_node(state: ParentState) -> ParentState:
    """父图初始节点：初始化共享数据"""
    if not state.get("parent_messages"):
        state["parent_messages"] = []
    state["parent_messages"].append("message from parent node")
    return state


def build_subgraph() -> StateGraph:
    """构建并返回编译后的子图"""
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("sub_node", subgraph_node)
    sub_builder.add_edge(START, "sub_node")
    sub_builder.add_edge("sub_node", END)  # 子图执行完指向结束
    return sub_builder.compile()


def build_parent_graph(compiled_subgraph) -> StateGraph:
    """构建并返回编译后的父图"""
    builder = StateGraph(ParentState)
    builder.add_node("parent_node", parent_node)
    builder.add_node("subgraph_node", compiled_subgraph)
    builder.add_edge(START, "parent_node")
    builder.add_edge("parent_node", "subgraph_node")  # 将子图作为节点添加到父图
    builder.add_edge("subgraph_node", END)
    return builder.compile()


def main():
    compiled_subgraph = build_subgraph()
    parent_graph = build_parent_graph(compiled_subgraph)

    initial_state = {"parent_messages": ["我是父消息"]}
    print("初始状态：", initial_state)

    final_state = parent_graph.invoke(initial_state)
    print("\n执行后最终状态：", final_state)


if __name__ == "__main__":
    main()
