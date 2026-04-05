import time
from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class BasicState(TypedDict):
    topic: str
    joke: str


def refine_topic(state: BasicState):
    time.sleep(1)
    return {"topic": state["topic"] + " and cats"}


def generate_joke(state: BasicState):
    time.sleep(1)
    return {"joke": f"This is a joke about {state['topic']}"}


def main():
    graph = (
        StateGraph(BasicState)
        .add_node(refine_topic)
        .add_node(generate_joke)

        .add_edge(START, "refine_topic")
        .add_edge("refine_topic", "generate_joke")
        .add_edge("generate_joke", END)

        .compile()
    )

    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="updates"):
        print(chunk)

    print()

    for chunk in graph.stream({"topic": "ice cream"}, stream_mode="values"):
        print(chunk)


if __name__ == "__main__":
    main()
