from fastapi import FastAPI, Depends
from sqlmodel import create_engine, Session, SQLModel, Field
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL="postgresql://neondb_owner:npg_YThdLGN5gn2i@ep-jolly-hat-axyvwqcz-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"
engine = create_engine(DATABASE_URL, echo=True)

class User(SQLModel, table=True):
    id: int = Field(primary_key=True)
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
    id: int
    username: str
    email: str
    age: int

@app.post("/createUser")
def create_user(user: PUser, session: Session = Depends(get_session)):
    
    get_user = User(
        id = user.id,
        username = user.username,
        email = user.email,
        age = user.age
    )

    session.add(get_user)
    session.commit()
    session.refresh(get_user)

    return "user created"