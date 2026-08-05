from pydantic import BaseModel
from fastapi import FastAPI


app = FastAPI()

class User(BaseModel):
    name: str 
    password: str
    age: int

user_list = [{"name": "Zain", "password": "123", "age": 21}]

@app.get('/user')
def get_user():
    return user_list

@app.post('/adduser')
def add_user(user: User):
    # user is an object
    temp_dict = {
        "name": user.name,
        "password": user.password,
        "age": user.age
    }
    user_list.append(temp_dict)
    return "user added"

@app.delete('/deleteuser')
def delete_user(user: User):

    for temp_user in user_list:
        if temp_user["name"] == user.name:
            user_list.remove(temp_user)
            return "user deleted"
    return "user not found"

@app.put('/updateuser')
def update_user(name: str, user: User):
    for temp_user in user_list:
        if temp_user["name"] == name:
            temp_user["name"] = user.name
            temp_user["password"] = user.password
            temp_user["age"] = user.age
            return "user updated"
    return "user not found"
            