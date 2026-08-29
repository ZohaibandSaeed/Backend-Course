from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Users(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    clerk_user_id: str = Field(index=True)
    name: str
    email: str = Field(unique=True)
    created_at: datetime = Field(default_factory=datetime.now)

class Document(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    file_url: str
    imagekit_file_id: str
    created_at: datetime = Field(default_factory=datetime.now)
