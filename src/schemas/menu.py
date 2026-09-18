from datetime import datetime

from pydantic import BaseModel, Field


class MenuBase(BaseModel):
    id: int
    name: str
    created_at: datetime


class MenuCreate(BaseModel):
    name: str = Field(min_length=3, max_length=50)


class MenuUpdate(MenuCreate):
    pass