from sqlalchemy.orm import Session

from src.schemas.auth_schema import TokenSchema
from src.core.security import verify_password
from src.core.exceptions import NotFoundError, UnauthorizedError, ConflictError
from src.database.models.manager import Manager
from src.repositories.manager import ManagerRepository
from src.schemas.manager_schema import ManagerUpdate, ManagerLogin
from src.services.base import BaseService


class ManagerService(BaseService[Manager]):
    def __init__(self, repository: ManagerRepository) -> None:
        super().__init__(repository)

    def login(self, session: Session, obj: ManagerLogin) -> TokenSchema:
        exists_phone_number = self.repository.get_user_by_phone_number(session, obj.phone_number)

        if not exists_phone_number:
            raise NotFoundError(detail="Phone number not exists")

        if not verify_password(obj.password, exists_phone_number.hashed_password):
            raise UnauthorizedError(detail="Password incorrect")

        return self._issue_tokens(exists_phone_number.id)

    def create(self, session: Session, obj: Manager) -> TokenSchema:
        exists_phone_number = self.repository.get_user_by_phone_number(session, obj.phone_number)

        if exists_phone_number:
            raise ConflictError(detail="Phone number already exists")

        client = self.repository.create(session, obj)
        session.commit()
        session.refresh(client)

        return self._issue_tokens(client.id)


    def update(self, session: Session, id: int, obj: ManagerUpdate) -> Manager:
        manager = self.repository.get(session, id)

        if not manager:
            raise NotFoundError(detail="Admin not found")

        update_data = obj.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(manager, field, value)

        updated_obj = self.repository.update(session, manager)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        manager = self.repository.get(session, id)

        if not manager:
            raise NotFoundError(detail="Admin not found")

        self.repository.delete(session, manager)