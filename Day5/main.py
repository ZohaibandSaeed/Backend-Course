from time import process_time
import time
from fastapi import FastAPI, Request, Header

app = FastAPI()

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    print("start middle-ware")
    start_time = time.time()

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Custom-Time"] = str(process_time)
    print("end middle-ware")

    return response


@app.get("/")
def get_request(request: Header):
    
    return {"message": "hello"}
