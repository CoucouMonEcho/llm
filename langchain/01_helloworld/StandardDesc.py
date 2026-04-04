import os

from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.exceptions import LangChainException

load_dotenv(encoding='utf-8', override=True)

import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def init_llm_client() -> init_chat_model:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set")
    llm = init_chat_model(
        "qwen-plus",
        model_provider="openai",
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
        temperature=0.7,
        max_tokens=100,
    )
    return llm

def main():
    try:
        llm = init_llm_client()
        logger.info(f'llm is {llm}')

        question = "你是谁"
        response = llm.invoke(question)

        logger.info(f'question is {question}')
        logger.info(f'response is {response}')

        print("============================ stream ============================")

        responseStream = llm.stream("介绍下langchain，100字以内")
        for chunk in responseStream:
            print(chunk.content,end="")


    except ValueError as e:
        logger.error(f'ValueError: {str(e)}')
    except LangChainException as e:
        logger.error(f'LangChainException: {str(e)}')
    except Exception as e:
        logger.error(f'Exception: {str(e)}')

if __name__ == '__main__':
    main()
