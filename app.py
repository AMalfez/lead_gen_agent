from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

origins = os.getenv('FRONTEND_URL') or ["http://localhost:5174","http://localhost:5173",]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    sres = response['structured_response']
    match sres.type:
        case "email":
            return {"response": sres.email}
        case "verification":
            return {"response": sres.status}
        case "companies":
            return {"response": sres.companies}
        case "people":
            return {"response": sres.people}
        case "general":
            return {"response": sres.response}
        case _:
            return {"response": "Unknown response type"}