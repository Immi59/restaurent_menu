from sqlalchemy.orm import Session
from src.database.models.admin import Admin
from src.repositories.base import BaseRepository


class AdminRepository(BaseRepository[Admin]):
    model = Admin

    def get_user_by_phone_number(self, session: Session, email: str) -> Admin:
        query = session.query(self.model)
        if email is not None:
            query = query.where(self.model.email == email)

        return session.scalar(query)

    def update(self, session: Session, obj: Admin) -> Admin:
        session.flush()
        return obj
