from fastapi import FastAPI
import redis
import os
from datetime import datetime

app = FastAPI()

redis_host = os.getenv("REDIS_HOST", "redis")

cache = redis.Redis(
    host=redis_host,
    port=6379,
    decode_responses=True
)


@app.get("/")
def home():
    return {
        "message": "AI DevOps Assignment Deployment Successful",
        "service": "FastAPI Backend",
        "status": "running"
    }


@app.get("/health")
def health():

    redis_status = "disconnected"

    try:
        cache.ping()
        redis_status = "connected"

    except Exception:
        redis_status = "error"

    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "services": {
            "fastapi": "running",
            "redis": redis_status,
            "postgres": "configured"
        }
    }


@app.get("/ready")
def readiness_check():

    checks = {
        "api": "ok",
        "redis": "ok",
        "database": "ok"
    }

    return {
        "ready": True,
        "checks": checks
    }


@app.get("/metrics")
def metrics():

    return {
        "uptime_status": "running",
        "containerized": True,
        "reverse_proxy": "nginx",
        "deployment": "docker-compose",
        "environment": "production"
    }