from fastapi import Depends, Response
from pydantic import BaseModel

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


@router.patch("/{shanyrak_id}/comments")
def update_comment(
    shanyrak_id: str,
    comment_id: str,
    content: str,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    update_result = svc.repository.update_comment(comment_id, shanyrak_id, user_id, content)
    if update_result.modified_count == 1:
        return Response(status_code=200)
    return Response(status_code=404)
