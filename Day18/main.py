from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import SQLModel, Session, text, Field, select
from typing import Optional
from database import get_db, engine
from upstash_redis import Redis
from dotenv import load_dotenv
import os
import json

# .env load karo
load_dotenv()

# Upstash Redis
redis_client = Redis(
    url=os.getenv("UPSTASH_REDIS_REST_URL"),
    token=os.getenv("UPSTASH_REDIS_REST_TOKEN")
)


# User Model
class UserProfile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True)
    description: str


# Database tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)


# Home
@app.get("/")
def read_root():
    return {
        "message": "FastAPI + Neon + Upstash Redis"
    }


# Test Database
@app.get("/test-db")
def test_db_connection(db: Session = Depends(get_db)):
    try:
        db.exec(text("SELECT 1")).first()

        return {
            "message": "Neon Database connection successful!",
            "status": "ok"
        }

    except Exception as e:
        return {
            "message": "Neon Database connection failed!",
            "error": str(e)
        }


# Create User
@app.post("/users/")
def create_user(
    user: UserProfile,
    db: Session = Depends(get_db)
):

    existing_user = db.exec(
        select(UserProfile)
        .where(UserProfile.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Yeh email pehle se registered hai"
        )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Agar purana cache exist karta hai to delete
    cache_key = f"user:{user.email}"
    redis_client.delete(cache_key)

    return user


# Get User
@app.get("/users/{email}")
def get_user_by_email(
    email: str,
    db: Session = Depends(get_db)
):

    # -------------------------
    # 1. Redis Cache Check
    # -------------------------

    cache_key = f"user:{email}"

    cached_user = redis_client.get(cache_key)

    if cached_user:

        print("⚡ Data UPSTASH REDIS se araha hai!")

        return json.loads(cached_user)


    # -------------------------
    # 2. Neon Database
    # -------------------------

    print("🐢 Data NEON DATABASE se araha hai!")

    user = db.exec(
        select(UserProfile)
        .where(UserProfile.email == email)
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User nahi mila"
        )


    # -------------------------
    # 3. Redis mein Cache
    # -------------------------

    redis_client.setex(
        cache_key,
        60,
        user.model_dump_json()
    )

    return user