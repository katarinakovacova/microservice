import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from .database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    description = Column(String)

    offers = relationship("Offer", back_populates="product")


class Offer(Base):
    __tablename__ = "offers"

    primary_key = Column(Integer, primary_key=True)
    id = Column(UUID(as_uuid=True))
    price = Column(Integer)
    items_in_stock = Column(Integer)
    product_id = Column(UUID, ForeignKey("products.id"))

    product = relationship("Product", back_populates="offers")
