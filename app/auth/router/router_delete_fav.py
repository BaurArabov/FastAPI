from typing import Any, List

from fastapi import Depends, Response
from pydantic import Field

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


@router.delete("/users/favorites/shanyraks/{shanyrakid}")
def delete_favorites(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
) -> Response:
    user_id = jwt_data.user_id
    svc.repository.delete_favorite(user_id, shanyrak_id)

    return {"msg": "Deleted successfully"}