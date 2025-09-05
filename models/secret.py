from pydantic import BaseModel, Field
from typing import Optional
from typing import List, Tuple


class Secret(BaseModel):
    title: str
    secret: str

class AlterSecret(BaseModel):
    title: Optional[str] 
    secret: Optional[str]