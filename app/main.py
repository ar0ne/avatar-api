from fastapi import FastAPI

from .avatars.router import router as avatars_router


app = FastAPI()

app.include_router(avatars_router)

