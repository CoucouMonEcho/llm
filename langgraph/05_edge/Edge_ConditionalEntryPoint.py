from typing import TypedDict
from langgraph.graph import StateGraph, START, END


class SimpleState(TypedDict):
    user_input: str
    response: str
    node_visited: str


def route_input(state: SimpleState) -> str:
    text = state["user_input"].lower()

    if "hello" in text or "hi" in text:
        return "greeting"
    elif "bye" in text or "exit" in text:
        return "farewell"
    else:
        return "question"


def handle_greeting(state: SimpleState) -> SimpleState:
    state["response"] = "你好！很高兴见到你！"
    state["node_visited"] = "greeting_node"
    return state


def handle_farewell(state: SimpleState) -> SimpleState:
    state["response"] = "再见！祝你有个美好的一天！"
    state["node_visited"] = "farewell_node"
    return state


def handle_question(state: SimpleState) -> SimpleState:
    state["response"] = "我听到了你的问题，需要更多帮助吗？"
    state["node_visited"] = "question_node"
    return state


def create_simple_graph():
    stateGraph = StateGraph(SimpleState)

    stateGraph.add_node("greeting_node", handle_greeting)
    stateGraph.add_node("farewell_node", handle_farewell)
    stateGraph.add_node("question_node", handle_question)

    stateGraph.add_conditional_edges(
        START,
        route_input,
        {
            "greeting": "greeting_node",
            "farewell": "farewell_node",
            "question": "question_node"
        }
    )

    stateGraph.add_edge("greeting_node", END)
    stateGraph.add_edge("farewell_node", END)
    stateGraph.add_edge("question_node", END)

    return stateGraph.compile()


def run_example():
    app = create_simple_graph()
    test_inputs = [
        "Hello everyone!",
        "Goodbye now",
        "What time is it?"
    ]

    for user_input in test_inputs:
        print(f"\n输入: {user_input}")
        print("-" * 30)

        initial_state = SimpleState(
            user_input=user_input,
            response="",
            node_visited=""
        )

        result = app.invoke(initial_state)

        print(f"路由决策: {route_input(initial_state)}")
        print(f"访问的节点: {result['node_visited']}")
        print(f"响应: {result['response']}")

    print()
    print(app.get_graph().print_ascii())
    # https://www.processon.com/mermaid
    print(app.get_graph().draw_mermaid())


if __name__ == "__main__":
    run_example()
