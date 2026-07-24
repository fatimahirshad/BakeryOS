from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class ProductService:

    @staticmethod
    def create_product(db: Session, product_data: ProductCreate):

        existing_product = (
            db.query(Product)
            .filter(func.lower(Product.name) == product_data.name.lower())
            .first()
        )

        if existing_product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Product already exists."
            )

        product = Product(
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            stock=product_data.stock,
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def get_products(db: Session):
        return db.query(Product).all()

    @staticmethod
    def get_product(db: Session, product_id: int):

        product = db.query(Product).filter(Product.id == product_id).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found."
            )

        return product

    @staticmethod
    def update_product(
        db: Session,
        product: Product,
        product_data: ProductUpdate,
    ):

        if product_data.name is not None:

            existing_product = (
                db.query(Product)
                .filter(
                    func.lower(Product.name) == product_data.name.lower(),
                    Product.id != product.id,
                )
                .first()
            )

            if existing_product:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Product already exists."
                )

            product.name = product_data.name

        if product_data.description is not None:
            product.description = product_data.description

        if product_data.price is not None:
            product.price = product_data.price

        if product_data.stock is not None:
            product.stock = product_data.stock

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def update_status(
        db: Session,
        product: Product,
        is_active: bool,
    ):

        product.is_active = is_active

        db.commit()
        db.refresh(product)

        return product

    @staticmethod
    def delete_product(
        db: Session,
        product: Product,
    ):

        db.delete(product)
        db.commit()