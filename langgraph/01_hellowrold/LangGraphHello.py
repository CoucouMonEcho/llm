from typing import TypedDict
from langgraph.graph import StateGraph, START, END
import uuid


class HelloState(TypedDict):
    name: str
    greeting: str


def greet(h: HelloState) -> dict:
    name = h["name"]
    return {"greeting": f"Hello, {name}!"}


def add_haha(h: HelloState) -> dict:
    greeting = h["greeting"]
    return {"greeting": f"{greeting}...haha!"}


graph = StateGraph(HelloState)

graph.add_node("greeting", greet)
graph.add_node("add_emoji", add_haha)

graph.add_edge(START, "greeting")
graph.add_edge("greeting", "add_emoji")
graph.add_edge("add_emoji", END)

app = graph.compile()

res = app.invoke({"name": "z3"})
print(res)
print(res["greeting"])
print("=" * 50)

# img
print(app.get_graph().print_ascii())
# https://www.processon.com/mermaid
print(app.get_graph().draw_mermaid())

# png_bytes = app.get_graph().draw_mermaid_png(max_retries=2,retry_delay=2.0)
# output_path = "./img/langgraph" + str(uuid.uuid4())[:8] + ".png"
# with open(output_path, "wb") as f:
#     f.write(png_bytes)
# print(f"图片已生成：{output_path}")