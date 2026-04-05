from functools import partial
from typing import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy
from requests import RequestException, Timeout


class GraphState(TypedDict):
    process_data: dict  # 默认更新策略


def input_node(state: GraphState) -> GraphState:
    print(f'input_node收到的初始值:{state}')
    return {"process_data": {"input": "input_value"}}


def process_node(state: dict, param1: int, param2: str) -> dict:
    print(state, param1, param2)
    return {"process_data": {"process": "process_value"}}


retry_policy = RetryPolicy(
    # 最大重试次数
    max_attempts=3,
    # 初始间隔
    initial_interval=1,
    # 抖动（添加随机性避免重试风暴）
    jitter=True,
    # 退避乘数（每次重试间隔时间的增长倍数）
    backoff_factor=2,
    # 只重试这些异常
    retry_on=[RequestException, Timeout]
)

stateGraph = StateGraph(GraphState)
stateGraph.add_node("input", input_node)
process_with_params = partial(process_node, param1=100, param2="test")
stateGraph.add_node("process", process_with_params, retry=retry_policy)

stateGraph.add_edge(START, "input")
stateGraph.add_edge("input", "process")
stateGraph.add_edge("process", END)

graph = stateGraph.compile()

print(stateGraph.edges)
print(stateGraph.nodes)
print(graph.get_graph().print_ascii())

print()

initial_state = {"process_data": 5}
result = graph.invoke(initial_state)
print(f"最后的结果是:{result}")
