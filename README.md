# northstar-support-multi-agent

Multi-agent customer support ticket triage system for Northstar Support Co.
(a TPA / employee-benefits support desk).

## What it does

An employee submits a plain-English benefits question. A **Router** agent
classifies it, a **Specialist** agent (Billing / Dental / Benefits &
Coverage — each with its own system prompt) drafts an answer grounded in
fictional plan policy text, and a **Critic** agent audits that draft for
groundedness, safety, and completeness before anything is sent back to the
employee. Tickets the router can't confidently classify, or drafts the
critic can't approve after retries, are automatically escalated to a human
reviewer.

## How a ticket flows through the graph

```
Employee submits ticket (name, question, additional info)
        |
Shared state initialized (graph_state.py)
        |
Orchestrator classifies the ticket ---------------> human_review
        | (billing / dental / benefits_coverage)         |
        v                                                 |
Specialist drafts an answer, grounded in                  |
fake policy text for that category                        |
        |                                                  |
        v                                                  |
Critic audits the draft (question + policy + draft)        |
        |                                                  |
   PASS ------> final_response sent to employee            |
   RETRY -----> back to the SAME specialist, with           |
   (up to 3x)   the critic's specific feedback attached     |
   ESCALATE --------------------------------------------> human_review
        |
        v
Streamlit UI (app.py) displays the final response or an escalation notice
```

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
copy .env.example .env        # then fill in DEEPSEEK_API_KEY
```

## Run

```bash
python main.py            # CLI entry point
streamlit run app.py      # web UI
```

Every agent hop (router -> specialist -> critic -> finalize) is written as
one JSON line to `logs/exchange_log.jsonl` (gitignored, regenerated per
run) — the full audit trail for a ticket, including retries and
escalations, correlated by a real ticket ID.

## Project layout

```
ticket.py                # create_ticket() -- builds the ticket dict, real ID via uuid
graph_state.py            # SupportState TypedDict -- the shared-state contract every node reads/writes
policy.py                 # fictional policy text per category (deliberately not RAG/ChromaDB)
routing.py                # conditional-edge logic: category routing, retry cap (MAX_RETRIES = 3)
workflow.py                # builds and compiles the LangGraph StateGraph
logger.py                  # writes logs/exchange_log.jsonl, the audit trail
agents/
  orchestrator.py          # orchestrator_node -- LLM routing via ROUTER_PROMPT
  sub_agents.py             # billing/dental/benefits specialist agents + their graph nodes,
                             # critic_node (audits drafts, deterministic guard against a raw
                             # "INSUFFICIENT_CONTEXT" reaching an employee)
tools/
  specialists.py            # specialist-dispatch tool wrappers
prompts.py                  # all system prompts (router, specialists, critic)
config.py                   # DeepSeek client (langchain_deepseek.ChatDeepSeek)
main.py                     # CLI entry point, runs a ticket through the compiled graph
app.py                       # Streamlit frontend
measure_approval_rate.py     # runs a batch of test tickets through the graph and tallies
                             # PASS/ESCALATE outcomes -- used to back pitch-deck claims with real data
```

## What's been tested

- Full end-to-end runs through the real compiled graph with real API calls
- Retry-with-feedback proven both directions: a fixable gap in a draft gets
  corrected on retry and passes; a genuinely unfixable gap (info missing
  from policy) correctly exhausts retries and escalates
- A batch of 18 representative tickets across all three categories (plus
  ambiguous edge cases) run through the graph — currently ~89%
  auto-approved / ~11% escalated (`measure_approval_rate.py`)
- A real bug found via that batch test and fixed: the critic could
  inconsistently let a bare `INSUFFICIENT_CONTEXT` specialist signal reach
  an employee as if it were a real answer. Now guarded deterministically —
  one coached retry first, then automatic escalation if still unanswerable.

## Current status

Core pipeline, retry/escalation logic, the fake-policy lookup, the audit
trail, and the Streamlit frontend are all built, tested, and merged into
`dre-integration-engine`. Reconciled against the stakeholder pitch deck —
the retry cap and the auto-approval-rate claim are both now backed by
actual measured behavior, not assumptions.

**Open items:**
- `agents/critic.py` exists but is unused (an earlier alternate critic
  implementation) — team should decide whether to update it to match the
  current field names or remove it
- `config.py` uses `langchain_deepseek.ChatDeepSeek`; worth reconciling
  against the original stack description ("DeepSeek through an
  OpenAI-compatible API")
- No formal `pytest`-style test suite yet — verification so far has been
  through direct runs and `measure_approval_rate.py`
