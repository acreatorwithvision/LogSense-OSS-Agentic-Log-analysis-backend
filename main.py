from fastapi import FastAPI
from schemas import LogRequest, QueryRequest
from aggregate import aggregate_logs
from cache import get_cached_aggregation, set_cached_aggregation
from vector_store import add_documents, search

app = FastAPI(title="LogSense OSS")

AGGREGATED_STATE = {}

@app.post("/logs")
async def ingest_logs(request: LogRequest):
    global AGGREGATED_STATE

    cached = get_cached_aggregation(request.logs)
    if cached:
        AGGREGATED_STATE = cached
        return {
            "message": "Cache hit",
            "summary": AGGREGATED_STATE
        }

    aggregated = aggregate_logs(request.logs)
    set_cached_aggregation(request.logs, aggregated)

    # Add raw logs to vector DB
    add_documents(request.logs)

    AGGREGATED_STATE = aggregated

    return {
        "message": "Aggregated, cached, and indexed",
        "summary": AGGREGATED_STATE
    }

@app.post("/query")
async def query_logs(request: QueryRequest):
    retrieved_logs = search(request.question)

    return {
        "question": request.question,
        "retrieved_logs": retrieved_logs
    }
