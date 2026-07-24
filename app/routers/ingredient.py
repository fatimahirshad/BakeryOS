from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import require_admin
from app.models.user import User
from app.schemas.ingredient import (
    IngredientCreate,
    IngredientResponse,
    IngredientStatusUpdate,
    IngredientUpdate,
)
from app.services.ingredient_service import IngredientService

router = APIRouter(
    prefix="/ingredients",
    tags=["Ingredients"],
)


@router.post(
    "/",
    response_model=IngredientResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_ingredient(
    ingredient: IngredientCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return IngredientService.create_ingredient(db, ingredient)


@router.get(
    "/",
    response_model=list[IngredientResponse],
)
def get_ingredients(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return IngredientService.get_ingredients(db)


@router.get(
    "/{ingredient_id}",
    response_model=IngredientResponse,
)
def get_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    return IngredientService.get_ingredient(db, ingredient_id)


@router.put(
    "/{ingredient_id}",
    response_model=IngredientResponse,
)
def update_ingredient(
    ingredient_id: int,
    ingredient_data: IngredientUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    ingredient = IngredientService.get_ingredient(db, ingredient_id)

    return IngredientService.update_ingredient(
        db,
        ingredient,
        ingredient_data,
    )


@router.patch(
    "/{ingredient_id}/status",
    response_model=IngredientResponse,
)
def update_ingredient_status(
    ingredient_id: int,
    status_data: IngredientStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    ingredient = IngredientService.get_ingredient(db, ingredient_id)

    return IngredientService.update_status(
        db,
        ingredient,
        status_data.is_active,
    )


@router.delete(
    "/{ingredient_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    ingredient = IngredientService.get_ingredient(db, ingredient_id)

    IngredientService.delete_ingredient(db, ingredient)