from sqlmodel import Session, SQLModel, create_engine

from atlas.core.config import get_settings
from atlas.database import models  # noqa: F401


settings = get_settings()

#DATABASE_URL = "sqlite:///atlas.db"

#engine = create_engine(
#    DATABASE_URL,
#    echo=settings.debug,
#)

engine = create_engine(
    settings.database_url,
    echo=settings.debug,
)

def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)


def get_session() -> Session:
    return Session(engine)
