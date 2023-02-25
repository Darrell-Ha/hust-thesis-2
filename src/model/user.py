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
    age: int=0
    birthday: date

