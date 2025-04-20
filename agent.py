from model import llm
from langgraph.prebuilt import create_react_agent
from langgraph.prompts import create_prompt
from langgraph.tools import write_email, schedule_meeting, check_calendar_availability
from memory import manage_memory_tool, search_memory_tool, store

tools=[write_email, schedule_meeting, check_calendar_availability, manage_memory_tool, search_memory_tool]

response_agent = create_react_agent(
    llm,
    tools=tools,
    prompt=create_prompt,
    store=store
)