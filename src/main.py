from utils.login_processing import *
from model.db import MongoConnection

# from typing import Union
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/", status_code=200)
async def root():
    return {"message": "Login-CTT-SIS Microservices, "}

@app.get("/api/v1/users", description="Get information account in SIS, ")
async def get_all_users():
    response = []
    ## Query in mongodb account with client
    try: 
        client_mdb = MongoConnection().get_client()
        collection_acc = client_mdb.get_database("login_service").get_collection("account")
        response = collection_acc.find({})
        if response:
            return response
        else:
            return {
                "meassage": "Server Empty!",
                "status_code": 500
            }
    except Exception as e:
        return {
            "message": e.__str__
        }

@app.post("/api/v1/users/login", description="Login sis account")
async def login(request: LoginRequest):
    valid_user = validate_user(request)
    if valid_user:
        return {
            "message": f"Hello" ## name or something to show that exists
        }
    else:
        return {
            "message": "This account hasn't existed yet, please sign up to continue!",
            "status_code": 403
        }

@app.post("/api/v1/users", description="Sign-up account to sis")
async def sign_up(request: SignUpRequest):

    if not exists_account(request):
        ## Insert to mongodb:
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
    