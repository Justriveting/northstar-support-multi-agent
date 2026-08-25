from langchain.agents import create_agent
from config import llm
from prompts import (
    SPECIALIST_BILLING_PROMPT,
    SPECIALIST_DENTAL_PROMPT,
    SPECIALIST_BENEFITS_PROMPT,
    CRITIC_PROMPT,
)

# AGENT INITIALIZATION

billing_agent = create_agent(
    model=llm,
    system_prompt=SPECIALIST_BILLING_PROMPT
)

dental_agent = create_agent(
    model=llm,
    system_prompt=SPECIALIST_DENTAL_PROMPT
)

benefits_agent = create_agent(
    model=llm,
    system_prompt=SPECIALIST_BENEFITS_PROMPT
)

critic_agent = create_agent(
    model=llm,
    system_prompt=CRITIC_PROMPT
)