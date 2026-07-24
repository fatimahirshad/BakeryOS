from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.supplier import Supplier
from app.schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:

    @staticmethod
    def create_supplier(db: Session, supplier_data: SupplierCreate):

        existing_supplier = (
            db.query(Supplier)
            .filter(func.lower(Supplier.name) == supplier_data.name.lower())
            .first()
        )

        if existing_supplier:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Supplier already exists."
            )

        if supplier_data.email:
            existing_email = (
                db.query(Supplier)
                .filter(func.lower(Supplier.email) == supplier_data.email.lower())
                .first()
            )

            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists."
                )

        if supplier_data.phone:
            existing_phone = (
                db.query(Supplier)
                .filter(Supplier.phone == supplier_data.phone)
                .first()
            )

            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Phone already exists."
                )

        supplier = Supplier(
            name=supplier_data.name,
            contact_person=supplier_data.contact_person,
            phone=supplier_data.phone,
            email=supplier_data.email,
            address=supplier_data.address,
        )

        db.add(supplier)
        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def get_suppliers(db: Session):
        return db.query(Supplier).all()

    @staticmethod
    def get_supplier(db: Session, supplier_id: int):

        supplier = (
            db.query(Supplier)
            .filter(Supplier.id == supplier_id)
            .first()
        )

        if not supplier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Supplier not found."
            )

        return supplier

    @staticmethod
    def update_supplier(
        db: Session,
        supplier: Supplier,
        supplier_data: SupplierUpdate,
    ):

        if supplier_data.name is not None:

            existing_supplier = (
                db.query(Supplier)
                .filter(
                    func.lower(Supplier.name) == supplier_data.name.lower(),
                    Supplier.id != supplier.id,
                )
                .first()
            )

            if existing_supplier:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Supplier already exists."
                )

            supplier.name = supplier_data.name

        if supplier_data.email is not None:

            existing_email = (
                db.query(Supplier)
                .filter(
                    func.lower(Supplier.email) == supplier_data.email.lower(),
                    Supplier.id != supplier.id,
                )
                .first()
            )

            if existing_email:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists."
                )

            supplier.email = supplier_data.email

        if supplier_data.phone is not None:

            existing_phone = (
                db.query(Supplier)
                .filter(
                    Supplier.phone == supplier_data.phone,
                    Supplier.id != supplier.id,
                )
                .first()
            )

            if existing_phone:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Phone already exists."
                )

            supplier.phone = supplier_data.phone

        if supplier_data.contact_person is not None:
            supplier.contact_person = supplier_data.contact_person

        if supplier_data.address is not None:
            supplier.address = supplier_data.address

        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def update_status(
        db: Session,
        supplier: Supplier,
        is_active: bool,
    ):

        supplier.is_active = is_active

        db.commit()
        db.refresh(supplier)

        return supplier

    @staticmethod
    def delete_supplier(
        db: Session,
        supplier: Supplier,
    ):

        db.delete(supplier)

        db.commit()