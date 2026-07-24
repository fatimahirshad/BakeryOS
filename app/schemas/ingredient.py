from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.utils.enums import Unit


class IngredientCreate(BaseModel):
    name: str
    unit: Unit
    stock: Decimal = Field(default=0, ge=0)


class IngredientUpdate(BaseModel):
    name: Optional[str] = None
    unit: Optional[Unit] = None
    stock: Optional[Decimal] = Field(default=None, ge=0)


class IngredientStatusUpdate(BaseModel):
    is_active: bool


class IngredientResponse(BaseModel):
    id: int
    name: str
    unit: Unit
    stock: Decimal
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)