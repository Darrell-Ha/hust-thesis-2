from .utils.login_processing import *
from fastapi import FastAPI

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
    - **Show informations of all account in sis**: by /api/v1/admin/users
    - **Grant admin to one or more signed users**

"""

tags_metadata = [
    {
        "name": "basic",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "admin",
        "description": "Manage other users"
    },
]


app = FastAPI(
    title="Login service for SIS",
    version="v1.0.1",
    description=description,
    openapi_tags=tags_metadata,
    contact={
        "name": "Dat Trong Ha - 20195851",
        "email": "dat.ht195851@sis.hust.edu.vn"
    },
    docs_url='/'
)

@app.post("/api/v1/users/login", description="Login sis account", tags=['basic'])
async def login(request: LoginRequest):
    return process_login(request)

@app.post("/api/v1/users", description="Sign-up account to sis", tags=['basic'])
async def sign_up(request: SignUpRequest):
    return process_sign_up(request)

# @app.post("/api/v1/users/{username}/info", description="Show information of given username", tags=['basic'])
# async def show_info()

@app.get("/api/v1/admin/accounts", description="Get information account in SIS, ", tags=['admin'])
async def get_all_users():
    return process_get_all_users()
    
@app.put("/api/v1/admin/grants/{username}/{role}", tags=['admin'])
async def set_privilege_user(username: str, role: RoleName):
    return process_set_privilege_user(username, role)
