from typing import Dict, Any
from pydantic import BaseModel


class UptimesResponse(BaseModel):
    __root__: Dict[str, Any]