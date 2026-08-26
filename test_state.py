from ticket import create_ticket
from graph_state import create_shared_state


ticket = create_ticket(
    customer_name="John Smith",
    question="Why was I charged twice?",
    additional_info="I placed my order yesterday."
)


state = create_shared_state(ticket)


print(state)