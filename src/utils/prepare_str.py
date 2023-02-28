import os
import jwt
from datetime import date, datetime
from dotenv import load_dotenv


load_dotenv("src/.env")

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM")

__all__ = [
    "generate_token",
    "sanitize_key",
    "standardize_json",
    "convert_date_to_str",
    "convert_datetime_to_str"
]

def sanitize_key(token: str) -> str:
    return token.replace("-","").replace("_", "")

def generate_token(payload: dict) -> str:
    if JWT_SECRET_ALGORITHM and JWT_SECRET_ALGORITHM:
        return sanitize_key(jwt.encode(payload, key=JWT_SECRET_KEY, algorithm=JWT_SECRET_ALGORITHM).split(".")[2])
    else:
        raise ValueError(
            "KEY OR ALGORITHMS FOR GENERATE TOKEN HAVEN'T DEFINED!")

def convert_date_to_str(_date: date) -> str:
    return _date.strftime("%Y-%m-%d")

def convert_datetime_to_str(_datetime: datetime) -> str:
    return _datetime.strftime("%Y-%m-%d %H:%M:%S")

def standardize_json(_json: dict):
    for item in _json.items():
        if isinstance(item[1], date):
            _json.update({item[0]: convert_date_to_str(item[1])})
        elif isinstance(item[1], datetime):
            _json.update({item[0]: convert_datetime_to_str(item[1])})
        else:
            continue
    return _json