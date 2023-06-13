from fastapi import Depends, Response
from pydantic import BaseModel

from ..adapters.jwt_service import JWTData
from ..service import Service, get_service
from . import router
from .dependencies import parse_jwt_user_data


class UpdatePersonalDataRequest(BaseModel):
    phone: str
    name: str
    city: str


@router.patch("/users/me")
def update_personal_data(
    input: UpdatePersonalDataRequest,
    jwt_data: dict = Depends(parse_jwt_user_data),
    svc: Service = Depends(get_service),
):
    user_id = jwt_data.user_id
    svc.repository.update_user(user_id, input.dict())

    return {"status": Response(status_code=200), "msg": "Data updated successfully"}
