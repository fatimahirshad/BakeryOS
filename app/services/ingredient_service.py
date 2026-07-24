from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient
from app.schemas.ingredient import IngredientCreate, IngredientUpdate


class IngredientService:

    @staticmethod
    def create_ingredient(db: Session, ingredient_data: IngredientCreate):

        existing = (
            db.query(Ingredient)
            .filter(func.lower(Ingredient.name) == ingredient_data.name.lower())
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ingredient already exists."
            )

        ingredient = Ingredient(
    name=ingredient_data.name,
    unit=ingredient_data.unit.value.lower(),
    stock=ingredient_data.stock,
)

        db.add(ingredient)
        db.commit()
        db.refresh(ingredient)

        return ingredient

    @staticmethod
    def get_ingredients(db: Session):
        return db.query(Ingredient).all()

    @staticmethod
    def get_ingredient(db: Session, ingredient_id: int):

        ingredient = (
            db.query(Ingredient)
            .filter(Ingredient.id == ingredient_id)
            .first()
        )

        if not ingredient:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Ingredient not found."
            )

        return ingredient

    @staticmethod
    def update_ingredient(
        db: Session,
        ingredient: Ingredient,
        ingredient_data: IngredientUpdate,
    ):

        if ingredient_data.name is not None:
            ingredient.unit = ingredient_data.unit.value.lower()

            existing = (
                db.query(Ingredient)
                .filter(
                    func.lower(Ingredient.name) == ingredient_data.name.lower(),
                    Ingredient.id != ingredient.id,
                )
                .first()
            )

            if existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Ingredient already exists."
                )

            ingredient.name = ingredient_data.name

        if ingredient_data.unit is not None:
            ingredient.unit = ingredient_data.unit

        if ingredient_data.stock is not None:
            ingredient.stock = ingredient_data.stock

        db.commit()
        db.refresh(ingredient)

        return ingredient

    @staticmethod
    def update_status(
        db: Session,
        ingredient: Ingredient,
        is_active: bool,
    ):

        ingredient.is_active = is_active

        db.commit()
        db.refresh(ingredient)

        return ingredient

    @staticmethod
    def delete_ingredient(
        db: Session,
        ingredient: Ingredient,
    ):

        db.delete(ingredient)
        db.commit()