from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
load_dotenv()

@tool
def find_email(domain: str, first_name: str, last_name: str) -> str:
    """Find the email address of a person given their company's domain and their first name and last name.

    Args:
        domain (str): The domain of the person's email address or domain of the person'e company.
        first_name (str): The first name of the person.
        last_name (str): The last name of the person.

    Returns:
        str: The email address of the person.
    """

    if not domain or not first_name or not last_name:
        return "Error: domain, first_name, and last_name are required parameters."
    
    try:
        url = f"https://api.hunter.io/v2/email-finder?domain={domain}&first_name={first_name}&last_name={last_name}&api_key=test-api-key"
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data['data']['email']
        else:
            return f"Error: {response.status_code} - {response.text}"
        
    except Exception as e:
        return str(e)