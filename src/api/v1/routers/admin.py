from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Admin
from src.schemas.admin_schema import AdminCreate, AdminBase, AdminUpdate
from src.api.v1.dependancies import get_admin_service
from src.services.admin import AdminService
from src.database.session import get_session

router = APIRouter(prefix="/admins", tags=["admins"])


@router.get("/", response_model=list[AdminBase])
def get_all_admins(
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    return service.get_all(session=session)


@router.post("/", response_model=AdminBase, status_code=status.HTTP_201_CREATED)
def create_admin(
        payload: AdminCreate,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    db_admin = Admin(**payload.model_dump())
    new_admin = service.create(session=session, obj=db_admin)
    return new_admin


@router.get("/{category_id}", response_model=AdminBase, status_code=status.HTTP_200_OK)
def get_admin_by_id(
        category_id: int,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    return service.get(session, category_id)


@router.put("/{category_id}", response_model=AdminBase, status_code=status.HTTP_200_OK)
def update_admin(
        payload: AdminUpdate,
        category_id: int,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):

    return service.update(session, category_id, payload)


@router.delete("/{admin_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_admin(
        admin_id: int,
        session: Session = Depends(get_session),
        service: AdminService = Depends(get_admin_service),
):
    return service.delete(session, admin_id)  # noqa
