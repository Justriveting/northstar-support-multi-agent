from langchain.agents import create_agent
from langchain.tools import tool
from config import llm


# 1. SPECIALIST SYSTEM PROMPTS AND RULES TO FOLLOW

SPECIALIST_BILLING_PROMPT = """You are a TPA Billing & Claims Specialist. Answer the employee's billing question using ONLY the provided context.

Rules:
1. Do NOT offer legal or financial planning advice.
2. If mathematical calculations are required (deductibles, coinsurance), show the step-by-step arithmetic.
3. If the context lacks necessary information, reply strictly with: "INSUFFICIENT_CONTEXT" """


SPECIALIST_DENTAL_PROMPT = """You are a TPA Dental Coverage Specialist. Answer the employee's question using ONLY the provided context.

Rules:
1. Do NOT provide dental diagnostic or medical advice.
2. Explicitly distinguish between in-network and out-of-network coverage rules.
3. If the context lacks necessary information, reply strictly with: "INSUFFICIENT_CONTEXT" """


SPECIALIST_BENEFITS_PROMPT = """You are a TPA Benefits & Coverage Specialist. Answer the employee's question using ONLY the provided context.

Rules:
1. Do NOT provide medical advice or evaluate clinical symptoms.
2. Detail applicable copays, deductibles, or zero-cost preventive rules clearly.
3. If the context lacks necessary information, reply strictly with: "INSUFFICIENT_CONTEXT" """


# CRITIC & SYNTHESIZER SYSTEM PROMPTS

CRITIC_PROMPT = """You are a TPA Compliance & Quality Audit Critic evaluating an AI Specialist's draft output.

Audit Checklist:
1. GROUNDEDNESS: Is every claim supported by the provided context?
2. SAFETY: Does the output refrain from offering direct medical, legal, or financial advice?
3. COMPLETENESS: Does the draft directly answer the employee's core question?

Output strictly valid JSON:
{
  "decision": "PASS" | "RETRY" | "ESCALATE",
  "reasoning": "Explanation of audit finding",
  "critic_feedback": "Specific instructions if RETRY, or empty string if PASS"
}"""


SYNTHESIZER_PROMPT = """You are the primary TPA Customer Support Assistant.
Format the approved specialist response into a clear, empathetic, and professional message for the employee.
Remove internal process labels, database IDs, or system jargon."""


# ROUTER / ORCHESTRATOR SYSTEM PROMPT

ROUTER_PROMPT = """You are an expert TPA Benefits Query Router.
Analyze the employee's input question and classify the primary intent into one or more categories:
- BILLING (claims, out-of-pocket costs, deductibles, coinsurance, reimbursements)
- DENTAL (cleanings, fillings, orthodontia, dental networks)
- BENEFITS (copays, preventive care, coverage eligibility, physicals)

Output strictly valid JSON:
{
  "category": "billing" | "dental" | "benefits_coverage" | "human_review",
  "reasoning": "Brief justification for classification"
}"""


# AGENT INITIALIZATION

billing_agent = create_agent(
    model=llm,
    system_prompt=SPECIALIST_BILLING_PROMPT
)

dental_agent = create_agent(
    model=llm,
    system_prompt=SPECIALIST_DENTAL_PROMPT
)

benefits_agent = create_agent(
    model=llm,
    system_prompt=SPECIALIST_BENEFITS_PROMPT
)

critic_agent = create_agent(
    model=llm,
    system_prompt=CRITIC_PROMPT
)

synthesizer_agent = create_agent(
    model=llm,
    system_prompt=SYNTHESIZER_PROMPT
)



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
