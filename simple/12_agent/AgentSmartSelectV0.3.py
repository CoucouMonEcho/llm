import json
import os
import httpx
import logging
from langchain.chat_models import init_chat_model
from langchain_classic.agents import create_tool_calling_agent
from langchain_classic.agents import AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
api_key = os.getenv("OPENWEATHER_API_KEY")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@tool()
def get_weather(loc: str) -> str:
    """
        查询即时天气函数
        :param loc: 必要参数，字符串类型，用于表示查询天气的具体城市名称。
                    注意，中国的城市需要用对应城市的英文名称代替，例如如果需要查询北京市天气，
                    则 loc 参数需要输入 'Beijing'。
        :return: OpenWeather API 查询即时天气的结果。具体 URL 请求地址为：
                 https://api.openweathermap.org/users/sign_in。
                 返回结果对象类型为解析之后的 JSON 格式对象，并用字符串形式表示，
                 其中包含了全部重要的天气信息。
        """
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": loc,
        "appid": api_key,
        # 摄氏度
        "units": "metric",
        "lang": "zh_cn"
    }
    resp = httpx.get(url, params=params, timeout=30)
    data = resp.json()
    logger.info(f"查询{loc}天气结果:{data}")
    return json.dumps(data)


model = init_chat_model(
    "qwen2.5:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是天气助手，请根据用户的问题，给出相应的天气信息"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

tools = [get_weather]

agent = create_tool_calling_agent(model, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

res = agent_executor.invoke({"input": "请问今天北京和上海的天气怎么样，哪个城市更热？"})

print(res)