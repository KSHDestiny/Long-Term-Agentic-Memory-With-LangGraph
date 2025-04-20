from langgraph.store.memory import InMemoryStore
from langchain_ollama import OllamaEmbeddings
from langmem import create_manage_memory_tool, create_search_memory_tool

embedding = OllamaEmbeddings(model="mxbai-embed-large")

store = InMemoryStore(index={"embed": embedding})

manage_memory_tool = create_manage_memory_tool(
    namespace=(
        "email_assistant", 
        "{langgraph_user_id}",
        "collection"
    )
)
search_memory_tool = create_search_memory_tool(
    namespace=(
        "email_assistant",
        "{langgraph_user_id}",
        "collection"
    )
)

print(manage_memory_tool.name)
print(manage_memory_tool.description)
print(manage_memory_tool.args)

print(search_memory_tool.name)
print(search_memory_tool.description)
print(search_memory_tool.args)