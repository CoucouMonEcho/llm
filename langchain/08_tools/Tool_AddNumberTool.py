from langchain.tools import tool
from pydantic import BaseModel, Field
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class FieldInfo(BaseModel):
    """定义假发运算所需的参数信息"""
    a: int = Field(description="第1个参数")
    b: int = Field(description="第2个参数")

# 通过args_schema定义参数信息，也可以定义name、description、return_direct参数
@tool(args_schema=FieldInfo)
def add_number(a: int, b: int) -> int:
    """两个整数相加"""
    return a + b


res = add_number.invoke({"a": 1, "b": 2})
logger.info(res)

logger.info(f"\n{add_number.name}\n{add_number.description}\n{add_number.args}\n{add_number.return_direct}")
# add_number.name='add_number'
# add_number.description='两个整数相加'
# add_number.args='{'a': {'title': 'A', 'type': 'integer'}, 'b': {'title': 'B', 'type': 'integer'}}'
# add_number.return_direct='False'


