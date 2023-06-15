from app.config import database

from .adapters.s3_service import S3Service
from .repository.repository import ShanyraksRepository


class Service:
    def __init__(
        self,
        repository: ShanyraksRepository,
    ):
        self.repository = repository
        self.s3service = S3Service()


def get_service():
    repository = ShanyraksRepository(database)

    svc = Service(repository)
    return svc
