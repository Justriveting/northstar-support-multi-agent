# Northstar Support Co. - Critic / Reviewer Agent
from typing import Literal

from pydantic import BaseModel

from config import llm
from graph_state import SupportState
from prompts import CRITIC_PROMPT

MAX_RETRIES = 2


class CriticVerdict(BaseModel):
    decision: Literal["PASS", "RETRY", "ESCALATE"]
    reasoning: str
    critic_feedback: str = ""


critic_llm = llm.with_structured_output(CriticVerdict)


def critic_node(state: SupportState) -> SupportState:
    if state["human_review"] or state["category"] == "human_review":
        state["critic_status"] = "ESCALATE"
        state["critic_feedback"] = "Already flagged for human review; nothing to audit."
        state["human_review"] = True
        return state

    draft = state["draft_output"]
    if not draft or draft.strip() == "INSUFFICIENT_CONTEXT":
        state["critic_status"] = "ESCALATE"
        state["critic_feedback"] = "Specialist lacked sufficient context to answer."
        state["human_review"] = True
        return state

    verdict = critic_llm.invoke([
        {"role": "system", "content": CRITIC_PROMPT},
        {"role": "user", "content": (
            f"Employee question:\n{state['ticket']}\n\n"
            f"Policy context:\n{state.get('policy') or '(none provided)'}\n\n"
            f"Specialist draft:\n{draft}"
        )},
    ])

    state["critic_status"] = verdict.decision
    state["critic_feedback"] = verdict.critic_feedback or verdict.reasoning

    if verdict.decision == "RETRY":
        state["retry_count"] += 1
        if state["retry_count"] > MAX_RETRIES:
            state["critic_status"] = "ESCALATE"
            state["human_review"] = True
    elif verdict.decision == "ESCALATE":
        state["human_review"] = True

    return state


def route_after_critic(state: SupportState) -> str:
    """For graph.add_conditional_edges("critic", route_after_critic, {...})"""
    return {"PASS": "synthesize", "RETRY": "retry"}.get(state["critic_status"], "human_review")


if __name__ == "__main__":
    from graph_state import create_shared_state

    state = create_shared_state("Is my annual dental cleaning covered?")
    state["category"] = "dental"
    state["policy"] = "In-network preventive dental cleanings are covered at 100%, twice per year."
    state["draft_output"] = "Yes, covered at 100% in-network, twice per year."

    state = critic_node(state)
    print(state)
    print("Next node:", route_after_critic(state))
