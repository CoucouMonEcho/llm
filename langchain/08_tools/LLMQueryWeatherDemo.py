from langchain.chat_models import init_chat_model
from langchain_core.output_parsers import StrOutputParser, JsonOutputKeyToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda
from QueryWeatherTool import get_weather
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

model = init_chat_model(
    "qwen3.5:9b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

model_with_tools = model.bind_tools([
    get_weather,
])

parser = JsonOutputKeyToolsParser(key_name=get_weather.name, first_tool_only=True)

get_weather_chain = model_with_tools | parser | get_weather
# print(get_weather_chain.invoke("你好，北京的天气怎么样？"))

output_prompt = ChatPromptTemplate.from_template(
    """你将收到一段JSON 格式的天气数据{weather_json}，请用简洁自然的方式将其转述给用户。以下是天气JS0N数据：
    请将其转换为中文天气描述，例如：
    “北京现在天气：多云，气温28°C，体感有点闷热(约32°C)，湿度75%，微风(东南风2米/秒)，
    能见度很好，大约10公里。建议穿短袖短裤。适合做户外运动。"""
)

output_parser = StrOutputParser()

output_chain = output_prompt | model | output_parser

full_chain = get_weather_chain | RunnableLambda(lambda x: {"weather_json": x}) | output_chain

res = full_chain.invoke("北京的天气怎么样？")
logger.info(res)