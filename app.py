from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class AgenticRequest(BaseModel):
    query: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/agent")
async def run_agent(request: AgenticRequest):
    from agent import agent
    q = request.query
    response = agent.invoke({"messages":[{"role":"user","content":q}]})
    return response['structured_response']