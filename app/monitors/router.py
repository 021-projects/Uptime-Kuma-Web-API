from fastapi import APIRouter, Depends, HTTPException, Path
from uptime_kuma_api import UptimeKumaException
from typing import Dict, List, Any
from pydantic import BaseModel

from .schemas import Monitor, MonitorUpdate, MonitorTag, MonitorsResponse, MonitorDashboardResponse, MonitorActionResponse
from auth.schemas import JWTSession
from auth.dependencies import get_jwt_session
from config import logger as logging
from .raises import raise_monitor_not_found
from pings.utils import get_avg_pings
from uptimes.utils import get_uptimes

router = APIRouter(redirect_slashes=True)


@router.get("", response_model=MonitorsResponse, description="Get all monitors")
async def get_monitors(s: JWTSession = Depends(get_jwt_session)):
    try:
        # Convert each monitor dict to a Monitor object
        monitors_data = s.api.get_monitors()
        monitors = [Monitor(**monitor) for monitor in monitors_data]
        return {"monitors": monitors}
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{monitor_id}", response_model=Monitor, description="Get monitor by ID")
async def get_monitor(monitor_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)) -> Monitor:
    try:
        monitor_data = s.api.get_monitor(monitor_id)
        # Convert dictionary to Monitor object
        return Monitor(**monitor_data)
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{monitor_id}/dashboard", response_model=MonitorDashboardResponse, description="Get monitors dashboard data")
async def get_monitor_dashboard(
        monitor_id: int = Path(...),
        heartbeat_hours: int = 1,
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        monitor = s.api.get_monitor(monitor_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))

    response = {
        "monitor": monitor,
        "avgResponseTime": None,
        "uptimes": {
            "24": None,
            "720": None,
        },
        "cert": None,
    }

    try:
        pings = await get_avg_pings(s.api)
        if monitor_id in pings:
            response["avgResponseTime"] = pings[monitor_id]
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))

    try:
        uptimes = await get_uptimes(s.api)
        if monitor_id in uptimes:
            response["uptimes"] = uptimes[monitor_id]
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))

    try:
        beats = s.api.get_monitor_beats(monitor_id, heartbeat_hours)
        response["heartbeats"] = beats
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))

    try:
        info = s.api.cert_info()
        if monitor_id in info:
            response["cert"] = info[monitor_id]
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))

    return response


@router.get("/{monitor_id}/cert", response_model=Dict[str, Any], description="Get monitors certificate info")
async def get_monitor_cert_info(monitor_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        info = s.api.cert_info()
        if monitor_id not in info:
            raise_monitor_not_found()
        return info[monitor_id]
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("", response_model=MonitorActionResponse, description="Create a monitor")
async def create_monitor(monitor: Monitor, s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.add_monitor(**monitor.dict())
    except TypeError as e:
        logging.error(e)
        raise HTTPException(422, str(e))
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.patch("/{monitor_id}", response_model=Dict[str, Any], description="Update a specific monitor")
async def update_monitor(
        monitor: MonitorUpdate,
        monitor_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        return {
            **s.api.edit_monitor(id_=monitor_id, **monitor.dict(exclude_unset=True)),
            "monitor": monitor.dict(exclude_unset=True)
        }
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except TypeError as e:
        logging.error(e)
        raise HTTPException(422, str(e))
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.delete("/{monitor_id}", response_model=MonitorActionResponse, description="Delete a specific monitor")
async def delete_monitor(monitor_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        # kinda dumb the api doesnt check if th id exists he just sends an event
        return s.api.delete_monitor(monitor_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("/{monitor_id}/pause", response_model=MonitorActionResponse, description="Pause a specific monitor")
async def pause_monitor(monitor_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.pause_monitor(monitor_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("/{monitor_id}/resume", response_model=MonitorActionResponse, description="Resume a specific monitor")
async def resume_monitor(monitor_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.resume_monitor(monitor_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{monitor_id}/beats", response_model=List[Dict[str, Any]], description="Get monitor beats in the last N hours ( by default its 1 hour) ")
async def monitor_beats(
        monitor_id: int = Path(...),
        hours: int = 1,
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        return s.api.get_monitor_beats(monitor_id, hours)
    except UptimeKumaException as e:
        logging.info(e)
        raise_monitor_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("/{monitor_id}/tag", response_model=MonitorActionResponse, description="Add an already created tag to a specific monitors")
async def add_monitor_tag(
        tag: MonitorTag,
        monitor_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        return s.api.add_monitor_tag(monitor_id=monitor_id, **tag.dict())
    except UptimeKumaException as e:
        logging.info(e)
        raise HTTPException(404, {"message": "Monitor or Tag not found!"})
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.delete("/{monitor_id}/tag", response_model=MonitorActionResponse, description="Delete a tag from a specific monitors")
async def delete_monitor_tag(
        tag: MonitorTag,
        monitor_id: int = Path(...),
        s: JWTSession = Depends(get_jwt_session)
):
    try:
        msg = s.api.delete_monitor_tag(monitor_id=monitor_id, **tag.dict())
    except UptimeKumaException as e:
        logging.info(e)
        raise HTTPException(404, {"message": "Monitor or Tag not found!"})
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))
