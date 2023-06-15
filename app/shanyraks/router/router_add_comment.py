from typing import List

from fastapi import Depends, Response

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data
from app.utils import AppModel

from ..service import Service, get_service
from . import router


class CreateCommentRequest(AppModel):
    content: str = ""


@router.post("/{shanyrak_id}/comments")
def add_comment(
    shanyrak_id: str,
    comment: CreateCommentRequest,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service)
):
    user_id = jwt_data.user_id
    svc.repository.add_comment_to_shanyrak(user_id, shanyrak_id, comment.content)

    return {"msg": comment.content}
    
    
    # return Response(status_code=200)