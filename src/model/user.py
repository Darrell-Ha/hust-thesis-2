from pydantic import BaseModel
from enum import Enum
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

class RoleName(str, Enum):
    admin = "admin"
    student = "student"

__all__ = [
    "Account",
    "SignUpRequest",
    "LoginRequest",
    "RoleName"
]