# from fastapi import APIRouter, Depends, HTTPException, status
# from src.repositories.category import CategoryRepository
# from src.schemas.category_schema import CategoryBase, CategoryCreate, CategoryUpdate
from idlelib import pathbrowser

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Category
from src.schemas.category_schema import CategoryCreate, CategoryUpdate
from src.api.v1.dependancies import get_category_service
from src.services.category import CategoryService
from src.database.session import get_session


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/")
def get_all_categories(
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return service.get_all(session=session)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_category(
        payload: CategoryCreate,
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    db_category = Category(**payload.model_dump())

    new_category = service.create(session=session, obj=db_category)
    return new_category

# @router.post("/", status_code=status.HTTP_201_CREATED)
# def create_category(
#         payload: CategoryCreate,
#         session: Session = Depends(get_session),
#         service: CategoryService = Depends(get_category_service),
# ):
#     new_category = service.create(session, obj=payload)
#     return new_category

@router.get("/{category_id}", status_code=status.HTTP_200_OK)
def get_category_by_id(
        category_id: int,
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    return service.get(session, category_id)

@router.patch("/{category_id}", status_code=status.HTTP_200_OK)
def update_category_by_id(
        category_id: int,
        payload: CategoryUpdate,
        session: Session = Depends(get_session),
        service: CategoryService = Depends(get_category_service),
):
    updater = service.get(session, category_id).name = payload.name

    return service.update(session, obj=updater)
