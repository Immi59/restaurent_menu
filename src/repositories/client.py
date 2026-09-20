from src.database.models.client import Client
from src.repositories.base import BaseRepository


class ClientRepository(BaseRepository[Client]):
    model = Client

    def update(self, session: Session, obj: Client) -> Client:
        session.flush()
        return obj
