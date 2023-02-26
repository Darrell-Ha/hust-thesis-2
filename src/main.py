from .model.db import create_connection_mdb
from .utils.login_processing import *

# from typing import Union
import jwt
from fastapi import FastAPI
from datetime import datetime, timedelta

app = FastAPI()

@app.get("/", status_code=200)
async def root():
    return {"message": "Login-CTT-SIS Microservices, "}

@app.get("/api/v1/admin/users", description="Get information account in SIS, ")
async def get_all_users():
    response = []
    ## Query in mongodb account with client
    try: 
        conn = create_connection_mdb(database_name="login_service", collection_name="accounts")
        response = list(conn.find({}))
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

@app.post("/api/v1/users/login", description="Login sis account")
async def login(request: LoginRequest):
    valid_user, conn = validate_user(request)
    if valid_user:
        user = valid_user[0]
        conn.update_one(
            {
                "username": user.get("username")
            },
            {
                "$set": {
                    "last_login": datetime.now()
                }
            }
        )
        return {
            "message": f"Hello {valid_user.get('username', '')}", ## name or something to show that exists
            "info": valid_user.__dict__
        }
    else:
        return {
            "message": "This account hasn't existed yet, please sign up to continue!",
            "status_code": 403
        }

@app.post("/api/v1/users", description="Sign-up account to sis")
async def sign_up(request: SignUpRequest):
    exist_acc, conn = exists_account(request)
    if not exist_acc:
        ## Insert to mongodb:
        new_user = request.__dict__
        new_user.update({"create_account_time": datetime.now()})
        secret_key = f'{new_user.get("username")}{new_user.get("username")}{new_user.get("create_account_time")}'
        token = jwt.encode(new_user, secret_key, algorithm='HS256')
        new_user.update({"secret_key": f'sis_{token}'})
        conn.insert_one(new_user)
        return {
            "message": "Sign up completed!",
            "status_code": 200,
            "info_account": request.__dict__
        }
    else:
        return {
            "meassage": "Error, please try again!",
            "status_code": 500
        }
    