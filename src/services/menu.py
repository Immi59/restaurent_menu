from sqlalchemy.orm import Session

from src.database.models import Category
from src.core.exceptions import NotFoundError
from src.database.models.menu import Menu
from src.repositories.menu import MenuRepository
from src.schemas.menu_schema import MenuUpdate, MenuCreate
from src.services.base import BaseService


class MenuService(BaseService[Menu]):
    def __init__(self, repository: MenuRepository) -> None:
        super().__init__(repository)

    def update(self, session: Session, id: int, obj: MenuUpdate) -> Menu:
        menu = self.repository.get(session, id)

        if not menu:
            raise NotFoundError(detail="Menu not found")

        update_data = obj.model_dump(exclude_unset=True)

        if "category_id" in update_data:
            category = session.query(Category).filter(Category.id == update_data["category_id"]).first()
            if not category:
                raise NotFoundError(detail="Category not found")

        for field, value in update_data.items():
            setattr(menu, field, value)

        updated_obj = self.repository.update(session, menu)
        session.commit()
        session.refresh(updated_obj)
        return updated_obj

    def delete(self, session: Session, id: int) -> None:
        menu = self.repository.get(session, id)

        if not menu:
            raise NotFoundError(detail="Menu not found")

        self.repository.delete(session, menu)
