from graph_state import SupportState

CATEGORY_TO_NODE = {
    "billing": "billing",
    "dental": "dental",
    "benefits_coverage": "benefits",
}

MAX_RETRIES = 2


def route_after_orchestrator(state: SupportState) -> str:
    """Conditional edge: routes to the specialist node matching the ticket's category."""
    return CATEGORY_TO_NODE.get(state["category"], "human_review")


def route_after_critic(state: SupportState) -> str:
    """Conditional edge: routes based on the critic's decision, category, and retry count."""
    status = state["critic_status"]

    if status == "PASS":
        return "finalize"

    if status == "RETRY" and state["retry_count"] < MAX_RETRIES:
        return CATEGORY_TO_NODE.get(state["category"], "human_review")

    return "human_review"
