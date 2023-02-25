from datetime import date
from pydantic import BaseModel

class LoginRequest(BaseModel):
    user_name: str
    password: str

class SignUpRequest(BaseModel):
    user_type: str
    username: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    identity_number: str
    age: int=0
    birthday: date

def validate_user(request_log: LoginRequest)-> bool:
    return False