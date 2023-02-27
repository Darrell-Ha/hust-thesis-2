from typing import Tuple
from datetime import datetime
from pymongo.collection import Collection
import jwt
from src.model.db import create_connection_mdb
from src.model.user import *

__all__ = [
    "LoginRequest",
    "SignUpRequest",
    "RoleName",
    "process_login",
    "process_sign_up",
    "process_get_all_users",
    "process_set_privilege_user"
]


def validate_user(request_log: LoginRequest)-> Tuple[list, Collection]:
    '''
    Check user loginning to sis is valid or not
    '''
    conn = create_connection_mdb(collection_name="accounts")
    users = list(conn.find(
        {"$and": [
            {"username": request_log.username},
            {"password": request_log.password}
        ]}, 
        {"username": 1, "password": 1}
    ))
    return users, conn

def exists_account(request_sign_up: SignUpRequest) -> Tuple[list, Collection]:
    '''
    Check user loginning to sis is exists or not by username or id_student
    '''
    conn = create_connection_mdb(collection_name="accounts")
    users = list(conn.find(
        {"$or": [
            {"username": request_sign_up.username},
            {"identity_number": request_sign_up.identity_number}
        ]}, 
        {"username": 1, "identity_number": 1})
    )
    return users, conn

def process_login(request: LoginRequest) -> dict:
    try:
        valid_user, conn = validate_user(request)
        if valid_user:
            user = valid_user[0]
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
                "message": f"Hello {valid_user.get('username', '')}", ## name or something to show that exists
                "info": valid_user
            }
        else:
            return {
                "message": "This account hasn't existed yet, please sign up to continue!",
                "status_code": 403
            }
    except Exception as e:
        print(e)


def process_sign_up(request: SignUpRequest) -> dict:
    exist_acc, conn = exists_account(request)
    if not exist_acc:
        ## Insert to mongodb:
        new_user = request.dict()
        new_user.update({"create_account_time": datetime.now().strftime("%Y-%m-%d %H-%M-%S")})
        secret_key = f'{new_user.get("username")}{new_user.get("username")}'
        new_user.update({"birthday": new_user.get("birthday", "").strftime("%Y-%m-%d")})
        token = jwt.encode(new_user, secret_key, algorithm='HS256')
        new_user.update({"secret_key": f'sis_{token.split(".")[2]}'})
        conn.insert_one(new_user)
        return {
            "message": "Sign up completed!",
            "status_code": 200,
            "info_account": new_user
        }
    else:
        return {
            "meassage": "Error, account existed!",
            "status_code": 304
        }

def process_get_all_users() -> dict:
    response = []
    ## Query in mongodb account with client
    try: 
        conn = create_connection_mdb(collection_name="accounts")
        response = list(conn.find())
        if response:
            return response
        else:
            return {
                "meassage": "Server Empty!",
                "status_code": 500
            }
    except Exception as e:
        return {
            "message": e
        }

def process_set_privilege_user(username: str, role: RoleName) -> dict:
    return {
        "username": username,
        "new_privilege": role
    }
