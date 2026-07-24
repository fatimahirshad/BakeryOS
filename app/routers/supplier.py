from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models.user import User
from app.schemas.supplier import (
    SupplierCreate,
    SupplierUpdate,
    SupplierStatusUpdate,
    SupplierResponse,
)
from app.services.supplier_service import SupplierService

router = APIRouter(
    prefix="/suppliers",
    tags=["Suppliers"]
)


@router.post(
    "/",
    response_model=SupplierResponse,
    status_code=status.HTTP_201_CREATED
)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return SupplierService.create_supplier(db, supplier)


@router.get(
    "/",
    response_model=list[SupplierResponse]
)
def get_suppliers(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return SupplierService.get_suppliers(db)


@router.get(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return SupplierService.get_supplier(db, supplier_id)


@router.put(
    "/{supplier_id}",
    response_model=SupplierResponse
)
def update_supplier(
    supplier_id: int,
    supplier_data: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    supplier = SupplierService.get_supplier(db, supplier_id)

    return SupplierService.update_supplier(
        db,
        supplier,
        supplier_data,
    )


@router.patch(
    "/{supplier_id}/status",
    response_model=SupplierResponse
)
def update_supplier_status(
    supplier_id: int,
    status_data: SupplierStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    supplier = SupplierService.get_supplier(db, supplier_id)

    return SupplierService.update_status(
        db,
        supplier,
        status_data.is_active,
    )


@router.delete(
    "/{supplier_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    supplier = SupplierService.get_supplier(db, supplier_id)

    SupplierService.delete_supplier(db, supplier)