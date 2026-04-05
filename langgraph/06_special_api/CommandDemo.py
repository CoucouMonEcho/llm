from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

RECURSION_LIMIT = 50


class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    current_agent: str
    task_completed: bool


def decision_agent(state: AgentState) -> Command[AgentState]:
    """根据消息内容路由代理，任务完成则直接终止"""
    print("执行节点: decision_agent")
    if state["task_completed"]:
        print("✅ 检测到任务已完成，直接终止流程")
        return Command(
            update={"messages": [("system", "所有任务处理完成，流程正常结束")]},
            goto=END
        )
    last_message = state["messages"][-1] if state["messages"] else ("", "")
    last_msg_content = last_message[1]
    print(f"最新消息文本: {last_msg_content}")

    if "数学" in last_msg_content:
        print("✅ 检测到数学任务，路由到数学代理")
        return Command(
            update={"messages": [("system", "路由到数学代理")], "current_agent": "math_agent"},
            goto="math_agent"
        )
    elif "翻译" in last_msg_content:
        print("✅ 检测到翻译任务，路由到翻译代理")
        return Command(
            update={"messages": [("system", "路由到翻译代理")], "current_agent": "translation_agent"},
            goto="translation_agent"
        )
    else:
        print("❌ 未识别任务类型，标记任务完成并终止")
        return Command(
            update={"messages": [("system", "任务完成")], "task_completed": True},
            goto=END
        )


def math_agent(state: AgentState) -> Command[AgentState]:
    """处理数学计算任务，完成后返回决策代理"""
    print("执行节点: math_agent")
    result = "2 + 2 = 4"
    print(f"计算结果: {result}")
    return Command(
        update={
            "messages": [("assistant", f"数学计算结果: {result}")],
            "current_agent": "decision_agent",
            "task_completed": True
        },
        goto="decision_agent"
    )


def translation_agent(state: AgentState) -> Command[AgentState]:
    """处理中英翻译任务，完成后返回决策代理"""
    print("执行节点: translation_agent")
    translation = "Hello -> 你好"
    print(f"翻译结果: {translation}")
    return Command(
        update={
            "messages": [("assistant", f"翻译结果: {translation}")],
            "current_agent": "decision_agent",
            "task_completed": True
        },
        goto="decision_agent"
    )


def main():
    """Command基础用法：状态更新+动态路由+流程终止"""

    builder = StateGraph(AgentState)
    builder.add_node("decision_agent", decision_agent)
    builder.add_node("math_agent", math_agent)
    builder.add_node("translation_agent", translation_agent)

    builder.add_edge(START, "decision_agent")
    # builder.add_edge("math_agent", "decision_agent")
    # builder.add_edge("translation_agent", "decision_agent")
    builder.add_edge("decision_agent", END)

    graph = builder.compile()

    print("【测试1: 数学任务】")
    initial_state = {"messages": [("user", "我需要计算数学题")], "current_agent": "user", "task_completed": False}
    print("初始状态:", initial_state)
    result = graph.invoke(initial_state, recursion_limit=RECURSION_LIMIT)
    print("最终状态(简化):", {k: v for k, v in result.items() if k != "messages"})  # 简化输出
    print("\n" + "-" * 50 + "\n")

    print("【测试2: 翻译任务】")
    initial_state = {"messages": [("user", "我需要翻译文本")], "current_agent": "user", "task_completed": False}
    print("初始状态:", initial_state)
    result = graph.invoke(initial_state, recursion_limit=RECURSION_LIMIT)
    print("最终状态(简化):", {k: v for k, v in result.items() if k != "messages"})
    print("\n" + "-" * 50 + "\n")

    print("【测试3: 未识别任务类型】")
    initial_state = {"messages": [("user", "你好")], "current_agent": "user", "task_completed": False}
    print("初始状态:", initial_state)
    result = graph.invoke(initial_state, recursion_limit=RECURSION_LIMIT)
    print("最终状态(简化):", {k: v for k, v in result.items() if k != "messages"})

    print(graph.get_graph().print_ascii())
    # https://www.processon.com/mermaid
    print(graph.get_graph().draw_mermaid())


if __name__ == "__main__":
    main()
