from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from retrieval.query_engine import query

app = FastAPI(title="SmartQuery - Telemetry Intelligence Assistant")

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: list[str]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/query", response_model=QueryResponse)
def ask(request: QueryRequest):
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question cannot be empty")
    result = query(request.question)
    return {
        "question": result["question"],
        "answer": result["answer"],
        "sources": result["sources"]
    }