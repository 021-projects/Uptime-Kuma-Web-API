from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from config import logger as logging
from auth.schemas import JWTSession
from auth.dependencies import get_jwt_session
from .utils import get_avg_pings
from monitors.raises import raise_monitor_not_found
from .schemas import PingsResponse

router = APIRouter(redirect_slashes=True)


@router.get("", response_model=PingsResponse, description="Get average pings")
async def get_avg_ping(s: JWTSession = Depends(get_jwt_session)):
    try:
        return await get_avg_pings(s.api)
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{monitor_id}", response_model=float, description="Get average pings by monitors ID")
async def get_avg_ping_by_monitor_id(monitor_id: int, s: JWTSession = Depends(get_jwt_session)):
    try:
        pings = await get_avg_pings(s.api)

        if monitor_id not in pings:
            raise_monitor_not_found()

        return pings[monitor_id]
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))
