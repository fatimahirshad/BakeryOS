from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, func
from sqlalchemy.orm import relationship
from app.core.database import Base


class Supplier(Base):
    __tablename__ = "suppliers"
    

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, nullable=False)

    contact_person = Column(String, nullable=True)

    phone = Column(String, unique=True, nullable=True)

    email = Column(String, unique=True, nullable=True)

    address = Column(Text, nullable=True)

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
    purchases = relationship(
        "Purchase",
        back_populates="supplier",
    )
    