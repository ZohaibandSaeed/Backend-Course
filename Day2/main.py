
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from typing import List, Dict

class Register(BaseModel):
    username : str = Field(max_length=10, min_length=3)
    password : str
    confirm_password : str
    gamil : EmailStr
    uid : int = Field (strict=True)
    test: Dict[str, int]
    
    @field_validator('username', mode="before")
    @classmethod
    def user_name_set(cls, value):
        upper_case = value.lower()
        print(upper_case)
        return upper_case
    
    @model_validator(mode="after")
    def confirm_password_validate(self):
        if self.password == self.confirm_password:
            return self
        else:
            return "Password and Conform Password not match"


obj = Register(username="Zohaib", password="123", confirm_password="123", gamil="abc@gmail.com", uid=10, test={"one": 1})

print(obj.username)
print(obj.password)
print(obj.confirm_password)
print(obj.gamil)
print(obj.uid)
print(type(obj.uid))