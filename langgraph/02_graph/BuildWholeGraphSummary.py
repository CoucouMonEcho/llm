from typing import TypedDict
from langgraph.constants import START, END
from langgraph.graph import StateGraph

class GraphState(TypedDict):
    process_data: dict

def input_node(state: GraphState) -> GraphState:
    print(f"input_node节点执行state.get('process_data')方法结果:  {state.get('process_data')}")
    return {"process_data": {"input": "input_value"}}

def process_node(state: dict) -> dict:
    print(f"process_node节点执行state.get('process_data')方法结果:  {state.get('process_data')}")
    return {"process_data": {"process": "process_value"}}

def output_node(state: GraphState) -> GraphState:
    print(f"output_node节点执行state.get('process_data')方法结果:  {state.get('process_data')}")
    return {"process_data": state.get('process_data')}

graph = StateGraph(GraphState)

graph.add_node("input", input_node)
graph.add_node("process", process_node)
graph.add_node("output", output_node)

graph.add_edge(START, "input")
graph.add_edge("input", "process")
graph.add_edge("process", "output")
graph.add_edge("output", END)

app = graph.compile()

result = app.invoke({"process_data": {"name": "测试数据", "value": 123456}})
print(f"最后的结果是:{result}")

print(app.get_graph().print_ascii())
# https://www.processon.com/mermaid
print(app.get_graph().draw_mermaid())