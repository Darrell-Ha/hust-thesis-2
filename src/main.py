from .utils.login_processing import *
from fastapi import FastAPI, Header

description = """

Login service School systems

## Description:
Simulation some simple case to Login service of sis

## Privilege:

* **Users**:

    - **Login to systems** by username and password signed
    - **Sign up** with username, password and more information in detail
    - **See personal profile** has signed to sis
    - 

* **Admin**:

    - **All of privilege in users**
    - **Show informations of all account in sis**
    - **Delete Account** with specific identity_number 

"""

tags_metadata = [
    {
        "name": "Basic",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "Admin",
        "description": "Manage other users"
    },
]


app = FastAPI(
    title="Login service for SIS",
    version="1.0.0",
    description=description,
    openapi_tags=tags_metadata,
    contact={
        "name": "Dat Trong Ha - 20195851",
        "email": "dat.ht195851@sis.hust.edu.vn"
    },
    openapi_prefix="/thesis_2/api/v1"
)

@app.get("/")
async def root():
    return {"message": "Welcome to thesis2"}


@app.post("/users/login", description="Login sis account to see information account", tags=['Basic'])
async def login(request: LoginRequest):
    return process_login(request)


@app.post("/users/signup", description="Sign-up account to sis", tags=['Basic'])
async def sign_up(request: SignUpRequest):
    return process_sign_up(request)


@app.put("/users/{username}/change_info", description="Change info account", tags=['Basic'])
async def change_info(username: str, request: ChangeInfoRequest, token: str = Header(alias="x_secret_token")):
    return process_change_info(username, request, token)


@app.get("/admin/accounts", description="Get information account in SIS, ", tags=['Admin'])
async def get_all_users(token_admin: str = Header(alias="x_secret_token")):
    return process_get_all_users(token_admin)


@app.delete("/admin/offs/{identity_number}", description="Delete account with given username", tags=['Admin'])
async def delete_account(identity_number: str, token: str = Header(alias="x_secret_token")):
    return process_delete_account(identity_number, token)
