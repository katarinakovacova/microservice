import asyncio
from datetime import datetime
from functools import lru_cache

from fastapi import Depends, FastAPI, HTTPException
from pydantic.types import UUID4
from sqlalchemy.orm import Session

from . import crud, models, schemas, offers
from .config import Settings
from .database import get_engine, get_session


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
engine = get_engine(settings.postgres_password)

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = get_session(engine)
    try:
        yield db
    finally:
        db.close()


access_token = None


async def token_refresh_loop():
    global access_token
    while True:
        if not settings.is_testing:
            access_token = offers.refresh_access_token(settings.offers_base_url, settings.refresh_token)
        await asyncio.sleep(300)


async def update_offers_loop():
    while True:
        if not settings.is_testing:
            db = get_session(engine)
            offers.update_offers(settings.offers_base_url, access_token, db)
        await asyncio.sleep(30)


app = FastAPI()


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(token_refresh_loop())
    asyncio.create_task(update_offers_loop())


@app.post("/products/", response_model=schemas.Product, status_code=201)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db), settings: Settings = Depends(get_settings)):
    db_product = crud.get_product_by_name(db, product.name)

    if db_product is not None:
        raise HTTPException(status_code=400, detail="Product with this name alredy registered")
    
    db_product = crud.create_product(db=db, product=product)

    if not settings.is_testing:
        product = schemas.Product.from_orm(db_product)
        response = offers.register_new_product(access_token, product, settings.offers_base_url)

        if response.status_code == 201:
            print(f"{datetime.now()} INFO Product was successfully registered {db_product.id}")
        else: 
            print(f"{datetime.now()} ERROR Registration failed {db_product.id} {response.status_code} {response.text}")
            crud.delete_product(db, db_product.id)
            raise HTTPException(status_code=response.status_code, detail=response.text)

    return db_product


@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: UUID4, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return db_product


@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product_id: UUID4, product: schemas.ProductCreate, db: Session = Depends(get_db)):
    db_product = crud.get_product_by_id(db, product_id=product_id)

    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return crud.update_product(db=db, product_id=product_id, product=product)


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: UUID4, db: Session = Depends(get_db)):
    crud.delete_product(db=db, product_id=product_id)


@app.get("/products/{product_id}/offers", response_model=list[schemas.Offer])
def read_product_offers(product_id: UUID4, db: Session = Depends(get_db)):
    db_offers = crud.get_offers_by_product_id(db, product_id=product_id)

    if db_offers is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    return db_offers
