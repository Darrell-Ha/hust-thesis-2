from utils.login_processing import LoginRequest, validate_user

from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/", status_code=200)
async def root():
    return {"message": "Login-CTT-SIS Microservices, "}

@app.post("/api/v1/users", description="Get information Users")
async def login(request: LoginRequest):
    user_login = validate_user(request)
    if user_login:
        return request
    else:
        return {
            "meassage": "Account hasn't exists yet, please sign up to continue!",
            "status_code": 304
        }

@app.post("/api/v1/signup")
async def signup(request: LoginRequest):
    user_login = validate_user(request)
    if user_login:
        return request
    else:
        return {
            "meassage": "Error, please try again!",
            "status_code": 500
        }
