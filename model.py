from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
load_dotenv()

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")

if __name__ == "__main__":
    response = model.invoke("Hi how are you?")
    print(response.text)