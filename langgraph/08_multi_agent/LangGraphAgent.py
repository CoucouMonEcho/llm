from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage
from langchain.agents import create_agent


def get_weather(city: str) -> str:
    """获取指定城市的天气信息。
        Args:
            city: 城市名称
        Returns:
            返回该城市的天气描述
    """
    return f"今天{city}是晴天，仅做测试，固定写死"


model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

agent = create_agent(
    model=model,
    tools=[get_weather]
)

# <class 'langgraph.graph.state.CompiledStateGraph'>
print(type(agent))

human_message = HumanMessage(content="今天深圳天气怎么样？")
response = agent.invoke({"messages": [human_message]})

print(response)
print()
print("模型回答：", response["messages"][-1].content)
print()
response["messages"][-1].pretty_print()
