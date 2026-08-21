from langchain.agents import create_agent
from prompts import SPECIALIST_BENEFITS_PROMPT, SPECIALIST_BILLING_PROMPT, SPECIALIST_DENTAL_PROMPT, CRITIC_PROMPT
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