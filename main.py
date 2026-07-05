from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time
import uuid

EMAIL = "23f2004697@ds.study.iitm.ac.in"

app = FastAPI()

# Custom middleware
class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{time.perf_counter()-start:.6f}"
        return response

app.add_middleware(MetricsMiddleware)

# CORS MUST be added after the custom middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://dash-actksd.example.com"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/stats")
def stats(values: str = Query(...)):
    nums = [int(x) for x in values.split(",")]

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": sum(nums),
        "min": min(nums),
        "max": max(nums),
        "mean": sum(nums) / len(nums),
    }