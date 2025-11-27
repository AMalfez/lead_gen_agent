from langchain.tools import tool
import requests

@tool
def verify_email(email: str) -> str:
    """
    Verify the validity of an email address.
    Args:
        email (str): The email address to verify.
    Returns:
        str: The verification result of the email address.
    """
    
    try:
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key=test-api-key"
        response = requests.get(url)
        if response.status_code == 200:
            # Parse the JSON response
            data = response.json()
            return data['data']['status']
        else:
            return f"Error: {response.status_code} - {response.text}"
        
    except Exception as e:
        return str(e)