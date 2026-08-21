# Northstar Support Co. - Orchestrator Agent
# Temporary prompt until the Prompt Engineer provides the final version.

from langchain.agent import create_agent
from prompts import ROUTER_PROMPT

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

def create_state(ticket):
    """
    Create the shared state that follows a support request
    through the multi-agent workflow.
    """
    return {
        "ticket": ticket,
        "category": None,
        "specialist_output": None,
        "critic_status": None,
        "critic_feedback": None,
        "retry_count": 0,
        "human_review": False,
        "final_response": None
    }

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
    """
    Placeholder for sending the request to the routed specialist agent.
    The real specialist agent functions will be connected later.
    """

    category = state["category"]

    if category == "dental":
        state["specialist_output"] = "Placeholder response from Dental Agent."

    elif category == "billing":
        state["specialist_output"] = "Placeholder response from Billing Agent."

    elif category == "benefits_coverage":
        state["specialist_output"] = "Placeholder response from Benefits Coverage Agent."

    elif category == "human_review":
        state["specialist_output"] = None

    return state

# Final Router / Orchestrator Agent
router_agent = create_agent(
    model=llm,
    tools=[
        ask_billing_specialist, 
        ask_dental_specialist, 
        ask_benefits_specialist, 
        review_draft_response
    ],
    system_prompt=ROUTER_PROMPT
)

if __name__ == "__main__":
    ticket = input("Enter an employee benefits question: ")

    state = create_state(ticket)
    state = category_request(state)
    state = send_to_specialist(state)

    print("\nOrchestrator Result:")
    print(state)
    