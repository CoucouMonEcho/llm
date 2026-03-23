from langchain_ollama import ChatOllama

model = ChatOllama(
    base_url="http://localhost:11434",
    model="deepseek-r1:14b",
    reasoning=False
)

print(model.invoke("你是谁"))
