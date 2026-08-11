from os import sendfile
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import select, Session, or_

from database import create_db_and_tables, get_session
from models import Users, Transaction
from auth import get_current_user, get_current_admin
from schemas import UserSync, Email_Balance, Email_Status, User_Transaction

app = FastAPI()

# React ko API se connect karne ke liye CORS lazmi hai
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def hello():
    return {"message": "Hello World"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/me")
def get_my_profile(current_user: Users = Depends(get_current_user)):
    return {
        "message": "Authenticate successful",
        "user_data": current_user
    }


@app.post("/sync-user")
def sync_user(user: UserSync, session: Session = Depends(get_session)):
    
    already_register = session.exec(select(Users).where(Users.clerk_user_id == user.clerk_user_id)).first()
    if already_register:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    
    new_user = Users(
        clerk_user_id = user.clerk_user_id,
        name = user.name,
        email = user.email,
        role = "user",
        balance = 0.0,
        status = "active",
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    
    return {"message": "User Created Successfully", "user": new_user}

@app.post("/admin/add-credits")
def add_credits(payload: Email_Balance, session: Session = Depends(get_session), admin: Users = Depends(get_current_admin)):
    user = session.exec(select(Users).where(Users.email == payload.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not active")
    
    user.balance += payload.balance
    
    session.add(user)
    session.commit()
    session.refresh(user)

    return {"message": "Credits Added Successfully", "user": user}

@app.post("/admin/block-user")
def block_user(payload: Email_Status, session: Session = Depends(get_session), admin: Users = Depends(get_current_admin)):
    user = session.exec(select(Users).where(Users.email == payload.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin Status Cannot be Modified")
    
    if user.status == "block":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already blocked")
    
    user.status = "block"
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {"message": "User Blocked Successfully", "user": user}


@app.post("/admin/unblock-user")
def unblock_user(payload: Email_Status, session: Session = Depends(get_session), admin: Users = Depends(get_current_admin)):
    user = session.exec(select(Users).where(Users.email == payload.email)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.role == "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin Status Not be Modeify")
    
    if user.status == "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is already active")
    
    user.status = "active"
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return {"message": "User Unblocked Successfully", "user": user}


@app.post("/user/transfer")
def transfer_money(
    payload: User_Transaction, 
    session: Session = Depends(get_session), 
    current_user: Users = Depends(get_current_user)
):
    if current_user.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your account is blocked.")
    
    if current_user.balance < payload.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient Balance.")
    
    if current_user.email == payload.receiver_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You cannot send money to yourself.")
        
    receiver = session.exec(select(Users).where(Users.email == payload.receiver_email)).first()
    
    if not receiver:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver not found.")
        
    if receiver.status != "active":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Receiver's account is not active.")

    current_user.balance -= payload.amount
    receiver.balance += payload.amount
    
    new_transaction = Transaction(
        sender_id=current_user.id, 
        receiver_id=receiver.id, 
        amount=payload.amount, 
        status="completed"
    )
    
    session.add(current_user)
    session.add(receiver)
    session.add(new_transaction)
    session.commit()
    
    session.refresh(current_user)
    
    return {
        "message": "Money Transferred Successfully!", 
        "amount_sent": payload.amount,
        "new_balance": current_user.balance
    }

@app.get("/user/transaction-history")
def transaction_history(session: Session = Depends(get_session), current_user: Users = Depends(get_current_user)):
    if current_user.status == "block":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Your account is blocked.")
    
    history = session.exec(select(Transaction).where(or_(Transaction.sender_id == current_user.id, Transaction.receiver_id == current_user.id))).all()

    return {"message": "Transaction History", "history": history}
