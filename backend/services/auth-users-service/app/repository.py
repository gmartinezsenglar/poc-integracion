from uuid import UUID
from sqlalchemy.orm import Session
from .models import Profile


class ProfileRepository:
    def __init__(self, db: Session):
        self.db = db

    def get(self, user_id: UUID) -> Profile | None:
        return self.db.get(Profile, user_id)

    def upsert(self, user_id: UUID, nombre: str) -> Profile:
        row = self.get(user_id)
        if row is None:
            row = Profile(id=user_id, nombre=nombre)
            self.db.add(row)
        else:
            row.nombre = nombre
        self.db.commit()
        self.db.refresh(row)
        return row
