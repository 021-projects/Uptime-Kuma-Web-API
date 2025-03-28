from typing import Dict, Any
from pydantic import BaseModel


class InfoResponse(BaseModel):
    __root__: Dict[str, Any]