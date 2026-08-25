# Northstar Support Co. - Application Entry Point

from graph_state import create_shared_state
from agents.orchestrator import (
    category_request,
    send_to_specialist,
    review_specialist_output,
    handle_critic_decision,
)


def main():
    ticket = input("Enter an employee benefits question: ").strip()

    # 1. Create shared state
    state = create_shared_state(ticket)

    # 2. Orchestrator classifies the ticket
    state = category_request(state)

    # Human-review tickets stop before specialist processing
    if state.get("category") == "human_review":
        state["human_review"] = True
        print("\nNorthstar Support Response:")
        print("This request requires human review.")
        return

    # 3. Send ticket to appropriate specialist
    state = send_to_specialist(state)

    # 4. Critic reviews specialist response
    state = review_specialist_output(state)

    # 5. Orchestrator handles critic decision
    state = handle_critic_decision(state)

    # 6. Display final result
    print("\nNorthstar Support Response:")

    if state.get("human_review"):
        print("This request has been escalated for human review.")

    elif state.get("final_response"):
        print(state["final_response"])

    else:
        print(state.get("specialist_output", "No response available."))


if __name__ == "__main__":
    main()