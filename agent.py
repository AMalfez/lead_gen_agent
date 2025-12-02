from langchain.agents import create_agent
from model import model
from tools.find_email import find_email
from tools.verify_email import verify_email
from tools.discover import discover_companies, discover_people
from pydantic import BaseModel
from typing import Literal
from langchain.agents.structured_output import ToolStrategy
from middleware.trim_msg import trim_messages
from langchain_core.runnables import RunnableConfig
import os

ENV = os.getenv("ENV") or "dev"

class AgentResponse(BaseModel):
    type: Literal[
        "email",
        "verification",
        "companies",
        "people",
        "general"
    ]
    email: str | None = None
    status: str | None = None
    companies: list[str] | None = None
    people: list[dict] | None = None
    response: str | None = None

tools = [find_email, verify_email, discover_companies, discover_people]

config: RunnableConfig = {"configurable": {"thread_id": "1"}}

prompt = """
You are an AI agent that helps users find and connect to leads.
    You have access to the following tools:
    1. find_email: Find the email address of a person given their domain, first name, and last name.
    2. verify_email: Verify the validity of an email address.
    3. discover_companies: Discover potential target companies based on a description from the query.
    4. discover_people: Discover potential people working at a company based on the domain.
    Use these tools to assist users in finding and verifying email addresses as well as discovering target companies and people to reach out to in a particular company.
    You must ALWAYS answer using the AgentResponse JSON structure.

    The "type" field determines what you are returning:
    - "email" → fill the email field
    - "verification" → fill status
    - "companies" → fill companies[]
    - "people" → fill people[]
    - "general" → fill response (use this when you encounter error or returning a general message or follow up question)

    NEVER output plain text. NEVER output partial JSON. NEVER output fields that do not belong to AgentResponse.

    NOTE:
    verify_email tool returns the status of the email address. It takes 1 out of 6 possible values:

    "valid": the email address is valid.
    "invalid": the email address is not valid.
    "accept_all": the email address is valid but any email address is accepted by the server.
    "webmail": the email address comes from an email service provider such as Gmail or Outlook.
    "disposable": the email address comes from a disposable email service provider.
    "unknown": we failed to verify the email address.
"""

if ENV == "dev":
    from langgraph.checkpoint.memory import InMemorySaver
    agent = create_agent(
        model,
        tools = tools,
        middleware=[trim_messages],
        system_prompt=prompt,
        response_format=ToolStrategy(AgentResponse),
        checkpointer=InMemorySaver()
    )
else:
    from langgraph.checkpoint.postgres import PostgresSaver  
    DB_URI = "postgresql://postgres:postgres@localhost:5442/postgres?sslmode=disable"
    with PostgresSaver.from_conn_string(DB_URI) as checkpointer:
        checkpointer.setup() # auto create tables in PostgresSql
        agent = create_agent(
            model,
            tools=tools,
            checkpointer=checkpointer, 
            system_prompt=prompt,
            response_format=ToolStrategy(AgentResponse),
            middleware=[trim_messages],
        )

def invoke_agent(query:str):
    res = agent.invoke({"messages":[{"role":"user","content":query}]},config)
    return res['structured_response']

if __name__ == "__main__":
    query = "How are you?"
    res = agent.invoke({"messages":[{"role":"user","content":query}]},config)
    print(res['structured_response'])