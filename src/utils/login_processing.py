from typing import Union, Tuple
from datetime import date
from pymongo.collection import Collection
from pydantic import BaseModel
from src.model.db import create_connection_mdb

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

def validate_user(request_log: LoginRequest)-> Tuple[list, Collection]:
    '''
    Check user loginning to sis is valid or not
    '''
    conn = create_connection_mdb(collection_name="accounts")
    users = conn.find(
        {"$and": [
            {"username": request_log.username},
            {"password": request_log.password}
        ]}, 
        {"username": 1, "password": 1}
    )
    return users, conn

def exists_account(request_sign_up: SignUpRequest) -> Tuple[list, Collection]:
    '''
    Check user loginning to sis is exists or not by username or id_student
    '''
    conn = create_connection_mdb(collection_name="accounts")
    users = conn.find(
        {"$or": [
            {"username": request_sign_up.username},
            {"identity_number": request_sign_up.identity_number}
        ]}, 
        {"username": 1, "identity_number": 1}
    )
    return users, conn