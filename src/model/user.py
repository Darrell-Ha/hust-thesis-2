from pydantic import BaseModel
from datetime import date

class Account(BaseModel):
    user_id: int
    user_type: str
    username: str
    password_enc: str
    first_name: str
    last_name: str
    phone_number: str
    identity_number: str
    birthday: date
    secret_token: str

class LoginRequest(BaseModel):
    username: str
    password: str

class SignUpRequest(BaseModel):
    user_type: str
    username: str
    password: str
    first_name: str
    last_name: str
    phone_number: str
    identity_number: str
    birthday: date

__all__ = [
    "Account",
    "SignUpRequest",
    "LoginRequest"
]