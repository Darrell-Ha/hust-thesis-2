from typing import Union
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

class ChangeInfoRequest(BaseModel):
    username: str
    x_secret_token: str
    # username: Union[str, None]
    password: str
    # first_name: Union[str, None]
    # last_name: Union[str, None]
    # phone_number: Union[str, None]
    # identity_number: Union[str, None]
    # birthday: Union[date, None]

class GetAllRequest(BaseModel):
    x_secret_token: str

__all__ = [
    "Account",
    "SignUpRequest",
    "LoginRequest",
    "ChangeInfoRequest",
    "GetAllRequest"
]