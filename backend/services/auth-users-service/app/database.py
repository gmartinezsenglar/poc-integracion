from functools import lru_cache
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from .config import get_settings


@lru_cache
def session_factory():
    url = get_settings().database_url
    if not url:
        raise RuntimeError("DATABASE_URL no configurada")
    engine = create_engine(url, pool_pre_ping=True, pool_size=2, max_overflow=1, connect_args={"connect_timeout": 8})
    return sessionmaker(bind=engine, expire_on_commit=False)


def get_db():
    try:
        with session_factory()() as session:
            yield session
    except RuntimeError:
        raise HTTPException(503, "Base de datos no configurada") from None
