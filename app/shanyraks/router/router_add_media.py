from typing import List

from fastapi import Depends, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router


@router.post("/{shanyrak_id}/media")
def upload_files(
    shanyrak_id: str,
    files: List[UploadFile],
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    result = []
    for file in files:
        url = svc.s3service.upload_file(file.file, file.filename)
        svc.repository.add_media_to_shanyrak(user_id, shanyrak_id, url)
        result.append(file.filename)
    
    return {"msg": result}