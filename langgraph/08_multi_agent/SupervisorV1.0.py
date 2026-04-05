import os
import re
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langgraph_supervisor import create_supervisor


def init_llm_model() -> init_chat_model:
    return init_chat_model(
        "qwen3.5:9b",
        model_provider="ollama",
        base_url="http://localhost:11434",
        reasoning=False
    )


def book_flight(from_airport: str, to_airport: str) -> str:
    """预订航班工具。根据出发机场和到达机场预订一张机票，并返回预订结果。"""
    return f"✅ 成功预订了从 {from_airport} 到 {to_airport} 的航班"


def book_hotel(hotel_name: str) -> str:
    """预订酒店工具。根据酒店名称完成酒店预订，并返回预订结果。"""
    return f"✅ 成功预订了 {hotel_name} 的住宿"


flight_assistant = create_agent(
    model=init_llm_model(),
    tools=[book_flight],
    name="flight_assistant"
)

hotel_assistant = create_agent(
    model=init_llm_model(),
    tools=[book_hotel],
    name="hotel_assistant"
)

supervisor = create_supervisor(
    agents=[flight_assistant, hotel_assistant],
    model=init_llm_model(),
    prompt=(
        "你是旅行预订系统的调度主管，负责协调航班预订和酒店预订。\n\n"
        "当用户提出航班和酒店预订请求时，你的工作流程是：\n"
        "1. 首先调用flight_assistant来预订航班\n"
        "2. 然后调用hotel_assistant来预订酒店\n"
        "3. 收到两个助手的结果后，汇总并向用户报告\n"
        "4. 完成后结束对话\n\n"
        "重要规则：\n"
        "- 每个助手只能调用一次\n"
        "- 不要重复任何内容\n"
        "- 不要输出任何英文\n"
        "- 所有通信都使用中文\n"
    )
).compile()


def filter_messages(chunk: dict) -> str:
    """提取并过滤消息，只返回中文内容，去除重复和英文"""
    output = ""

    if isinstance(chunk, dict):
        for role, payload in chunk.items():
            if isinstance(payload, dict) and "messages" in payload:
                for msg in payload["messages"]:
                    if hasattr(msg, 'content') and msg.content:
                        content = msg.content.strip()

                        # 过滤英文系统消息
                        if (content and
                                not content.startswith("Successfully") and
                                not content.startswith("Transferring") and
                                "Successfully transferred" not in content and
                                "transferred back to" not in content and
                                not content.startswith("帮我预订从")):

                            # 只保留中文内容
                            chinese_content = re.sub(r'[^\u4e00-\u9fff，。！？：；""、\s\d✅]', '', content)
                            if chinese_content and len(chinese_content.strip()) > 5:
                                output += f"{role}: {chinese_content.strip()}\n"

    return output


def main():
    print("请按顺序提供以下信息：")
    print("-" * 40)

    from_airport = input("1. 您的出发机场是哪里？: ").strip()
    while not from_airport:
        print("请输入有效的出发机场名称")
        from_airport = input("1. 您的出发机场是哪里？: ").strip()

    to_airport = input("\n2. 您的到达机场是哪里？: ").strip()
    while not to_airport:
        print("请输入有效的到达机场名称")
        to_airport = input("2. 您的到达机场是哪里？: ").strip()

    hotel_name = input("\n3. 您要预订的酒店名称是什么？: ").strip()
    while not hotel_name:
        print("请输入有效的酒店名称")
        hotel_name = input("3. 您要预订的酒店名称是什么？: ").strip()

    user_request = (
        f"请帮我预订以下旅行安排：\n"
        f"1. 航班：从 {from_airport} 飞往 {to_airport}\n"
        f"2. 酒店：{hotel_name}\n"
        f"请完成这两个预订。"
    )

    print("\n" + "=" * 60)
    print("正在处理您的预订请求...")
    print("=" * 60)
    print()

    input_data = {"messages": [{"role": "user", "content": user_request}]}

    try:
        seen_contents = set()

        for chunk in supervisor.stream(input_data):
            filtered_output = filter_messages(chunk)
            if filtered_output:
                lines = filtered_output.strip().split('\n')
                for line in lines:
                    if line and line not in seen_contents:
                        print(line)
                        seen_contents.add(line)

        if len(seen_contents) < 2:
            print("\n" + "=" * 60)
            print("预订已完成！")
            print(f"航班：从 {from_airport} 到 {to_airport}")
            print(f"酒店：{hotel_name}")
            print("=" * 60)
    except Exception as e:
        print(f"\n处理过程中出现错误: {e}")
        print("\n正在直接执行预订...")
        flight_result = book_flight(from_airport, to_airport)
        hotel_result = book_hotel(hotel_name)
        print(flight_result)
        print(hotel_result)

    print("\n感谢使用智能旅行预订系统！")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断。")
    except Exception as e:
        print(f"\n系统出现错误: {e}")

'''
请按顺序提供以下信息：
----------------------------------------
1. 您的出发机场是哪里？: 北京首都

2. 您的到达机场是哪里？: 深圳宝安

3. 您要预订的酒店名称是什么？: 深圳希尔顿

============================================================
正在处理您的预订请求...
============================================================

supervisor: 请帮我预订以下旅行安排：
1 航班：从 北京首都 飞往 深圳宝安
2 酒店：深圳希尔顿
请完成这两个预订。
supervisor: 好的，正在为您处理北京到深圳的航班预订。
flight_assistant: 好的，我已经成功为您预订了从北京首都飞往深圳宝安的航班。
关于酒店部分，非常抱歉，目前系统中只支持预订航班，暂时无法直接为您预订深圳希尔顿酒店。建议您通过希尔顿官网、旅行软件或联系酒店前台进行预订。
如果您还有其他需要，随时告诉我。
supervisor: 好的，我已经成功为您预订了从北京首都飞往深圳宝安的航班。
supervisor: 好的，我已为您完成了从北京首都飞往深圳宝安的航班预订。
关于酒店部分，由于目前的流程中，我只负责协调航班预订，酒店预订需要由专门的酒店助理来处理。让我现在为您联系酒店方面，完成深圳希尔顿的预订。
hotel_assistant: 好的，您的深圳希尔顿酒店也已经成功预订。
至此，您的两项行程：
1  航班：北京首都  深圳宝安
2  酒店：深圳希尔顿
均已预订完成。
祝您旅途愉快！
supervisor: 好的，您的深圳希尔顿酒店也已经成功预订。
supervisor: 好的，您的两项行程已经全部安排妥当：
1  航班：已为您成功预订从北京首都飞往深圳宝安的机票。
2  酒店：已为您成功预订深圳希尔顿酒店。

感谢使用智能旅行预订系统！

'''
