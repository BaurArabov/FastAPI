from typing import Any, List

from fastapi import Depends, Response, status
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class GetUserFavsResponse(AppModel):
    id: Any = Field(alias="_id")
    address: str

class Favs(AppModel):
    shanyraks: List[GetUserFavsResponse]

@router.get("/users/favorites/shanyraks/{shanyrakid}", status_code=status.HTTP_200_OK, response_model=Favs)
def get_favorites(
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
) -> Response:
    user_id = jwt_data.user_id
    result = svc.repository.get_shanyrak_fav(user_id)
    return Favs(shanyraks=result)