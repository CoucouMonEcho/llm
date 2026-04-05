from typing import TypedDict
from langgraph.graph import StateGraph, START
from langchain.chat_models import init_chat_model
import os


class State(TypedDict):
    query: str
    answer: str


def node(state: State):
    print("开始调用node节点")
    model = init_chat_model(
        "qwen3.5:9b",
        model_provider="ollama",
        base_url="http://localhost:11434",
        reasoning=False
    )
    llm_result = model.invoke([("user", state["query"])])
    print("\nllm invoke结束", end="\n\n")

    return {"answer": llm_result}


def main():
    graph = (
        StateGraph(state_schema=State)
        .add_node(node)
        .add_edge(START, "node")
        .compile()
    )

    inputs = {"query": "以下是一个200字的小学生作文，主题为我的一天："}

    for chunk, meta_data in graph.stream(inputs, stream_mode="messages"):
        # <class 'langchain_core.messages.ai.AIMessageChunk'>
        # print(type(chunk))
        print(chunk.content, end="")
        # print(chunk,end="")


if __name__ == '__main__':
    main()
