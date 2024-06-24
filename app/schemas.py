from uuid import UUID

from pydantic import BaseModel
from pydantic.types import UUID4


class ProductBase(BaseModel):
    name: str
    description: str


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: UUID4

    class Config:
        from_attributes = True


class OfferBase(BaseModel):
    price: int
    items_in_stock: int


class Offer(OfferBase):
    id: UUID

    class Config:
        from_attributes = True
