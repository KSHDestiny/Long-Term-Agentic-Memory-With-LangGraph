from langgraph.graph import add_messages
from typing_extensions import TypedDict, Annotated

class State(TypedDict):
    email_input: dict
    messages: Annotated[list, add_messages]