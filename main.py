 import time
import uuid

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

EMAIL = "23f2004697@ds.study.iitm.ac.in"
ALLOWED_ORIGIN = "https://dash-actksd.example.com"

app = FastAPI()


class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start = time.perf_counter()

        response = await call_next(request)

        response.headers["X-Request-ID"] = str(uuid.uuid4())
        response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.6f}"

        return response


# Add Metrics FIRST
app.add_middleware(MetricsMiddleware)

# Add CORS LAST (so it executes first)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/stats")
async def stats(values: str = Query(...)):
    nums = [int(x.strip()) for x in values.split(",")]

    total = sum(nums)

    return {
        "email": EMAIL,
        "count": len(nums),
        "sum": total,
        "min": min(nums),
        "max": max(nums),
        "mean": total / len(nums),
    }