from typing import Any

from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.delete("/{shanyrak_id}")
def delete_shanyrak(
    shanyrak_id: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
)->dict[str, str]:
    user_id = jwt_data.user_id
    delete_item = svc.repository.delete_shanyrak(user_id, shanyrak_id)
    if delete_item.deleted_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)