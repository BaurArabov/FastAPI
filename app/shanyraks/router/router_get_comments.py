from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.utils import AppModel

from ...auth.adapters.jwt_service import JWTData
from ...auth.router.dependencies import parse_jwt_user_data
from ..service import Service, get_service
from . import router


class GetMyShanyrakResponse(AppModel):
    comments: List[Any] 


@router.get("/{shanyrak_id}/comments", response_model=GetMyShanyrakResponse)
def get_comments(
    shanyrak_id: str,
    svc: Service = Depends(get_service),
) -> GetMyShanyrakResponse:
    shanyrak_comments = svc.repository.get_comments(shanyrak_id)
    return GetMyShanyrakResponse(comments=shanyrak_comments)