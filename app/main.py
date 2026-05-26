from fastapi import FastAPI
import redis
import os

app = FastAPI()

redis_host = os.getenv("REDIS_HOST", "redis")

cache = redis.Redis(host=redis_host, port=6379)


@app.get("/")
def home():
    return {
        "message": "FastAPI application running successfully"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }