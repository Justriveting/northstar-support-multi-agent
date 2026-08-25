# TODO: This is where the agent program will start
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph_state import create_shared_state
from agents.orchestrator import router_agent

def main():
    ticket = input("Enter an employee benefits question: ").strip()
    state = create_shared_state(ticket)

    result = router_agent.invoke(
    {
        "messages": [
            {
                "role": "user",
                "content": state["ticket"],
            }
        ]
    }
)
    final_response = result["messages"][-1].content
    state["final_response"] = final_response

    print("\nNorthstar Support Response:")
    print(state["final_response"])

if __name__ == "__main__":
    main()