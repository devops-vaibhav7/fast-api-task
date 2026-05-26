from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import redis
import json
import os
from datetime import datetime

app = FastAPI()

# -------------------------
# DATABASE CONFIG
# -------------------------

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

# -------------------------
# REDIS CONFIG
# -------------------------

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "redis"),
    port=6379,
    decode_responses=True
)

# -------------------------
# USER MODEL
# -------------------------

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)

# Create table automatically
Base.metadata.create_all(bind=engine)

# -------------------------
# REQUEST MODEL
# -------------------------

class UserCreate(BaseModel):
    name: str
    email: str

# -------------------------
# ROOT
# -------------------------

@app.get("/")
def home():

    return {
        "message": "AI DevOps Assignment Running",
        "status": "success",
        "timestamp": datetime.utcnow().isoformat()
    }

# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/health")
def health():

    redis_status = "disconnected"
    postgres_status = "disconnected"

    try:
        redis_client.ping()
        redis_status = "connected"
    except:
        pass

    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        postgres_status = "connected"
        db.close()
    except:
        pass

    return {
        "status": "healthy",
        "services": {
            "fastapi": "running",
            "postgres": postgres_status,
            "redis": redis_status
        }
    }

# -------------------------
# CREATE USER
# -------------------------

@app.post("/users")
def create_user(user: UserCreate):

    db = SessionLocal()

    new_user = User(
        name=user.name,
        email=user.email
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # clear redis cache
    redis_client.delete("users")

    db.close()

    return {
        "message": "User created",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    }

# -------------------------
# GET USERS
# -------------------------

@app.get("/users")
def get_users():

    cached_users = redis_client.get("users")

    if cached_users:

        return {
            "source": "redis-cache",
            "data": json.loads(cached_users)
        }

    db = SessionLocal()

    users = db.query(User).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "name": user.name,
            "email": user.email
        })

    redis_client.set("users", json.dumps(result), ex=60)

    db.close()

    return {
        "source": "postgresql",
        "data": result
    }

# -------------------------
# DELETE USER
# -------------------------

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    redis_client.delete("users")

    db.close()

    return {
        "message": "User deleted"
    }

# -------------------------
# METRICS
# -------------------------

@app.get("/metrics")
def metrics():

    return {
        "environment": "production",
        "containerized": True,
        "reverse_proxy": "nginx",
        "database": "postgresql",
        "cache": "redis"
    }