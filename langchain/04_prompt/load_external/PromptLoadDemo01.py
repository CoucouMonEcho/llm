from langchain_core.prompts import load_prompt

template = load_prompt("prompt.json", encoding="utf-8")
print(template.format(name="不死川梨华", what="搞笑"))
