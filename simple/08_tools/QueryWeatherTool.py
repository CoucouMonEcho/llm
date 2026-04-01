from langchain.tools import tool
import json
import os
import httpx
from dotenv import load_dotenv

load_dotenv(encoding='utf-8', override=True)
api_key = os.getenv("OPENWEATHER_API_KEY")


@tool
def get_weather(loc):
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
    return json.dumps(data)


if __name__ == '__main__':
    res = get_weather.invoke("beijing")
    print(res)
