# Northstar Support Co. - Application Entry Point

from graph_state import create_shared_state
from ticket import create_ticket
from workflow import graph


def main():
    customer_name = input("Enter your name: ").strip()
    question = input("Enter your benefits question: ").strip()
    additional_info = input("Any additional info? (optional): ").strip()

    ticket = create_ticket(customer_name, question, additional_info)
    state = create_shared_state(ticket)

    result = graph.invoke(state)

    print("\nNorthstar Support Response:")

    if result["human_review"]:
        print("This request has been escalated for human review.")
    else:
        print(result["final_response"])


if __name__ == "__main__":
    main()
