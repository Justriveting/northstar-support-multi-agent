"""
Northstar Support Co. - Approval Rate Measurement

Runs a batch of representative fictional support tickets through the full
graph and tallies how many get auto-approved (critic PASS) versus escalated
to a human (critic ESCALATE, retry cap exceeded, or the router itself
flagging human_review). Used to back the "~85% auto-approved" claim in the
stakeholder pitch deck with real numbers instead of a guess.

This is a small sample of test tickets, not real production volume -- treat
the resulting percentage as "what we observed in testing," not a measured
production accuracy rate.
"""

from graph_state import create_shared_state
from ticket import create_ticket
from workflow import graph

TEST_TICKETS = [
    # billing
    ("Alex Kim", "What is my deductible for an in-network visit?", "No prior claims this year."),
    ("Alex Kim", "How much coinsurance do I pay after my deductible is met?", ""),
    ("Alex Kim", "How long does it take for a claim to be processed?", ""),
    ("Alex Kim", "Can I get reimbursed for an out-of-network specialist visit?", ""),
    ("Alex Kim", "What is my out-of-pocket maximum for the year?", ""),
    # dental
    ("Jamie Lee", "Is my annual dental cleaning covered?", "Visited an in-network dentist."),
    ("Jamie Lee", "How much of a filling does insurance cover?", ""),
    ("Jamie Lee", "Does my plan cover orthodontia for my kid?", ""),
    ("Jamie Lee", "Is teeth whitening covered under my dental plan?", ""),
    ("Jamie Lee", "What's the lifetime maximum for orthodontic coverage?", ""),
    # benefits_coverage
    ("Morgan Diaz", "Is my annual physical covered at no cost?", ""),
    ("Morgan Diaz", "What is my copay for a specialist visit?", ""),
    ("Morgan Diaz", "When am I eligible for coverage as a new hire?", ""),
    ("Morgan Diaz", "What is my copay for a primary care visit?", ""),
    ("Morgan Diaz", "Does my plan cover a second opinion from a specialist?", ""),
    # ambiguous / edge cases likely to need a human
    ("Riley Chen", "I think my last paycheck was wrong, can you fix it?", ""),
    ("Riley Chen", "My doctor wants to run a test that isn't listed anywhere, is it covered?", ""),
    ("Riley Chen", "I'm not sure what kind of question this is, can someone call me?", ""),
]


def main():
    results = []

    for customer_name, question, additional_info in TEST_TICKETS:
        ticket = create_ticket(customer_name, question, additional_info)
        state = create_shared_state(ticket)
        result = graph.invoke(state)

        outcome = "escalated" if result["human_review"] else "auto_approved"
        results.append({
            "ticket_id": ticket["id"],
            "question": question,
            "category": result["category"],
            "critic_status": result["critic_status"],
            "retry_count": result["retry_count"],
            "outcome": outcome,
        })

    total = len(results)
    auto_approved = sum(1 for r in results if r["outcome"] == "auto_approved")
    escalated = total - auto_approved

    print()
    print(f"{'Ticket':<10} {'Category':<18} {'Critic':<10} {'Retries':<8} {'Outcome'}")
    for r in results:
        print(f"{r['ticket_id']:<10} {str(r['category']):<18} {str(r['critic_status']):<10} {r['retry_count']:<8} {r['outcome']}")

    print()
    print(f"Total tickets:     {total}")
    print(f"Auto-approved:     {auto_approved} ({auto_approved / total:.0%})")
    print(f"Escalated:         {escalated} ({escalated / total:.0%})")


if __name__ == "__main__":
    main()
