from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.database.models.client import Client
from src.schemas.client_schema import ClientFilter
from src.repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client]):
    model = Client

    def get_all_client_by_filters(self, session: Session, filters: ClientFilter) -> list[Client]:
        query = session.query(self.model)

        if filters.category_id is not None:
            query = query.where(self.model.created_at == filters.category_id)

        if filters.is_active is not None:
            query = query.where(self.model.is_active == filters.is_active)

        return list(session.scalars(query).all())

    def update(self, session: Session, obj: Client) -> Client:
        session.flush()
        return obj
