from fastapi import FastAPI
from contextlib import asynccontextmanager

from atlas.database.session import create_db_and_tables
from atlas.api.router import router
from atlas.core.config import get_settings

settings = get_settings()

#app = FastAPI(
#    title=settings.app_name,
#    version=settings.app_version,
#)

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)
app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }
