from dotenv import load_dotenv

from langgraph.graph import StateGraph, START
from state import State
from IPython.display import Image, display
from helper import triage_router
from emails import email1, email2
from memory import store
from config import config
from agent import response_agent

_ = load_dotenv()

email_agent = StateGraph(State)
email_agent = email_agent.add_node(triage_router)
email_agent = email_agent.add_node("response_agent", response_agent)
email_agent = email_agent.add_edge(START, "triage_router")
email_agent = email_agent.compile(store=store)

display(Image(email_agent.get_graph(xray=True).draw_mermaid_png()))

response = email_agent.invoke({"email_input": email1}, config=config)
response = email_agent.invoke({"email_input": email2}, config=config)

for m in response["messages"]:
    m.pretty_print()