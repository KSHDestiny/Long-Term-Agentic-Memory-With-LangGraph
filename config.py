from agent import response_agent
from memory import store

config = {"configurable": {"langgraph_user_id": "lance"}}

response = response_agent.invoke(
    {"messages": [{"role": "user", "content": "Jim is my friend"}]},
    config=config
)

for m in response["messages"]:
    m.pretty_print()

response = response_agent.invoke(
    {"messages": [{"role": "user", "content": "who is jim?"}]},
    config=config
)

for m in response["messages"]:
    m.pretty_print()

store.list_namespaces()
store.search(('email_assistant', 'lance', 'collection'))
store.search(('email_assistant', 'lance', 'collection'), query="jim")