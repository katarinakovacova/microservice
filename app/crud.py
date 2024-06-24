from pydantic.types import UUID4
from sqlalchemy.orm import Session, joinedload

from . import models, schemas


def get_product_by_id(db: Session, product_id: UUID4) -> models.Product | None:
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_product_by_name(db: Session, product_name: str) -> models.Product | None:
    return db.query(models.Product).filter(models.Product.name == product_name).first()


def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.model_dump(), offers=[])
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: UUID4, product: schemas.ProductCreate) -> models.Product | None:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        return None
    
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: UUID4):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product is None:
        return
    
    db.delete(db_product)
    db.commit()


def get_offers_by_product_id(db: Session, product_id: UUID4) -> list[models.Offer] | None:
    return db.query(models.Product).options(joinedload(models.Product.offers)).filter(models.Product.id == product_id).first().offers


def get_all_products(db: Session) -> list[models.Product]:
    return db.query(models.Product).all()
