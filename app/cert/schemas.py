from typing import Dict, Any
from pydantic import BaseModel


class CertInfoResponse(BaseModel):
    __root__: Dict[str, Any]