from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException, Path
from uptime_kuma_api import UptimeKumaException

from auth.schemas import JWTSession
from auth.dependencies import get_jwt_session
from .schemas import Tag, TagUpdate
from config import logger as logging
from .raises import raise_tag_not_found

router = APIRouter(redirect_slashes=True)


@router.get("", response_model=Dict[str, List[Tag]], description="Get all tags")
async def get_tags(s: JWTSession = Depends(get_jwt_session)) -> Dict[str, List[Dict]]:
    try:
        return {"tags": s.api.get_tags()}
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.post("", response_model=Tag, description="Add a tag by name and color")
async def add_tag(tag: Tag, s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.add_tag(**tag.dict())
    except TypeError as e:
        logging.error(e)
        raise HTTPException(422, str(e))
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.get("/{tag_id}", response_model=Tag, description="Get a Tag By ID")
async def get_tag(tag_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        tag = s.api.get_tag(tag_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_tag_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))

    return {"tag": tag}


@router.delete("/{tag_id}", response_model=dict, description="Delete a specific Tag By ID")
async def delete_tag(tag_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.delete_tag(tag_id)
    except UptimeKumaException as e:
        logging.info(e)
        raise_tag_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))


@router.patch("/{tag_id}", response_model=TagUpdate, description="Update a specific Tag By ID")
async def update_tag(tag: TagUpdate, tag_id: int = Path(...), s: JWTSession = Depends(get_jwt_session)):
    try:
        return s.api.edit_tag(tag_id, **tag.dict())
    except UptimeKumaException as e:
        logging.info(e)
        raise_tag_not_found()
    except Exception as e:
        logging.fatal(e)
        raise HTTPException(500, str(e))
