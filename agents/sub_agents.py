import json

from langchain.agents import create_agent
from config import llm
from graph_state import SupportState
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

def billing_node(state: SupportState) -> dict:
    """LangGraph node: gets a draft response from the billing specialist."""
    question = state["ticket"]["question"]
    result = billing_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return {"specialist_output": result["messages"][-1].content}


def dental_node(state: SupportState) -> dict:
    """LangGraph node: gets a draft response from the dental specialist."""
    question = state["ticket"]["question"]
    result = dental_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return {"specialist_output": result["messages"][-1].content}


def benefits_node(state: SupportState) -> dict:
    """LangGraph node: gets a draft response from the benefits specialist."""
    question = state["ticket"]["question"]
    result = benefits_agent.invoke({"messages": [{"role": "user", "content": question}]})
    return {"specialist_output": result["messages"][-1].content}


def critic_node(state: SupportState) -> dict:
    """LangGraph node: audits the specialist's draft output for groundedness, safety, and completeness."""
    draft = state["specialist_output"]

    result = critic_agent.invoke({"messages": [{"role": "user", "content": draft}]})
    audit = json.loads(result["messages"][-1].content)

    updates = {
        "critic_status": audit["decision"],
        "critic_feedback": audit["critic_feedback"],
    }

    if audit["decision"] == "RETRY":
        updates["retry_count"] = state["retry_count"] + 1

    return updates