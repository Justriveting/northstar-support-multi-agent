import uuid


# Creates a new customer support ticket
def create_ticket(customer_name, question, additional_info):

    # Organizes the customer information into a ticket dictionary
    ticket = {
        "id": uuid.uuid4().hex[:8],
        "customer_name": customer_name,
        "question": question,
        "additional_info": additional_info,
        "status": "open"
    }

    # Returns the completed ticket to the rest of the program
    return ticket