from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime
from langchain_core.messages import AIMessage, HumanMessage
from dataclasses import dataclass


class AgentState(TypedDict):
    messages: Annotated[list, lambda x, y: x + y]
    response: str


@dataclass
class ContextSchema:
    model_name: str
    db_connection: str
    api_key: str


def process_message(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    """处理用户消息的节点，使用context中的信息"""
    print("执行节点: process_message")

    last_message = state["messages"][-1].content if state["messages"] else ""
    print(f"用户消息: {last_message}")

    model_name = runtime.context.model_name
    db_connection = runtime.context.db_connection
    api_key = runtime.context.api_key

    print(f"使用的模型: {model_name}")
    print(f"数据库连接: {db_connection}")
    print(f"API密钥前缀: {api_key[:5]}***")

    response = f"使用 {model_name} 处理了您的请求，已连接到 {db_connection}"

    return {
        "messages": [AIMessage(content=response)],
        "response": response
    }


def generate_response(state: AgentState, runtime: Runtime[ContextSchema]) -> dict:
    """生成最终响应的节点"""
    print("执行节点: generate_response")

    model_name = runtime.context.model_name
    print(f"使用模型 {model_name} 生成最终响应")

    previous_response = state["response"]

    final_response = f"{previous_response}\n\n这是使用 {model_name} 生成的完整响应。"

    return {
        "messages": [AIMessage(content=final_response)],
        "response": final_response
    }


def main():
    context = ContextSchema(
        model_name="gpt-4-turbo",
        db_connection="postgresql://user:pass@localhost:5432/orders_db",
        api_key="sk-abcdefghijklmnopqrstuvwxyz123456"
    )

    builder = StateGraph(AgentState, context_schema=ContextSchema)

    builder.add_node("process_message", process_message)
    builder.add_node("generate_response", generate_response)

    builder.add_edge(START, "process_message")
    builder.add_edge("process_message", "generate_response")
    builder.add_edge("generate_response", END)

    graph = builder.compile()

    initial_state = {
        "messages": [HumanMessage(content="请帮我查询最新的订单信息")],
        "response": ""
    }

    print("初始状态:", initial_state)
    print()
    print("上下文信息:\n", {
        "model_name": context.model_name,
        "db_connection": context.db_connection,
        "api_key": f"{context.api_key[:5]}***"
    })
    print("\n" + "-" * 50 + "\n")

    result = graph.invoke(initial_state, context=context)

    print("\n" + "=" * 50)
    print("最终状态:", result)
    print("\n最终响应:")
    print(result["response"])


if __name__ == "__main__":
    main()
