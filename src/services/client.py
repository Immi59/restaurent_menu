from sqlalchemy.orm import Session

from src.core.exceptions import NotFoundError
from src.database.models.client import Client
from src.repositories.client import ClientRepository
from src.schemas.client_schema import ClientUpdate
from src.services.base import BaseService


class ClientService(BaseService[Client]):
    def __init__(self, repository: ClientRepository) -> None:
        super().__init__(repository)

    def update(self, session: Session, id: int, obj: ClientUpdate) -> Client:
        client = self.repository.get(session, id)

        if not client:
            raise NotFoundError(detail="Client not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(client, field, value)

        updated_obj = self.repository.update(session, client)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        client = self.repository.get(session, id)

        if not client:
            raise NotFoundError(detail="Client not found")

        self.repository.delete(session, client)
