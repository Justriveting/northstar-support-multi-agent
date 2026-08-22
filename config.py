import os
from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek

load_dotenv()

llm = ChatDeepSeek(
    model="deepseek-v4-flash",
)

response = llm.invoke("Hello! Say 'DeepSeek is connected.'")

print(response.content)
