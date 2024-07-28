from fastapi import HTTPException


class AvatarNotFoundError(HTTPException):
    ...


