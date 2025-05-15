from pydantic import BaseModel
from typing import Optional

__all__ = [
    "SessionData"
]

class SessionData(BaseModel):
    user: Optional[dict] = None