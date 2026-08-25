# Northstar Support Co. - Critic / Reviewer Agent
# Aligned with graph_state.SupportState, prompts.CRITIC_PROMPT, and config.llm
# from the team repo (Justriveting/northstar-support-multi-agent).

import json

from config import llm
from graph_state import SupportState
from prompts import CRITIC_PROMPT

MAX_RETRIES = 3


def critic_node(state: SupportState) -> SupportState:
    """
    LangGraph node: audits the specialist's draft_output against
    CRITIC_PROMPT's checklist (groundedness, safety, completeness).

    Writes state["critic_status"] as one of "PASS" / "RETRY" / "ESCALATE",
    matching the JSON contract defined in prompts.CRITIC_PROMPT.
    """
    # Already flagged for human review upstream (e.g. router couldn't
    # confidently classify) -- nothing to audit.
    if state["human_review"] or state["category"] == "human_review":
        state["critic_status"] = "ESCALATE"
        state["critic_feedback"] = "No specialist draft to review; request already flagged for human review."
        state["human_review"] = True
        return state

    draft = state["draft_output"]

    # Specialist explicitly signaled it couldn't answer from context.
    if not draft or draft.strip() == "INSUFFICIENT_CONTEXT":
        state["critic_status"] = "ESCALATE"
        state["critic_feedback"] = "Specialist could not answer from the available policy context."
        state["human_review"] = True
        return state

    audit_input = (
        f"Employee question:\n{state['ticket']}\n\n"
        f"Policy context provided to specialist:\n{state.get('policy') or '(none provided)'}\n\n"
        f"Specialist draft output:\n{draft}"
    )

    response = llm.invoke([
        {"role": "system", "content": CRITIC_PROMPT},
        {"role": "user", "content": audit_input},
    ])

    decision, feedback = _parse_critic_response(response.content)

    state["critic_status"] = decision
    state["critic_feedback"] = feedback

    if decision == "RETRY":
        state["retry_count"] += 1
        if state["retry_count"] > MAX_RETRIES:
            state["critic_status"] = "ESCALATE"
            state["human_review"] = True
            state["critic_feedback"] = f"{feedback} (max retries exceeded, escalating to human review)"
    elif decision == "ESCALATE":
        state["human_review"] = True

    return state


def _parse_critic_response(raw_content: str) -> tuple[str, str]:
    """
    Parses the critic LLM's JSON response per CRITIC_PROMPT's contract:
    {"decision": "PASS"|"RETRY"|"ESCALATE", "reasoning": "...", "critic_feedback": "..."}

    Falls back to ESCALATE if the model doesn't return valid/parseable JSON --
    never silently approves on a parsing failure.
    """
    try:
        result = json.loads(raw_content)
        decision = str(result.get("decision", "ESCALATE")).upper()
        if decision not in ("PASS", "RETRY", "ESCALATE"):
            return "ESCALATE", f"Critic returned an unrecognized decision: '{decision}'."
        feedback = result.get("critic_feedback") or result.get("reasoning", "")
        return decision, feedback
    except (json.JSONDecodeError, AttributeError, TypeError):
        return "ESCALATE", "Critic response could not be parsed as valid JSON."


def finalize_response(state: SupportState) -> SupportState:
    """
    Turns the critic's verdict into what the employee actually sees.
    """
    if state["critic_status"] == "PASS":
        state["final_response"] = state["draft_output"]
    elif state["critic_status"] == "ESCALATE":
        state["final_response"] = (
            "This request has been routed to a human specialist for review. "
            "You'll receive a follow-up shortly."
        )
    else:
        # RETRY and still within budget -- no final response yet;
        # the graph should loop back to the specialist node.
        state["final_response"] = None

    return state


if __name__ == "__main__":
    # Minimal standalone smoke test with a fake draft, since this file
    # doesn't own routing or specialist execution.
    from graph_state import create_shared_state

    state = create_shared_state("Is my annual dental cleaning covered?")
    state["category"] = "dental"
    state["policy"] = "In-network preventive dental cleanings are covered at 100%, twice per year."
    state["draft_output"] = (
        "Yes, your annual dental cleaning is covered at 100% if performed "
        "in-network, up to twice per year."
    )

    state = critic_node(state)
    state = finalize_response(state)

    print("\nCritic Result:")
    print(state)