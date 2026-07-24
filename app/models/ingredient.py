from sqlalchemy import Boolean, Column, DateTime, Integer, Numeric, String, func

from app.core.database import Base
from sqlalchemy.orm import relationship


class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)

    unit = Column(String, nullable=False)

    stock = Column(Numeric(10, 2), default=0, nullable=False)

    is_active = Column(Boolean, default=True, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    purchase_items = relationship(
    "PurchaseItem",
    back_populates="ingredient",
)