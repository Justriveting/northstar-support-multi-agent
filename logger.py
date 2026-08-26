"""
Northstar Support Co. - Exchange Logger

Every agent-to-agent hop (orchestrator -> specialist -> critic -> finalize)
is written here as one JSON line, so a reviewer can reconstruct exactly
what each agent saw and said for any ticket, without re-running anything.
"""

import json
import os
from datetime import datetime, timezone

LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
LOG_PATH = os.path.join(LOG_DIR, "exchange_log.jsonl")

os.makedirs(LOG_DIR, exist_ok=True)


def log_exchange(ticket_id: str, agent: str, event: str, payload: dict) -> None:
    """
    Append one structured record of an agent's input/output to the shared
    exchange log.

    ticket_id: correlates every hop for a single support ticket
    agent:     which agent produced this event (orchestrator, billing_specialist,
               dental_specialist, benefits_specialist, critic, finalize, human_review)
    event:     "input", "output", or "decision"
    payload:   whatever is useful to reconstruct that step (kept as plain
               strings/dicts so the file stays human-readable)
    """
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ticket_id": ticket_id,
        "agent": agent,
        "event": event,
        "payload": payload,
    }
    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"[{record['timestamp']}] ({ticket_id}) {agent} :: {event} -> "
          f"{json.dumps(payload, ensure_ascii=False)[:300]}")


def read_ticket_trail(ticket_id: str) -> list[dict]:
    """Return every logged event for a given ticket, in order."""
    if not os.path.exists(LOG_PATH):
        return []
    trail = []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record["ticket_id"] == ticket_id:
                trail.append(record)
    return trail
