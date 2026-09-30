import os
from fastapi import FastAPI, Depends, HTTPException, Request
from dotenv import load_dotenv
from upstash_redis import Redis

load_dotenv()

app = FastAPI()

redis = Redis.from_env()

RATE_LIMIT = 5 # 5 requests allowed
RATE_LIMIT_WINDOW = 60 # per 60 seconds

def rate_limiter(request: Request):
    ip = request.client.host
    print(ip)
    print(request.headers)
    key = f"rate_limit:{ip}"
    
    # Count ko increment karo
    count = redis.incr(key)
    
    # Agar pehli request hai toh expiry (TTL) lagao
    if count == 1:
        redis.expire(key, RATE_LIMIT_WINDOW)
        
    # Agar limit cross ho jaye toh error return karo
    if count > RATE_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Too Many Requests. Please wait and try again."
        )

@app.get("/")
def read_root():
    return {"message": "Hello World"}

# /hii route par rate limiter apply kar diya
@app.get("/hii", dependencies=[Depends(rate_limiter)])
def read_hii():
    return "hii"
