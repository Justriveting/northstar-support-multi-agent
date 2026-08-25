from typing import Optional, TypedDict


class SupportState(TypedDict):
    ticket: str
    category: Optional[str]
    policy: Optional[str]
    specialist_output: Optional[str]
    critic_status: Optional[str]
    critic_feedback: Optional[str]
    retry_count: int
    human_review: bool
    final_response: Optional[str]


def create_shared_state(ticket: str) -> SupportState:
    return {
        "ticket": ticket,
        "category": None,
        "policy": None,
        "specialist_output": None,
        "critic_status": None,
        "critic_feedback": None,
        "retry_count": 0,
        "human_review": False,
        "final_response": None,
    }
