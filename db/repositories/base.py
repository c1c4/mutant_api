


from db import SessionLocal


class BaseRepository:
    def __init__(self, db: SessionLocal) -> None:
        self.db = db