import uuid
from datetime import timedelta
from typing import Annotated
from fastapi.routing import APIRouter
from fastapi import Depends, UploadFile
from fastapi.responses import StreamingResponse
from minio.error import S3Error
from .error import AvatarNotFoundError

from ..minio.client import minio_client
from .. import config
from ..config import get_settings


router = APIRouter(
    prefix="/avatars", tags=["avatar"], responses={404: {"data": "Not found"}}
)


@router.get("/{avatar_id}", tags=["avatar"])
async def get_avatar(
    avatar_id: str, settings: Annotated[config.Settings, Depends(get_settings)]
):
    if not minio_client.bucket_exists(settings.bucket_name):
        minio_client.make_bucket(settings.bucket_name)

    try:
        avatar = minio_client.get_object(settings.bucket_name, avatar_id)
    except S3Error:
        raise AvatarNotFoundError(
            status_code=404, detail=f"Avatar with id '{avatar_id}' not found."
        )

    return StreamingResponse(avatar)


@router.get("/{avatar_id}/url", tags=["avatar"])
async def get_avatar_presigned_url(
    avatar_id: str, settings: Annotated[config.Settings, Depends(get_settings)]
):
    if not minio_client.bucket_exists(settings.bucket_name):
        minio_client.make_bucket(settings.bucket_name)

    try:
        minio_client.get_object(settings.bucket_name, avatar_id)
    except S3Error:
        raise AvatarNotFoundError(
            status_code=404, detail=f"Avatar with id '{avatar_id}' not found."
        )

    # todo: create new presigned url each time
    expires = timedelta(hours=2)
    return {
        "url": minio_client.presigned_get_object(
            settings.bucket_name, avatar_id, expires=expires
        ),
        "expires": expires,
    }


@router.post("/upload", tags=["avatar"])
async def create_avatar(
    file: UploadFile, settings: Annotated[config.Settings, Depends(get_settings)]
):
    avatar_id = str(uuid.uuid4())
    result = minio_client.put_object(
        settings.bucket_name,
        avatar_id,
        file.file,
        length=-1,
        part_size=10 * 1024 * 1024,
    )
    return {"avatar_id": avatar_id}
