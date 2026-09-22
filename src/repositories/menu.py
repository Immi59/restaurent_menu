from sqlalchemy.orm import Session

from src.database.models import Category
from src.schemas.menu_schema import MenuCreate
from src.database.models.menu import Menu
from src.repositories.base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    model = Menu

    def update(self, session: Session, obj: Menu) -> Menu:
        session.flush()
        return obj