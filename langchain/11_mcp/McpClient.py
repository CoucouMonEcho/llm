import asyncio
import json
import os
import logging
from typing import Any, Dict
from langchain.chat_models import init_chat_model
from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mcp_adapters.client import MultiServerMCPClient

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def load_servers(file_path: str = "mcp.json") -> Dict[str, Any]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data.get("servers", {})


async def run_chat_loop() -> None:
    servers = load_servers()

    mcp_client = MultiServerMCPClient(servers)
    tools = await mcp_client.get_tools()
    logger.info(f"已加载  {len(tools)} 个 MCP 工具:{[t.name for t in tools]}")

    model = init_chat_model(
        "qwen2.5:14b",
        model_provider="ollama",
        base_url="http://localhost:11434",
        reasoning=False
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个助手，使用提供的工具完成用户请求。"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ])

    agent = create_openai_tools_agent(model, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors="解析请求失败，请重新输入。"
    )

    logger.info("\nMCPAgent 已启动，请先输入一个提问给(LLM+MCP)，输入 'quit' 退出")
    while True:
        user_input = input("\nuser: ").strip()
        if user_input.lower() == "quit":
            break
        try:
            res = await agent_executor.ainvoke({"input": user_input})
            print(f"\nAI:{res['output']}")
        except Exception as e:
            logger.error(f"\n出错:{e}")

    logger.info("\nbye")


if __name__ == "__main__":
    asyncio.run(run_chat_loop())

# 北京的天气怎么样？
# 总结这篇文档```https://github.langchain.ac.cn/langgraph/reference/mcp/```