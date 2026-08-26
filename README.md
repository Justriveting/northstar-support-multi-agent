# 🧠 Northstar Support — Multi-Agent Customer Support System

## 📌 Project Overview

Northstar Support is a multi-agent AI customer support ticket triage system developed as a **Phase 2 Technical Employment Preparation Project (TEPP)** through The Knowledge House AI Business Solutions Innovation Fellowship.

The system demonstrates how specialized AI agents can work together to classify customer support requests, retrieve relevant information, generate responses, evaluate response quality, and escalate appropriate cases for human review.

## 💼 Business Problem

Traditional customer support workflows often require employees to manually review, categorize, route, and respond to incoming tickets. This can increase response times and create inconsistent handling across support teams.

Northstar explores how a multi-agent AI workflow can automate portions of the support process while maintaining quality controls and human oversight.

## 💡 Solution

Northstar uses specialized agents rather than relying on a single AI model to handle the entire customer support process.

A customer ticket moves through an orchestrated workflow where the system:

1. Receives the customer support ticket.
2. Routes the ticket to the appropriate specialist.
3. Retrieves relevant information when needed.
4. Generates a draft response.
5. Sends the response to a Critic Agent for evaluation.
6. Retries the specialist workflow when revision is required.
7. Sends approved responses to the Synthesizer.
8. Escalates appropriate cases to Human Review.

## 🔄 Multi-Agent Workflow

```text
Customer Ticket
      ↓
    Router
      ↓
Specialist Agent
      ↓
    Critic
   ↙     ↘
RETRY    PASS
  ↓        ↓
Specialist  Synthesizer
               ↓
          Final Response

ESCALATE → Human Review
```
   The workflow is designed to maintain human oversight while allowing routine support requests to move through an automated AI-assisted process.

## 🤖 Specialist Routing

The system routes tickets into support categories including:

* Billing
* Dental
* Benefits Coverage
* Human Review

Requests requiring additional judgment or falling outside the automated workflow can be escalated for human review.

## 📚 Retrieval-Augmented Generation (RAG)

Northstar incorporates retrieval to provide agents with relevant support information rather than relying only on an LLM’s general knowledge.

This helps ground generated responses in the available knowledge base and supports more consistent customer assistance.

## 🧠 Shared State & Orchestration

The agents communicate through a shared workflow state containing information such as:

* Ticket
* Category
* Priority
* Summary
* Relevant policy/context
* Draft response
* Critic decision

The orchestration layer controls how the ticket moves between the Router, Specialist Agents, Critic, Synthesizer, and Human Review.

## 🛡️ Human-in-the-Loop Design

Human oversight is an intentional part of the architecture.

Cases that cannot be handled confidently by the automated workflow can be escalated rather than forcing the system to generate an unsupported response.

This approach combines AI automation with human judgment for higher-risk or uncertain requests.

## 🛠️ Technologies

* Python
* Large Language Models (LLMs)
* Multi-Agent AI
* Retrieval-Augmented Generation (RAG)
* ChromaDB
* LangGraph / StateGraph
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
| **Drequan Walker** | Integration / RAG Engineer | RAG and ChromaDB integration, retrieval workflow, and system integration |



## 🚀 Key Skills Demonstrated

* AI Agent Orchestration
* Multi-Agent Systems
* Retrieval-Augmented Generation (RAG)
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

Northstar was developed to demonstrate the practical application of multi-agent AI architecture, retrieval-augmented generation, workflow orchestration, quality control, collaborative development, and human-in-the-loop AI design.

