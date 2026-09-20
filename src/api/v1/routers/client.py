from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.database.models import Client
from src.schemas.client_schema import ClientCreate, ClientBase, ClientUpdate
from src.api.v1.dependancies import get_client_service
from src.services.client import ClientService
from src.database.session import get_session

router = APIRouter(prefix="/clients", tags=["Clients"])


@router.get("/", response_model=list[ClientBase])
def get_all_clients(
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.get_all(session=session)


@router.post("/", response_model=ClientBase, status_code=status.HTTP_201_CREATED)
def create_client(
        payload: ClientCreate,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    payload_dump = payload.model_dump()
    hashed_password = hash_password(payload_dump.get("password"))
    payload_dump["hashed_password"] = hashed_password
    payload_dump.pop("password")
    '''
    {
        "full_name2": "Bexruz",
        "email": "user@example.com",
        "hashed_password": "hgevwfuybwfuyw"
    }
    '''
    db_client = Client(**payload_dump)
    new_client = service.create(session=session, obj=db_client)
    return new_client


@router.get("/{client_id}", response_model=ClientBase, status_code=status.HTTP_200_OK)
def get_client_by_id(
        client_id: int,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.get(session, client_id)


@router.patch("/{client_id}", response_model=ClientBase, status_code=status.HTTP_200_OK)
def update_client(
        payload: ClientUpdate,
        client_id: int,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):

    return service.update(session, client_id, payload)


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
        client_id: int,
        session: Session = Depends(get_session),
        service: ClientService = Depends(get_client_service),
):
    return service.delete(session, client_id)  # noqa
