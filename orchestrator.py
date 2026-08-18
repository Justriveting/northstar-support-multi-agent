# Northstar Support Co. - Orchestrator Agent
# Temporary prompt until the Prompt Engineer provides the final version.

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
policy information, route it for human review.
"""

def create_state(user_question):
    """
    Create the shared state that follows a support request
    through the multi-agent workflow.
    """
    return {
        "user_question": user_question,
        "route": None,
        "specialist_output": None,
        "critic_status": None,
        "critic_feedback": None,
        "retry_count": 0,
        "human_review": False,
        "final_response": None
    }

def route_request(state):
    """
    Temporary routing logic for the Orchestrator.
    This will later be replaced with LLM-based routing
    using the final prompt from the Prompt Engineer.
    """

    question = state["user_question"].lower()

    if "dental" in question or "dentist" in question:
        state["route"] = "dental"

    elif "bill" in question or "claim" in question or "deductible" in question:
        state["route"] = "billing"

    elif "coverage" in question or "eligible" in question or "doctor" in question:
        state["route"] = "benefits_coverage"

    else:
        state["route"] = "human_review"
        state["human_review"] = True

    return state
        
def send_to_specialist(state):
    """
    Placeholder for sending the request to the routed specialist agent.
    The real specialist agent functions will be connected later.
    """

    route = state["route"]

    if route == "dental":
        state["specialist_output"] = "Placeholder response from Dental Agent."

    elif route == "billing":
        state["specialist_output"] = "Placeholder response from Billing Agent."

    elif route == "benefits_coverage":
        state["specialist_output"] = "Placeholder response from Benefits Coverage Agent."

    elif route == "human_review":
        state["specialist_output"] = None

    return state



if __name__ == "__main__":
    question = input("Enter an employee benefits question: ")

    state = create_state(question)
    state = route_request(state)
    state = send_to_specialist(state)

    print("\nOrchestrator Result:")
    print(state)
    