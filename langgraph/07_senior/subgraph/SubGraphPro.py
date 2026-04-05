from langgraph.graph import StateGraph, START, END
from typing import TypedDict


class ParentState(TypedDict):
    user_query: str
    final_answer: str | None


class SubgraphState(TypedDict):
    analysis_input: str
    analysis_result: str
    intermediate_steps: list


def subgraph_analysis_node(state: SubgraphState) -> SubgraphState:
    """子图核心节点：处理分析逻辑，生成结果"""
    query = state["analysis_input"]
    state["intermediate_steps"] = [f"解析查询：{query}", "执行分析逻辑", "生成结果"]
    state["analysis_result"] = f"针对「{query}」的分析结果：这是子图处理后的内容"
    return state


def build_subgraph() -> StateGraph:
    """构建并编译子图"""
    sub_builder = StateGraph(SubgraphState)
    sub_builder.add_node("subgraph_analysis_node", subgraph_analysis_node)

    sub_builder.add_edge(START, "subgraph_analysis_node")
    sub_builder.add_edge("subgraph_analysis_node", END)
    return sub_builder.compile()


compiled_subgraph = build_subgraph()


def call_subgraph_proxy(state: ParentState) -> ParentState:
    subgraph_input = {
        "analysis_input": state["user_query"],
        "intermediate_steps": [],
        "analysis_result": ""
    }

    subgraph_response = compiled_subgraph.invoke(subgraph_input)

    return {
        "user_query": state["user_query"],
        "final_answer": subgraph_response["analysis_result"]
    }


def build_parent_graph() -> StateGraph:
    """构建并编译父图（添加代理节点，而非直接添加子图）"""
    parent_builder = StateGraph(ParentState)
    parent_builder.add_node("call_subgraph_proxy", call_subgraph_proxy)
    parent_builder.add_edge(START, "call_subgraph_proxy")
    parent_builder.add_edge("call_subgraph_proxy", END)
    return parent_builder.compile()


def main():
    parent_graph = build_parent_graph()

    initial_state = {
        "user_query": "请分析Python中StateGraph的使用场景",
        "final_answer": None
    }
    print("父图初始状态：", initial_state)

    final_state = parent_graph.invoke(initial_state)

    print("\n父图最终状态：", final_state)
    print("\n子图处理后的最终答案：", final_state["final_answer"])


if __name__ == "__main__":
    main()
