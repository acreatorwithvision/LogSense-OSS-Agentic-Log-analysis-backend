from fastapi import FastAPI
from schemas import LogRequest, QueryRequest
from aggregate import aggregate_logs

app = FastAPI(title="LogSense OSS")

# Temporary in-memory store (will replace later)
AGGREGATED_STATE = {}

@app.post("/logs")
async def ingest_logs(request: LogRequest):
    global AGGREGATED_STATE

    AGGREGATED_STATE = aggregate_logs(request.logs)

    return {
        "message": "Logs aggregated",
        "summary": AGGREGATED_STATE
    }

@app.post("/query")
async def query_logs(request: QueryRequest):
    return {
        "question": request.question,
        "answer": "Aggregation only for now"
    }
