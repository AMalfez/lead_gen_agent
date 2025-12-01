from langchain.tools import tool
import requests
import os
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("HUNTER_API_KEY")

@tool
def discover_companies(query: str) -> list:
    """
    Find potential target companies (along with their domain) based on description from the query.
    Args:
        query (str): Describe the companies you are looking for.
    Returns:
        list: A list of all relevant companies
    """
    
    try:
        url = f"https://api.hunter.io/v2/discover?api_key={API_KEY}"
        payload = {"query": f"{query}"}
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            res = []
            for company in data['data']:
                res.append(f"{company["organization"]} - {company["domain"]}")
            return res
        else:
            return f"Error: {response.status_code} - {response.text}"
        
    except Exception as e:
        return str(e)
    

@tool
def discover_people(domain: str) -> list:
    """
    Discover potential people (along with their email id, position and name) working at a company based on the domain.
    Args:
        domain (str): The domain of the company.
    Returns:
        list: A list of all relevant people with details.
    """

    if not domain:
        return "Error: domain is a required parameter."
    
    try:
        url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={API_KEY}"
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            res = []
            for person in data['data']['emails']:
                res.append({"email":person["value"], "first_name":person["first_name"], "last_name":person["last_name"], "position":person["position"]})
            return res
        else:
            return f"Error: {response.status_code} - {response.text}"
        
    except Exception as e:
        return str(e)