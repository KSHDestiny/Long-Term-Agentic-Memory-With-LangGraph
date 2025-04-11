from dotenv import load_dotenv
from model import llm
from langgraph.prebuilt import create_react_agent
from langgraph.tools import write_email, schedule_meeting, check_calendar_availability
from langgraph.prompts import create_prompt
from langgraph.graph import StateGraph, START
from state import State
from IPython.display import Image, display
from helper import triage_router
from emails import email1, email2

_ = load_dotenv()

tools=[write_email, schedule_meeting, check_calendar_availability]

agent = create_react_agent(
    llm,
    tools=tools,
    prompt=create_prompt,
)

email_agent = StateGraph(State)
email_agent = email_agent.add_node(triage_router)
email_agent = email_agent.add_node("response_agent", agent)
email_agent = email_agent.add_edge(START, "triage_router")
email_agent = email_agent.compile()

display(Image(email_agent.get_graph(xray=True).draw_mermaid_png()))

response = email_agent.invoke({"email_input": email1})
response = email_agent.invoke({"email_input": email2})

for m in response["messages"]:
    m.pretty_print()