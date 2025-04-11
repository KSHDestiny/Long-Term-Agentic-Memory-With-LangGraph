from langchain_ollama import ChatOllama

llm = ChatOllama(
    model = "llama3.2:latest",
    temperature = 0.8
)

llm_json = ChatOllama(
    model = "llama3.2:latest",
    temperature = 0,
    format="json"
)