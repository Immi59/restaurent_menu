from datetime import datetime

from pydantic import BaseModel, Field


class AdminBase(BaseModel):
    id: int
    name: str
    created_at: datetime


class AdminCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class AdminUpdate(AdminCreate):
    pass