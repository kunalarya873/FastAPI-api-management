from typing import Optional
from pydantic import BaseModel

class Note(BaseModel):
    title: str
    desc: str
    important: Optional[bool]
