from langchain.agents import create_agent
from model import model
from tools.find_email import find_email
from tools.verify_email import verify_email
from pydantic import BaseModel, Field
from typing import Union
from langchain.agents.structured_output import ToolStrategy

prompt = """
You are an AI agent that helps users find and verify email addresses.
You have access to the following tools:
1. find_email: Find the email address of a person given their domain, first name, and last name.
2. verify_email: Verify the validity of an email address.
Use these tools to assist users in finding and verifying email addresses as needed.

NOTE:
verify_email tool returns the status of the email address. It takes 1 out of 6 possible values:

"valid": the email address is valid.
"invalid": the email address is not valid.
"accept_all": the email address is valid but any email address is accepted by the server.
"webmail": the email address comes from an email service provider such as Gmail or Outlook.
"disposable": the email address comes from a disposable email service provider.
"unknown": we failed to verify the email address.

"""

class Email(BaseModel):
    """ Use this strucure if you are returning an email address """
    email: str|None = Field(description="The email address of the person.")

class isVerified(BaseModel):
    """ Use this strucure if you are returning the verification status of an email address """
    status: str|None = Field(description="The verification status of the provided email address.")

agent = create_agent(
    model,
    tools = [find_email, verify_email],
    system_prompt=prompt,
    response_format=ToolStrategy(Union[Email, isVerified]),
)

if __name__ == "__main__":
    # query = "Find me the email of alfez mansuri who works in Turing."
    query = "Verify the email: richard@piedpiper.com."
    res = agent.invoke({"messages":[{"role":"user","content":query}]})
    print(res['structured_response'])