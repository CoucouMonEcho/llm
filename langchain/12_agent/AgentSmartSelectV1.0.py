import json
import os

import httpx
import logging
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langchain.agents import create_agent
from dotenv import load_dotenv
from typing import TypedDict, cast, Any
from langchain.agents.structured_output import ToolStrategy


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


class WeatherCompareOutput(TypedDict):
    beijing_temp: float
    shanghai_temp: float
    hotter_city: str
    summary: str


model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

agent = create_agent(
    model=model,
    tools=[get_weather],
    system_prompt=("你是天气助手。用户询问多个城市天气时，分别调用工具获取数据，并比较分析。"
                   "最终必须返回 JSON，字段包括："
                   "beijing_temp, shanghai_temp, hotter_city, summary。"),
    # response_format=ToolStrategy(WeatherCompareOutput)
    response_format=WeatherCompareOutput
)

res = agent.invoke(cast(Any, {
    "messages": [
        {"role": "user", "content": "请问今天北京和上海的天气怎么样，哪个城市更热？"}
    ]
}))

print(res)
