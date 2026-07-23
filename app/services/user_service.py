from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.security import hash_password, verify_password
from app.models.role import Role
from app.models.user import User
from app.schemas.user import UserCreate


class UserService:


    @staticmethod
    def create_user(db: Session, user_data: UserCreate):

        # Check if email already exists
        existing_user = (
            db.query(User)
            .filter(func.lower(User.email) == user_data.email.lower())
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already exists."
            )

        # Check if role exists
        role = db.query(Role).filter(Role.id == user_data.role_id).first()

        if not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role not found."
            )

        # Create user
        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            role_id=user_data.role_id,
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    @staticmethod
    def authenticate_user(db: Session, email: str, password: str):
        user = db.query(User).filter(
            func.lower(User.email) == email.lower()
        ).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password."
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive."
            )

        return user
    



    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()


    @staticmethod
    def get_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        return user
    

    @staticmethod
    def update_user(db: Session, user: User, user_data):

        if user_data.email is not None:

            existing_user = (
                db.query(User)
                .filter(
                    func.lower(User.email) == user_data.email.lower(),
                    User.id != user.id
                )
                .first()
            )

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists."
                )

            user.email = user_data.email

        if user_data.full_name is not None:
            user.full_name = user_data.full_name

        if user_data.role_id is not None:

            role = db.query(Role).filter(
                Role.id == user_data.role_id
            ).first()

            if not role:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Role not found."
                )

            user.role_id = user_data.role_id

        db.commit()
        db.refresh(user)

        return user


    @staticmethod
    def update_status(db: Session, user: User, is_active: bool):

        user.is_active = is_active

        db.commit()
        db.refresh(user)

        return user


    @staticmethod
    def delete_user(db: Session, user: User):

        db.delete(user)

        db.commit()
    
    