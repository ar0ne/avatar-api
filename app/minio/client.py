from minio import Minio

from ..config import get_settings

settings = get_settings()


minio_client = Minio(
    endpoint=settings.minio_url,
    access_key=settings.minio_access_key,
    secret_key=settings.minio_secret_key,
    secure=False,
)
