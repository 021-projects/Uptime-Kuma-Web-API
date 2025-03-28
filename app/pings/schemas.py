from typing import Dict, Any
from pydantic import BaseModel


class PingsResponse(BaseModel):
    __root__: Dict[str, Any]