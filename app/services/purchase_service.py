from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.ingredient import Ingredient
from app.models.purchase import Purchase
from app.models.purchase_item import PurchaseItem
from app.models.supplier import Supplier
from app.schemas.purchase import PurchaseCreate


class PurchaseService:

    @staticmethod
    def create_purchase(db: Session, purchase_data: PurchaseCreate):

        # Validate supplier
        supplier = (
            db.query(Supplier)
            .filter(Supplier.id == purchase_data.supplier_id)
            .first()
        )

        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found."
            )

        # Create purchase with initial total
        purchase = Purchase(
            supplier_id=purchase_data.supplier_id,
            total_amount=Decimal("0.00"),
        )

        db.add(purchase)

        # Flush assigns purchase.id without committing the transaction
        db.flush()

        total_amount = Decimal("0.00")

        # Process each purchased ingredient
        for item in purchase_data.items:

            ingredient = (
                db.query(Ingredient)
                .filter(Ingredient.id == item.ingredient_id)
                .first()
            )

            if not ingredient:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ingredient with ID {item.ingredient_id} not found."
                )

            subtotal = item.quantity * item.unit_price

            purchase_item = PurchaseItem(
                purchase_id=purchase.id,
                ingredient_id=item.ingredient_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
                subtotal=subtotal,
            )

            db.add(purchase_item)

            # Increase ingredient stock
            ingredient.stock += item.quantity

            total_amount += subtotal

        # Update purchase total
        purchase.total_amount = total_amount

        db.commit()

        db.refresh(purchase)

        return purchase

    @staticmethod
    def get_purchases(db: Session):
        return db.query(Purchase).all()

    @staticmethod
    def get_purchase(db: Session, purchase_id: int):

        purchase = (
            db.query(Purchase)
            .filter(Purchase.id == purchase_id)
            .first()
        )

        if not purchase:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Purchase not found."
            )

        return purchase

    @staticmethod
    def delete_purchase(db: Session, purchase_id: int):

        purchase = PurchaseService.get_purchase(db, purchase_id)

        db.delete(purchase)
        db.commit()