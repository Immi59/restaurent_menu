from sqlalchemy.orm import Session

from src.schemas.manager_schema import ManagerFilter
from src.database.models.manager import Manager
from src.repositories.base import BaseRepository


class ManagerRepository(BaseRepository[Manager]):
    model = Manager

    def get_all_manager_by_filters(self, session: Session, filters: ManagerFilter) -> list[Manager]:
        query = session.query(self.model)

        if filters.full_name is not None:
            query = query.where(self.model.full_name == filters.full_name)

        if filters.phone_number is not None:
            query = query.where(self.model.phone_number == filters.phone_number)

        return list(session.scalars(query).all())

    def get_user_by_phone_number(self, session: Session, phone_number: str) -> Manager:
        query = session.query(self.model)
        if phone_number is not None:
            query = query.where(self.model.phone_number == phone_number)

        return session.scalar(query)

    def update(self, session: Session, obj: Manager) -> Manager:
        session.flush()
        return obj