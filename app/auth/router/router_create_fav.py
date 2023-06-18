from typing import Any

from fastapi import Depends, Response, status
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetUserResponse(AppModel):
    id: Any = Field(alias="_id")
    email: str
    phone: str = ""
    name: str = ""
    city: str = ""

@router.post("/users/favorites/shanyraks/{shanyrakid}", status_code=status.HTTP_200_OK)
def add_to_favourites(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
) -> Response:
    user_id = jwt_data.user_id
    svc.repository.create_fav(user_id, shanyrak_id)
    return Response(status_code=200)