from datetime import date
from pydantic import BaseModel

__all__ = [
    "validate_user",
    "exists_account",
    "LoginRequest",
    "SignUpRequest"
]

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

def validate_user(request_log: LoginRequest)-> bool:
    return False

def exists_account(request_sign_up: SignUpRequest) -> bool:
    return False