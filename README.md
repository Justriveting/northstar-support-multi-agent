# 🧠 Northstar Support — Multi-Agent Customer Support System

## 📌 Project Overview

Northstar Support is a multi-agent AI customer support ticket triage system developed as a **Phase 2 Technical Employment Preparation Project (TEPP)** through The Knowledge House AI Business Solutions Innovation Fellowship.

The system demonstrates how specialized AI agents can work together to classify customer support requests, generate responses grounded in plan policy, evaluate response quality, and escalate appropriate cases for human review.

## 💼 Business Problem

Traditional customer support workflows often require employees to manually review, categorize, route, and respond to incoming tickets. This can increase response times and create inconsistent handling across support teams.

Northstar explores how a multi-agent AI workflow can automate portions of the support process while maintaining quality controls and human oversight.

## 💡 Solution

Northstar uses specialized agents rather than relying on a single AI model to handle the entire customer support process.

A customer ticket moves through an orchestrated workflow where the system:

1. Receives the customer support ticket.
2. Routes the ticket to the appropriate specialist.
3. Drafts a response grounded in the relevant policy information.
4. Sends the response to a Critic Agent for evaluation.
5. Retries the specialist workflow when revision is required, with the critic's specific feedback attached.
6. Escalates appropriate cases to Human Review.

## 🔄 Multi-Agent Workflow

```text
Customer Ticket
      |
    Router
      |
Specialist Agent
      |
    Critic
   /       \
RETRY      PASS
  |          |
Specialist   Final Response

ESCALATE -> Human Review
```

The workflow is designed to maintain human oversight while allowing routine support requests to move through an automated AI-assisted process. See "How a ticket flows through the graph" below for the exact, code-accurate version of this diagram.

## 🤖 Specialist Routing

The system routes tickets into support categories including:

* Billing
* Dental
* Benefits Coverage
* Human Review

Requests requiring additional judgment or falling outside the automated workflow can be escalated for human review.

## 🧠 Shared State & Orchestration

The agents communicate through a shared workflow state. See `graph_state.py`'s `SupportState` (documented in the technical section below) for the exact, current field list.

The orchestration layer controls how the ticket moves between the Router, Specialist Agents, and Critic, with Human Review as the fallback path.

## 🛡️ Human-in-the-Loop Design

Human oversight is an intentional part of the architecture.

Cases that cannot be handled confidently by the automated workflow can be escalated rather than forcing the system to generate an unsupported response.

This approach combines AI automation with human judgment for higher-risk or uncertain requests.

## 🛠️ Technologies

* Python
* Large Language Models (LLMs)
* Multi-Agent AI
* LangChain / LangGraph (StateGraph)
* Streamlit
* Prompt Engineering
* Git
* GitHub

## 🤝 Team Contributions

Northstar was developed collaboratively by a four-person team, with each member responsible for a core component of the multi-agent system.
| Team Member | Role | Primary Contribution |
| --- | --- | --- |
| **Tayo Arogundade** | Orchestrator Engineer / Project Lead | Orchestration, routing logic, shared-state/workflow coordination, testing, integration alignment, and project coordination |
| **Kay Richardson** | Prompt Engineer | Prompt design and development for the AI agent workflow |
| **Lucy Edosomwan** | Critic / QA Engineer | Critic-agent development, response evaluation, quality assurance, and workflow testing |
| **Drequan Walker** | Integration Engineer | Built and tested the LangGraph pipeline end-to-end (orchestrator, specialist, and critic nodes; conditional routing and retry logic), the Streamlit frontend, the audit-trail logging system, and the policy lookup; found and fixed several correctness bugs (critic groundedness, a JSON-parsing crash, a retry-cap mismatch) through direct testing |



## 🚀 Key Skills Demonstrated

* AI Agent Orchestration
* Multi-Agent Systems
* Large Language Model Applications
* Prompt Engineering
* Python
* Workflow Design
* Human-in-the-Loop AI
* Business Process Automation
* Git & GitHub
* Cross-Functional Collaboration
* AI Solution Design

## 🎓 Project Context

The Knowledge House — AI Business Solutions Innovation Fellowship
Phase 2 TEPP Project — 2026

Northstar was developed to demonstrate the practical application of multi-agent AI architecture, workflow orchestration, quality control, collaborative development, and human-in-the-loop AI design.

---

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
- A second real bug found via a teammate's fresh install/test and fixed:
  the critic's structured-output parsing could throw an uncaught exception
  on malformed JSON from the model, crashing the whole request instead of
  failing safe. Now caught and escalated instead of crashing.

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
