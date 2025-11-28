from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

model = ChatGroq(model="moonshotai/kimi-k2-instruct-0905")

if __name__ == "__main__":
    messages = [
        ("system", "You are a helpful assistant."),
        ("user", "Hello!"),
    ]
    response = model.invoke(messages)
    print(response.text)