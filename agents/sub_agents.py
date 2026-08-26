import json

from langchain.agents import create_agent
from config import llm
from graph_state import SupportState
from logger import log_exchange
from prompts import SPECIALIST_BENEFITS_PROMPT, SPECIALIST_BILLING_PROMPT, SPECIALIST_DENTAL_PROMPT, CRITIC_PROMPT
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


# LANGGRAPH NODE WRAPPERS

def _build_specialist_message(state: SupportState) -> str:
    """
    Builds the message sent to a specialist agent: the question, plus
    policy context if available, plus the critic's feedback if this is
    a retry -- so a retry can actually correct the previous mistake
    instead of just re-asking the same thing and getting the same answer.
    """
    question = state["ticket"]["question"]
    policy = state.get("policy")

    message = f"Employee question: {question}"

    if policy:
        message += f"\n\nPolicy context: {policy}"

    if state.get("critic_feedback") and state.get("retry_count", 0) > 0:
        message += (
            f"\n\n[Revision needed] Your previous answer was rejected by the "
            f"compliance reviewer for this reason: {state['critic_feedback']} "
            f"Please produce a corrected answer."
        )

    return message


def billing_node(state: SupportState) -> dict:
    """LangGraph node: gets a draft response from the billing specialist."""
    ticket_id = state["ticket"]["id"]
    message = _build_specialist_message(state)

    log_exchange(ticket_id, "billing_specialist", "input", {"message": message})
    result = billing_agent.invoke({"messages": [{"role": "user", "content": message}]})
    output = result["messages"][-1].content
    log_exchange(ticket_id, "billing_specialist", "output", {"answer": output})

    return {"specialist_output": output}


def dental_node(state: SupportState) -> dict:
    """LangGraph node: gets a draft response from the dental specialist."""
    ticket_id = state["ticket"]["id"]
    message = _build_specialist_message(state)

    log_exchange(ticket_id, "dental_specialist", "input", {"message": message})
    result = dental_agent.invoke({"messages": [{"role": "user", "content": message}]})
    output = result["messages"][-1].content
    log_exchange(ticket_id, "dental_specialist", "output", {"answer": output})

    return {"specialist_output": output}


def benefits_node(state: SupportState) -> dict:
    """LangGraph node: gets a draft response from the benefits specialist."""
    ticket_id = state["ticket"]["id"]
    message = _build_specialist_message(state)

    log_exchange(ticket_id, "benefits_specialist", "input", {"message": message})
    result = benefits_agent.invoke({"messages": [{"role": "user", "content": message}]})
    output = result["messages"][-1].content
    log_exchange(ticket_id, "benefits_specialist", "output", {"answer": output})

    return {"specialist_output": output}


def critic_node(state: SupportState) -> dict:
    """LangGraph node: audits the specialist's draft output for groundedness, safety, and completeness."""
    ticket_id = state["ticket"]["id"]
    question = state["ticket"]["question"]
    policy = state.get("policy") or "(none provided)"
    draft = state["specialist_output"]

    audit_input = (
        f"Employee question: {question}\n\n"
        f"Policy context: {policy}\n\n"
        f"Specialist draft output: {draft}"
    )

    log_exchange(ticket_id, "critic", "input", {"audit_input": audit_input})

    result = critic_agent.invoke({"messages": [{"role": "user", "content": audit_input}]})
    audit = json.loads(result["messages"][-1].content)

    updates = {
        "critic_status": audit["decision"],
        "critic_feedback": audit["critic_feedback"],
    }

    if audit["decision"] == "RETRY":
        updates["retry_count"] = state["retry_count"] + 1

    log_exchange(ticket_id, "critic", "decision", {
        "critic_status": updates["critic_status"],
        "critic_feedback": updates["critic_feedback"],
        "retry_count": updates.get("retry_count", state["retry_count"]),
    })

    return updates
