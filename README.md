[README.md](https://github.com/user-attachments/files/23924191/README.md)
# Lead Gen Agent 🚀

An AI-powered lead generation assistant built using **LangChain**,
**FastAPI**, **Groq (Moonshot Kimi K2)**, **Hunter.io**, and **React**.

This project provides:

-   An intelligent agent that discovers companies\
-   Finds emails\
-   Verifies emails\
-   Discovers people working at target companies\
-   JSON-typed structured responses\
-   REST API interface\
-   LangGraph + LangSmith workflow tracing\
-   React frontend ready to plug in


## Architecture
<img width="1024" height="1536" alt="ChatGPT Image Dec 4, 2025, 11_43_07 AM" src="https://github.com/user-attachments/assets/7cdde145-c972-49f9-9ef4-7ad2cae230da" />


## ✨ Features

### 🔍 Discover Companies

Uses Hunter.io Discover API to return a list of relevant companies and
domains.

### 🧑‍💼 Discover People

Fetch employees with email, name, and job position.

### 📧 Find Email

Find a person's email using name + domain.

### ✔️ Verify Email

Check email validity (valid, invalid, disposable, etc.)

### 🧠 LLM Agent with Tool Calling

Moonshot Kimi K2 Instruct model through Groq API.

### 🧩 Structured Output

Every response matches the `AgentResponse` schema.

### 🧠 REST API

Powered by FastAPI.

### 🔗 LangGraph + LangSmith Tracing

Full workflow tracing.

## 📁 Project Structure

    ├── middleware/
    │   └── trim_msg.py
    ├── tools/
    │   ├── discover.py
    │   ├── find_email.py
    │   └── verify_email.py
    ├── agent.py
    ├── app.py
    ├── model.py
    ├── langgraph.json
    ├── requirements.txt
    ├── .env.example
    └── README.md

## 🚀 Getting Started

### 1. Clone the repo

    git clone https://github.com/AMalfez/lead_gen_agent.git
    cd lead_gen_agent

### 2. Create virtual environment

    python -m venv venv
    source venv/bin/activate
    # Windows: venv\Scripts\activate

### 3. Install dependencies

    pip install -r requirements.txt

### 4. Setup environment variables

Rename `.env.example` → `.env` and replace with your env variables.

### 5. Run FastAPI server

    fastapi run app.py

### 6. Run LangSmith Studio 
    langgraph dev

## 📡 API Endpoints

### Health Check

    GET /health

### Main Agent

    POST /agent

## 📈 LangSmith / LangGraph

Tracing enabled automatically when environment variables are set.

## ⚠️ Limitations

-   trim_messages middleware not supported by Moonshot model

## 🙌 Contributing

PRs welcome.

## ⭐ Support

Star the repo if this helped you!
