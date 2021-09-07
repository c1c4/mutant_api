from db import SessionLocal
from typing import Callable, Type

from fastapi import Depends
from sqlalchemy.orm.session import Session
from starlette.requests import Request

from db.repositories.base import BaseRepository


async def get_database() -> None:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_repository(Repo_type: Type[BaseRepository]) -> Callable:
    def get_repo(db: Session = Depends(get_database)) -> Type[BaseRepository]:
        return Repo_type(db)

    return get_repo