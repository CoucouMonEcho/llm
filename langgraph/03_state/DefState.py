from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class BasicState(TypedDict):
    """基本的 State定义"""
    user_input: str
    response: str
    count: int
    process_data: dict

basicState = StateGraph(BasicState)

basicState.add_edge(START, END)

app = basicState.compile()

initial_state = {
    "user_input": "a",
    "response": "resp",
    "count": 25,
    "process_data": {"k1": "v1"}
}

result = app.invoke(initial_state)
print("执行结果：", result)
