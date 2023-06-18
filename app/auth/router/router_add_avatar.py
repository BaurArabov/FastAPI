from typing import List

from fastapi import Depends, UploadFile

from app.auth.adapters.jwt_service import JWTData
from app.auth.router.dependencies import parse_jwt_user_data

from ..service import Service, get_service
from . import router

#TODO: check avatar uploading; finish avatar routes: get, delete avatar

@router.post("/users/avatar")
def upload_files(
    file: UploadFile,
    jwt_data: JWTData = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    url = svc.s3service.upload_file(file.file, file.filename)
    result = svc.repository.add_avatar(user_id, url)
    
    return {"msg": result}