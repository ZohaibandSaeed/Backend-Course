from fastapi import FastAPI, BackgroundTasks
import os 
from dotenv import load_dotenv
import resend
import time

load_dotenv()

app = FastAPI()


async def send_email():
    print("Email send start")

    resend.api_key = os.getenv("RESEND_API")

    r = resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": "nahope9959@hudzer.com",
        "subject": "Hello World",
        "html": "<p>Congrats on sending your Zohaib<strong>first email</strong>!</p>"
    })
    print("Email send end")

@app.post("/send")
def sendMail(background_tasks: BackgroundTasks):
    print("start")
    background_tasks.add_task(send_email)
    print("end")
    return "Email has been sent"
    
