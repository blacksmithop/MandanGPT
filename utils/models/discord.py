from pydantic import BaseModel
from typing import Optional

__all__ = [
    "HelpCmdArgs"
]

# Discord
class HelpCmdArgs(BaseModel):
    cog_or_cmd_name: Optional[str] = None
    cog_name: Optional[str] = None
    cmd_name: Optional[str] = None


