from langgraph.graph import StateGraph, START, END

from agents.orchestrator import orchestrator_node
from agents.sub_agents import billing_node, dental_node, benefits_node, critic_node
from graph_state import SupportState
from routing import route_after_orchestrator, route_after_critic


def finalize_node(state: SupportState) -> dict:
    """Terminal node: promotes the approved draft to the final response."""
    return {"final_response": state["specialist_output"]}


def human_review_node(state: SupportState) -> dict:
    """Terminal node: marks the ticket for human review; no automated final response is produced."""
    return {"human_review": True}


builder = StateGraph(SupportState)

builder.add_node("orchestrator", orchestrator_node)
builder.add_node("billing", billing_node)
builder.add_node("dental", dental_node)
builder.add_node("benefits", benefits_node)
builder.add_node("critic", critic_node)
builder.add_node("finalize", finalize_node)
builder.add_node("human_review", human_review_node)

builder.add_edge(START, "orchestrator")
builder.add_conditional_edges("orchestrator", route_after_orchestrator)

builder.add_edge("billing", "critic")
builder.add_edge("dental", "critic")
builder.add_edge("benefits", "critic")

builder.add_conditional_edges("critic", route_after_critic)

builder.add_edge("finalize", END)
builder.add_edge("human_review", END)

graph = builder.compile()
