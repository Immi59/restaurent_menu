from datetime import datetime

from pydantic import BaseModel, Field


class ManagerBase(BaseModel):
    id: int
    name: str
    created_at: datetime


class ManagerCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class ManagerUpdate(ManagerCreate):
    pass