from typing import List

from fastapi import Depends, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.delete("/{shanyrak_id}/media")
def delete_files(
    shanyrak_id: str,
    media_urls: List[str],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    for url in media_urls: 
        svc.s3service.delete_file(url)
        svc.repository.delete_media_from_shanyrak(user_id, shanyrak_id, url)
    