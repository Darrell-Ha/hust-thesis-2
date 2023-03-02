from fastapi import HTTPException, status
from typing import Tuple
from datetime import datetime
from pymongo.collection import Collection
from src.model.db import create_connection_mdb
from src.model.user import *
from .prepare_str import *

__all__ = [
    "LoginRequest",
    "SignUpRequest",
    "ChangeInfoRequest",
    "process_login",
    "process_sign_up",
    "process_get_all_users",
    "process_change_info",
    "process_delete_account"
]


def validate_user(username: str, password: str) -> Tuple[dict, Collection]:
    '''
    Check user loginning to sis is valid or not
    '''
    conn = create_connection_mdb(collection_name="accounts")
    res = conn.find_one(
        {"username": username},
        {"_id": 0}
    )
    user_pass = {} if res is None else dict(res)
    user_in_sis = decode_token(user_pass.get("password", ""))
    if user_in_sis.get("username", "") == username and user_in_sis.get("password", "") == password:
        user = user_pass
        user.pop("password")
    else:
        user = {}
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
        new_user = dict(request.dict())
        info_log = {
            "username": new_user.get("username", ""),
            "password": new_user.get("password", "")
        }
        new_user.update(
            {
                "password": generate_token(info_log),
                "create_account_time": convert_datetime_to_str(datetime.now()),
                "birthday": convert_date_to_str(new_user.get("birthday", ""))
            }
        )
        sis_token = generate_sis_token(new_user)
        new_user.update({"secret_key": f'sis_{sis_token}'})
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
        new_info = standardize_json({item[0]: item[1] for item in dict(info_change.dict()).items()
                                     if item[1] != None})
        new_info.update(
            {"last_updated_time": convert_datetime_to_str(datetime.now())})
        if any(field in new_info.keys() for field in {"username", "password"}):
            new_info_log = {
                "username": new_info.get("username", exists_acc['username']),
                "password": new_info.get("password", exists_acc['password'])
            }
            new_info.update({'password': generate_token(new_info_log)})
        conn.update_one({"secret_key": token}, {"$set": new_info})
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
        results_query = list(conn.find({}, {"_id": 0}))
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


def process_delete_account(identity_number: str, token: str) -> dict:
    # check token is owned by admin or not
    admin_acc, conn = exists_account_by_token(token=token)
    # admin_acc = {}
    if admin_acc.get("user_type", "student") == "admin":
        res = conn.delete_one({"identity_number": identity_number})
        if res.deleted_count > 0:
            return {
                "message": f"Delete student: {identity_number} successfully",
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="This action is not authorized to you"
        )
