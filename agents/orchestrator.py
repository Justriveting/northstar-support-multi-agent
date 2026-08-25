# Northstar Support Co. - Orchestrator Agent
# Temporary prompt until the Prompt Engineer provides the final version.

from langchain.agents import create_agent
from prompts import ROUTER_PROMPT
from graph_state import create_shared_state
from config import llm
from tools.specialists import (
    ask_billing_specialist,
    ask_dental_specialist,
    ask_benefits_specialist,
    review_draft_response,
) 

# TODO: Tayo, determine which prompt you want to use OR combine both prompts to one better prompt. 
# Make sure to put the final prompt in the prompts.py file
ORCHESTRATOR_PROMPT = """
You are the Orchestrator Agent for Northstar Support Co.,
a health benefits support service.

Your job is to:

1. Receive an employee support question.
2. Determine what type of support is needed.
3. Route the request to the appropriate specialist agent.
4. Collect the output from the specialist agent.
5. Coordinate review of the response.
6. Use the approved information to produce the final response.

Current possible routes:
- billing
- dental
- benefits_coverage
- human_review

Do not make up health plan information.
If a request cannot be safely routed or answered using available
policy information, category it for human review.
"""


       

def category_request(state):
    """
    Temporary routing logic for the Orchestrator.
    This will later be replaced with LLM-based routing
    using the final prompt from the Prompt Engineer.
    """

    ticket = state["ticket"].lower()

    if "dental" in ticket or "dentist" in ticket:
        state["category"] = "dental"

    elif "bill" in ticket or "claim" in ticket or "deductible" in ticket:
        state["category"] = "billing"

    elif "coverage" in ticket or "eligible" in ticket or "doctor" in ticket:
        state["category"] = "benefits_coverage"

    else:
        state["category"] = "human_review"
        state["human_review"] = True

    return state
        
def send_to_specialist(state):
    """Send the ticket to the specialist selected by the orchestrator."""

    category = state["category"]
    ticket = state["ticket"]

    if category == "dental":
        state["specialist_output"] = ask_dental_specialist.invoke(
            {"question": ticket}
        )

    elif category == "billing":
        state["specialist_output"] = ask_billing_specialist.invoke(
            {"question": ticket}
        )

    elif category == "benefits_coverage":
        state["specialist_output"] = ask_benefits_specialist.invoke(
            {"question": ticket}
        )

    elif category == "human_review":
        state["specialist_output"] = None
        state["human_review"] = True

    return state
def review_specialist_output(state):
    """Send the specialist response to the critic for review."""

    if state.get("human_review"):
        return state

    specialist_output = state.get("specialist_output")

    if not specialist_output:
        state["critic_status"] = "RETRY"
        state["critic_feedback"] = "No specialist response was produced."
        return state

    critic_result = review_draft_response.invoke(
        {"draft_data": specialist_output}
    )
    state["critic_feedback"] = critic_result

    # Capture the critic's decision in shared state
    critic_text = str(critic_result)

    if '"decision": "APPROVE"' in critic_text:
        state["critic_status"] = "APPROVE"

    elif '"decision": "RETRY"' in critic_text:
        state["critic_status"] = "RETRY"

    elif '"decision": "ESCALATE"' in critic_text:
        state["critic_status"] = "ESCALATE"
        state["human_review"] = True

    else:
        state["critic_status"] = "UNKNOWN"

    return state
def handle_critic_decision(state):
    """
    Handle the critic's decision after reviewing a specialist response.
    """

    decision = state.get("critic_status")

    if decision == "APPROVE":
        state["final_response"] = state.get("specialist_output")
        state["human_review"] = False

    elif decision == "RETRY":
        state["retry_count"] += 1

        if state["retry_count"] >= 2:
            state["critic_status"] = "ESCALATE"
            state["human_review"] = True
        else:
            state = send_to_specialist(state)
            state = review_specialist_output(state)

            if state.get("critic_status") != "APPROVE":
                state["critic_status"] = "ESCALATE"
                state["human_review"] = True
            else:
                state["final_response"] = state.get("specialist_output")

    elif decision == "ESCALATE":
        state["human_review"] = True

    else:
        state["critic_status"] = "ESCALATE"
        state["human_review"] = True

    return state
     
# Final Router / Orchestrator Agent
router_agent = create_agent(
    model=llm,
    tools=[
    ],
    system_prompt=ROUTER_PROMPT
)

