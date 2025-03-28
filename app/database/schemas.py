from typing import Dict, Any
from pydantic import BaseModel


class DBSizeResponse(BaseModel):
    unit: str
    size: int


class ShrinkResponse(BaseModel):
    message: str
    details: Dict[str, Any]