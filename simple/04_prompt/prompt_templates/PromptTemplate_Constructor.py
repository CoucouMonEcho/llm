from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

template = PromptTemplate(
    template="你是一个专业的{role}工程师，请根据我的问题给出回答，我的问题是：{question}",
    input_variables=['role', 'question']
)

prompt = template.format(role="Python开发", question="冒泡排序怎么写，只要代码其他不要，简洁回答")

print(prompt)

model = init_chat_model(
    "deepseek-r1:14b",
    model_provider="ollama",
    base_url="http://localhost:11434",
    reasoning=False
)

res = model.invoke(prompt)
print(res.content)
print("\n")
