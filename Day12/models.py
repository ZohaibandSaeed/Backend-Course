from sqlmodel import SQLModel, Field
from typing import Optional

class FileModel(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    imagekit_id: str
    file_url: str
    