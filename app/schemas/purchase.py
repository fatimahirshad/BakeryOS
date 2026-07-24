from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, ConfigDict, Field


class PurchaseItemCreate(BaseModel):
    ingredient_id: int
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(gt=0)


class PurchaseCreate(BaseModel):
    supplier_id: int
    items: List[PurchaseItemCreate]


class PurchaseItemResponse(BaseModel):
    ingredient_id: int
    quantity: Decimal
    unit_price: Decimal
    subtotal: Decimal

    model_config = ConfigDict(from_attributes=True)


class PurchaseResponse(BaseModel):
    id: int
    supplier_id: int
    total_amount: Decimal
    created_at: datetime
    items: List[PurchaseItemResponse]

    model_config = ConfigDict(from_attributes=True)