from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.role import RoleCreate, RoleUpdate


class RoleService:

    @staticmethod #We're not storing any data inside RoleService.We just use it as a container for related functions.
    def create_role(db: Session, role_data: RoleCreate):

        existing_role = (
            db.query(Role)
            .filter(func.lower(Role.name) == role_data.name.lower())
            .first()
        )

        if existing_role:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Role already exists."
            )

        role = Role(
            name=role_data.name,
            description=role_data.description
        )

        db.add(role)
        db.commit()
        db.refresh(role)

        return role

    @staticmethod
    def get_roles(db: Session):
        return db.query(Role).all()

    @staticmethod
    def get_role(db: Session, role_id: int):
        return db.query(Role).filter(Role.id == role_id).first()

    @staticmethod
    def update_role(db: Session, role: Role, role_data: RoleUpdate):
        
        if role_data.name is not None:

            existing_role = (
                db.query(Role)
                .filter(
                    func.lower(Role.name) == role_data.name.lower(),
                    Role.id != role.id
                )
                .first()
            )

            if existing_role:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Role already exists."
                )

            role.name = role_data.name

        if role_data.description is not None:
            role.description = role_data.description

        db.commit()
        db.refresh(role)

        return role

    @staticmethod
    def delete_role(db: Session, role: Role):
        db.delete(role)
        db.commit()