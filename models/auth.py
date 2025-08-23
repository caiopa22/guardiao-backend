from pydantic import BaseModel
from typing import Optional


class LoginModel(BaseModel):
    email: str
    password: str

class TokenPayload(BaseModel):
    _id: str
    email: str