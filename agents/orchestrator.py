import json

from config import llm
from graph_state import SupportState
from prompts import ROUTER_PROMPT


def orchestrator_node(state: SupportState) -> dict:
    """LangGraph node: uses ROUTER_PROMPT to classify the ticket into a category."""
    question = state["ticket"]["question"]

    response = llm.invoke([
        {"role": "system", "content": ROUTER_PROMPT},
        {"role": "user", "content": question},
    ])

    result = json.loads(response.content)
    category = result["category"]

    return {"category": category, "human_review": category == "human_review"}
