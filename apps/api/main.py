from fastapi import FastAPI
from prometheus_client import Counter, Histogram, generate_latest
from starlette.responses import Response
import time
import os
import psycopg2
import redis


app = FastAPI()

pg_conn = None
redis_client = None


def init_connections():
    global pg_conn, redis_client

    if pg_conn is None:
        pg_conn = psycopg2.connect(
            host=os.getenv("POSTGRES_HOST"),
            port=os.getenv("POSTGRES_PORT"),
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
        )

    if redis_client is None:
        redis_client = redis.Redis(
            host=os.getenv("REDIS_HOST"),
            port=int(os.getenv("REDIS_PORT")),
            decode_responses=True,
        )


init_connections()


REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint"]
)

REQUEST_LATENCY = Histogram(
    "http_request_latency_seconds",
    "HTTP request latency",
    ["endpoint"]
)


@app.get("/health")
def health():
    REQUEST_COUNT.labels(method="GET", endpoint="/health").inc()
    pg_ok = False
    redis_ok = False

    try:
        cur = pg_conn.cursor()
        cur.execute("SELECT 1")
        pg_ok = True
    except Exception:
        pg_ok = False

    try:
        redis_client.ping()
        redis_ok = True
    except Exception:
        redis_ok = False

    return {
        "status": "ok" if pg_ok and redis_ok else "degraded",
        "postgres": pg_ok,
        "redis": redis_ok
    }


@app.get("/")
def root():
    REQUEST_COUNT.labels(method="GET", endpoint="/").inc()
    return {"message": "Internal DevOps Platform API"}


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type="text/plain")


@app.get("/slow")
def slow():
    start = time.time()
    time.sleep(1)
    REQUEST_COUNT.labels(method="GET", endpoint="/slow").inc()
    REQUEST_LATENCY.labels(endpoint="/slow").observe(time.time() - start)
    return {"message": "slow response"}
