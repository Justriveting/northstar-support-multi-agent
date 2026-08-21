import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI


load_dotenv()


DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")


if not DEEPSEEK_API_KEY:
    raise ValueError(
        "DEEPSEEK_API_KEY was not found in the .env file."
    )


llm = ChatOpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
    model="deepseek-v4-flash",
)
