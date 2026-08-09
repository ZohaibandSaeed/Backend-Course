from pydantic import BaseModel

class UserSync(BaseModel):
    clerk_user_id: str
    name: str
    email: str

class Email_Balance(BaseModel):
    email: str
    balance: float

class Email_Status(BaseModel):
    email: str

class User_Transaction(BaseModel):
    receiver_email: str
    amount: float