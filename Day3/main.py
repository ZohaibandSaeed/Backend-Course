from fastapi import FastAPI, Depends
from sqlmodel import create_engine, Session, SQLModel, Field, select
from pydantic import BaseModel
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL, echo=True)

class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str
    email: str
    age: int

def get_session():
    with Session(engine) as session:
        yield session

def create_db():
    SQLModel.metadata.create_all(engine)

@app.on_event("startup")
def on_startup():
    create_db()

class PUser(BaseModel):
    username: str
    email: str
    age: int

@app.post("/createUser")
def create_user(user: PUser, session: Session = Depends(get_session)):
    usernames = session.exec(select(User.username)).all()
    print(type(usernames))

    for username in usernames:
        if username == user.username:
            return "User Found so new User Cannot be Register"

    get_user = User(
        username = user.username,
        email = user.email,
        age = user.age
    )

    session.add(get_user)
    session.commit()
    session.refresh(get_user)

    return "user created"

@app.get("/getUsers")
def get_all_users(session: Session = Depends(get_session)):
    
    session_data = session.exec(select(User))
    users = session_data.all()
    # users = session.exec(select(User)).all()
    return users

@app.get("/getuser/{username}")
def get_single_user(username: str, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(username == User.username)).first()
    return [user.email, user.id]

@app.put("/updateuser")
def update_user(id: int, new_user: PUser, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.id == id)).first()
    
    if not user:
        return "User Not Found"
    user.username = new_user.username
    user.email = new_user.email
    user.age = new_user.age
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    return "updated successfully"

@app.delete("/deleteUser")
def delete_user(username: str, session: Session = Depends(get_session)):

    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        return "User Not Found"
    session.delete(user)
    session.commit()

    return "Delete Successfully"