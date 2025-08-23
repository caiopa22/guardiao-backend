from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    name: str
    email: str
    password: str
    img: str
    role: str
    secrets: list[str]
    
class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    img: Optional[str] = None
    role: Optional[str] = None
    secrets: Optional[list[str]] = None