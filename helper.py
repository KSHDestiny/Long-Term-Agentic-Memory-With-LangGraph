from model import llm, llm_json
from prompts import triage_system_prompt, triage_user_prompt
from setup import profile, prompt_instructions
from langgraph.graph import END
from langgraph.types import Command
from state import State
from typing import Literal
from typing_extensions import Literal
from router import Router
import re

def triage_router(state: State) -> Command[
    Literal["response_agent", "__end__"]
]:
    author = state['email_input']['author']
    to = state['email_input']['to']
    subject = state['email_input']['subject']
    email_thread = state['email_input']['email_thread']

    system_prompt = triage_system_prompt.format(
        full_name=profile["full_name"],
        name=profile["name"],
        user_profile_background=profile["user_profile_background"],
        triage_no=prompt_instructions["triage_rules"]["ignore"],
        triage_notify=prompt_instructions["triage_rules"]["notify"],
        triage_email=prompt_instructions["triage_rules"]["respond"],
        examples=None
    )
    user_prompt = triage_user_prompt.format(
        author=author, 
        to=to, 
        subject=subject, 
        email_thread=email_thread
    )

    response = llm.invoke(
        [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
    )

    print("User Response:", response.content)

    user_prompt = f"""
        You are an AI assistant that classifies emails into one of three categories: "ignore", "respond", or "notify".

        Respond ONLY with a valid JSON object using the following format:
        {{
        "reasoning": "...",
        "classification": "respond"  // or "ignore", or "notify"
        }}

        Content:
        {response.content}
    """

    response = llm_json.invoke([
        {"role": "system", "content": "You classify emails based on their content."},
        {"role": "user", "content": user_prompt}
    ])

    print("Model Response:", response.content)

    try:
        json_match = re.search(r"\{.*\}", response.content, re.DOTALL)
        if json_match:
            json_data = json_match.group()
            result = Router.parse_raw(json_data)
            print("✅ Classification:", result.classification)
        else:
            print("❌ No JSON found:", response.content)
    except Exception as e:
        print("❌ Parsing failed:", e)
        print("Model output:", response.content)

    if result.classification == "respond":
        print("📧 Classification: RESPOND - This email requires a response")
        goto = "response_agent"
        update = {
            "messages": [
                {
                    "role": "user",
                    "content": f"Respond to the email {state['email_input']}",
                }
            ]
        }
    elif result.classification == "ignore":
        print("🚫 Classification: IGNORE - This email can be safely ignored")
        update = None
        goto = END
    elif result.classification == "notify":
        print("🔔 Classification: NOTIFY - This email contains important information")
        update = None
        goto = END
    else:
        raise ValueError(f"Invalid classification: {result.classification}")
    return Command(goto=goto, update=update)

