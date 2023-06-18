from pydantic import BaseSettings

from app.config import database

from .adapters.here_sevice import HereService
from .adapters.s3_service import S3Service
from .repository.repository import ShanyraksRepository


class Config(BaseSettings):
    HERE_API_KEY: str

class Service:
    def __init__(
        self,
        repository: ShanyraksRepository,
    ):
        config = Config()
        self.repository = repository
        self.s3service = S3Service()
        self.here_service = HereService(config.HERE_API_KEY)


def get_service():
    repository = ShanyraksRepository(database)

    svc = Service(repository)
    return svc
