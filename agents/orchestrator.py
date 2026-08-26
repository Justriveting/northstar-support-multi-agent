import json

from config import llm
from graph_state import SupportState
from logger import log_exchange
from policy import get_policy
from prompts import ROUTER_PROMPT


def orchestrator_node(state: SupportState) -> dict:
    """LangGraph node: uses ROUTER_PROMPT to classify the ticket into a category."""
    ticket_id = state["ticket"]["id"]
    question = state["ticket"]["question"]

    log_exchange(ticket_id, "orchestrator", "input", {"question": question})

    response = llm.invoke([
        {"role": "system", "content": ROUTER_PROMPT},
        {"role": "user", "content": question},
    ])

    result = json.loads(response.content)
    category = result["category"]

    log_exchange(ticket_id, "orchestrator", "decision", {
        "category": category,
        "reasoning": result.get("reasoning", ""),
    })

    return {
        "category": category,
        "policy": get_policy(category),
        "human_review": category == "human_review",
    }
