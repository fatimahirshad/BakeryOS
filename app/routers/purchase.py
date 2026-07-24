from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models.user import User
from app.schemas.purchase import PurchaseCreate, PurchaseResponse
from app.services.purchase_service import PurchaseService

router = APIRouter(
    prefix="/purchases",
    tags=["Purchases"],
)


@router.post(
    "/",
    response_model=PurchaseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_purchase(
    purchase: PurchaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return PurchaseService.create_purchase(db, purchase)


@router.get(
    "/",
    response_model=list[PurchaseResponse],
)
def get_purchases(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return PurchaseService.get_purchases(db)


@router.get(
    "/{purchase_id}",
    response_model=PurchaseResponse,
)
def get_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return PurchaseService.get_purchase(db, purchase_id)


@router.delete(
    "/{purchase_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_purchase(
    purchase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    PurchaseService.delete_purchase(db, purchase_id)