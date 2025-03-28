from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from pydantic import BaseModel

from config import logger as logging
from auth.schemas import JWTSession
from auth.dependencies import get_jwt_session
from .schemas import Backup, ImportHandleType

class BackupResponse(BaseModel):
    __root__: Dict[str, Any]

router = APIRouter(redirect_slashes=True)


@router.post("/upload-backup", response_model=BackupResponse, description="Upload a Backup")
async def upload_backup(
        backup: Backup,
        import_handle: ImportHandleType,
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        return s.api.upload_backup(backup.json(), import_handle)
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))
