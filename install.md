### 1. 创建虚拟环境

- python -m venv .venv

### 2. 激活虚拟环境

#### 2.1. Windows

- .venv\Scripts\activate

#### 2.2. Linux / macOS

- source .venv/bin/activate

### 3. 安装依赖

- pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
- pip install langchain
- pip install langchain-openai
- pip install openai
- pip install python-dotenv
- pip install langchain-core
- pip install -qU langchain-ollama
- pip install -U ollama

### 4. 锁定和重安装依赖

- pip freeze > requirements.txt
- pip install -r requirements.txt
