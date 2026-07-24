from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductStatusUpdate,
    ProductResponse,
)
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return ProductService.create_product(db, product)


@router.get(
    "/",
    response_model=list[ProductResponse]
)
def get_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return ProductService.get_products(db)


@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return ProductService.get_product(db, product_id)


@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    product = ProductService.get_product(db, product_id)

    return ProductService.update_product(
        db,
        product,
        product_data,
    )


@router.patch(
    "/{product_id}/status",
    response_model=ProductResponse
)
def update_product_status(
    product_id: int,
    status_data: ProductStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    product = ProductService.get_product(db, product_id)

    return ProductService.update_status(
        db,
        product,
        status_data.is_active,
    )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    product = ProductService.get_product(db, product_id)

    ProductService.delete_product(db, product)