from sqlalchemy.orm import Session
from sqlalchemy import or_

from src.core.exceptions import NotFoundError
from src.database.models import Category
from src.schemas.menu_schema import MenuCreate, MenuFilter
from src.database.models.menu import Menu
from src.repositories.base import BaseRepository


class MenuRepository(BaseRepository[Menu]):
    model = Menu

    def get_all_menu_by_filters(self, session: Session, filters: MenuFilter) -> list[Menu]:
        query = session.query(self.model)
        if filters.category_id is not None:
            query = query.where(self.model.category_id == filters.category_id)

        if filters.is_active is not None:
            query = query.where(self.model.is_active == filters.is_active)

        if filters.price_m is not None and filters.price_m != "More than":
            query = query.where(self.model.price >= int(filters.price_m))

        if filters.price_l is not None and filters.price_l != "Less than":
            query = query.where(self.model.price <= int(filters.price_l))

            if int(filters.price_m) >= int(filters.price_l):
                raise NotFoundError(detail="Give right number to price")


        return list(session.scalars(query).all())

    def update(self, session: Session, obj: Menu) -> Menu:
        session.flush()
        return obj
