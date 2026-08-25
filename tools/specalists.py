from langchain.tools import tool
from agents.sub_agents import billing_agent, dental_agent, benefits_agent, critic_agent

# SPECIALIST TOOLS

@tool
def ask_billing_specialist(question: str) -> str:
    """Ask the billing specialist about claims, out-of-pocket costs, deductibles, coinsurance, and reimbursements."""
    print(f"[orchestrator] -> billing_specialist: {question}")
    result = billing_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content


@tool
def ask_dental_specialist(question: str) -> str:
    """Ask the dental specialist about cleanings, fillings, orthodontia, and dental networks."""
    print(f"[orchestrator] -> dental_specialist: {question}")
    result = dental_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content


@tool
def ask_benefits_specialist(question: str) -> str:
    """Ask the benefits specialist about copays, preventive care, coverage eligibility, and physicals."""
    print(f"[orchestrator] -> benefits_specialist: {question}")
    result = benefits_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].content


@tool
def review_draft_response(draft_data: str) -> str:
    """Audit a specialist draft response for compliance, safety, and factual accuracy."""
    print(f"[orchestrator] -> critic_reviewer: {draft_data}")
    result = critic_agent.invoke({"messages": [{"role": "user", "content": draft_data}]})
    return result["messages"][-1].content