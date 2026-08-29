from pydantic import BaseModel
from typing import EmailStr

class UserSync(BaseModel):
    clerk_user_id: str
    name: str
    email: EmailStr

