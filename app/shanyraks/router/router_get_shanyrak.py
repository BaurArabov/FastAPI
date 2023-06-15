from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ...auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class GetShanyrakResponse(AppModel):
    shanyrak_id: Any = Field(alias="_id")
    type: str = ""
    price: int = 0
    address: str = ""
    area: float = 0
    rooms_count: int = 0
    description: str = ""
    media: List[str] = []
    comments: List[str] = []


@router.get("/{shanyrak_id}", response_model=GetShanyrakResponse)
def get_shanyrak_by_id(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
) -> dict[str, str]:
    shanyrak = svc.repository.get_shanyrak(shanyrak_id)
    if shanyrak is None:
        return Response(status_code=404)
    
    comments = shanyrak.get("comments", [])
    shanyrak["comments"] = [str(comment) for comment in comments]
    
    return GetShanyrakResponse(**shanyrak)