from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from config import logger as logging
from auth.dependencies import get_jwt_session
from auth.schemas import JWTSession
from .utils import get_uptimes
from .schemas import UptimesResponse

router = APIRouter(redirect_slashes=True)


@router.get("", response_model=UptimesResponse, description="Uptime")
async def get_uptime(s: JWTSession = Depends(get_jwt_session)):
    try:
        return await get_uptimes(s.api)
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{monitor_id}", response_model=float, description="Uptime for a specific monitors")
async def get_monitor_uptime(monitor_id: int, s: JWTSession = Depends(get_jwt_session)):
    try:
        uptimes = await get_uptimes(s.api)
        return uptimes[monitor_id] if monitor_id in uptimes else 0
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))
