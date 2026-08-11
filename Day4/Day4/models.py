from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    name: str
    email: str = Field(unique=True)
    role: str = Field(default="user")
    balance: float = Field(default=0.0)
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.now)

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="users.id")
    receiver_id: int = Field(foreign_key="users.id")
    amount: float = Field(default=0.0)
    status: str = Field(default="not_completed")
    created_at: datetime = Field(default_factory=datetime.now)
