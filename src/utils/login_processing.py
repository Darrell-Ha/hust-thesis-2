import jwt
import os
from fastapi import HTTPException, status
from dotenv import load_dotenv
from typing import Tuple
from datetime import datetime
from pymongo.collection import Collection
from src.model.db import create_connection_mdb
from src.model.user import *


load_dotenv("src/.env")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM")

__all__ = [
    "LoginRequest",
    "SignUpRequest",
    "ChangeInfoRequest",
    "process_login",
    "process_sign_up",
    "process_get_all_users",
    "process_change_info"
]

def sanitize_key(token: str) -> str:
    return token.replace("-","").replace("_", "")

def generate_token(payload: dict) -> str:
    if JWT_SECRET_ALGORITHM and JWT_SECRET_ALGORITHM:
        return sanitize_key(jwt.encode(payload, key=JWT_SECRET_KEY, algorithm=JWT_SECRET_ALGORITHM).split(".")[2])
    else:
        raise ValueError(
            "KEY OR ALGORITHMS FOR GENERATE TOKEN HAVEN'T DEFINED!")

def validate_user(username: str, password: str) -> Tuple[dict, Collection]:
    '''
    Check user loginning to sis is valid or not
    '''
    conn = create_connection_mdb(collection_name="accounts")
    res = conn.find_one(
        {"$and": [
            {"username": username},
            {"password": password}
        ]},
        {"_id": 0}
    )
    user = {} if res is None else dict(res)
    return user, conn


def exists_account(username: str, identity_number: str) -> Tuple[dict, Collection]:
    '''
    Check user signup to sis is exists or not by username or id_student
    '''
    conn = create_connection_mdb(collection_name="accounts")
    res = conn.find_one(
        {"$or": [
            {"username": username},
            {"identity_number": identity_number}
        ]},
        {"_id": 0, "username": 1, "identity_number": 1}
    )
    user = {} if res is None else dict(res)
    return user, conn


def exists_account_by_token(token: str) -> Tuple[dict, Collection]:
    '''
    Find account by secret_token
    '''
    conn = create_connection_mdb(collection_name="accounts")
    res = conn.find_one({"secret_key": token}, {"_id": 0})
    user = {} if res is None else dict(res)
    return user, conn


def process_login(request: LoginRequest) -> dict:
    
    username = request.username
    password = request.password
    valid_user, conn = validate_user(username, password)
    if valid_user:
        user = valid_user
        conn.update_one(
            {
                "username": user.get("username")
            },
            {
                "$set": {
                    "last_login": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            }
        )
        return {
            # name or something to show that exists
            "message": f"Hello {valid_user.get('username', '')}",
            "info": valid_user
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This account hasn't existed yet, please sign up to continue!"
        )


def process_sign_up(request: SignUpRequest) -> dict:

    username = request.username
    identity_number = request.identity_number
    exist_acc, conn = exists_account(username, identity_number)
    if not exist_acc:
        # Insert to mongodb:
        new_user = request.dict()
        new_user.update(
            {
                "create_account_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "birthday": new_user.get("birthday", "").strftime("%Y-%m-%d")
            }
        )
        token = generate_token(new_user)
        new_user.update({"secret_key": f'sis_{token}'})
        result = new_user.copy()
        conn.insert_one(new_user)
        return {
            "message": "Sign up completed!",
            "status_code": 200,
            "info_account": result
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Error, username is used or identity_number existed!"
        )


def process_change_info(username: str, info_change: ChangeInfoRequest, token: str) -> dict:
    exists_acc, conn = exists_account_by_token(token)
    if exists_acc.get("username", "") == username:
        new_info = {item for item in info_change.dict().items()
                    if item[1] != None}
        conn.update_one({"secret_key": token}, new_info)
        new_info_acc = conn.find_one({"secret_key": token}, {"_id": 0})
        new_info_acc = {} if new_info_acc is None else dict(new_info_acc)
        return {
            "message": "Update successfully!",
            "update_info": [item[0] for item in info_change.dict().items() if item[1] != None],
            "result": new_info_acc
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can't change infomation of other accounts"
        )

def process_get_all_users(token: str) -> dict:
    results_query = []
    # check token is owned by admin or not
    admin_acc, conn = exists_account_by_token(token=token)
    # admin_acc = {}
    if admin_acc.get("user_type", "student") == "admin":
        # Admin can query the list
        results_query = list(conn.find({}, {"_id", 0}))
        print(results_query)
        if results_query:
            return {
                "message": "Successfully",
                "results": results_query
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Server Empty!"
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action is not authorized to you"
        )
