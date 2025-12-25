from fastapi import FastAPI
from schemas import LogRequest, QueryRequest

app = FastAPI(title="LogSense OSS")

@app.post("/logs")
async def ingest_logs(request: LogRequest):
    return {
        "message": "Logs received",
        "count": len(request.logs)
    }

@app.post("/query")
async def query_logs(request: QueryRequest):
    return {
        "question": request.question,
        "answer": "Not implemented yet"
    }
