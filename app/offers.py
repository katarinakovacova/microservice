from datetime import datetime
from sqlalchemy.orm import Session

import httpx

from . import crud, schemas, models


def refresh_access_token(offers_base_url: str, refresh_token: str) -> str | None:
    response = httpx.post(f"{offers_base_url}/api/v1/auth", headers={"Bearer": refresh_token})
    
    if response.status_code == 201:
        access_token = response.json().get("access_token")
        print(f"{datetime.now()} INFO {access_token}")
        return access_token
    else:
        print(f"{datetime.now()} ERROR {response.status_code} {response.text}")
        return None
    

def register_new_product(access_token: str, product: schemas.Product, offers_base_url: str) -> httpx.Response:
    data = product.model_dump(mode="json")
    response = httpx.post(f"{offers_base_url}/api/v1/products/register", headers={"Bearer": access_token}, json=data)
    return response


def get_product_offers(product_id: str, access_token: str, offers_base_url: str) -> list[schemas.Offer] | None:
    response = httpx.get(f"{offers_base_url}/api/v1/products/{product_id}/offers", headers={"Bearer": access_token})

    if response.status_code == 200:
        offers = [schemas.Offer.from_orm(offer) for offer in response.json()]
        print(f"{datetime.now()} INFO Obtained {len(offers)} offers for product {product_id}")
        return offers
    else:
        print(f"{datetime.now()} ERROR {response.status_code} {response.text}")
        return None


def update_offers(offers_base_url: str, access_token: str, db: Session):
    db_products = crud.get_all_products(db)

    for db_product in db_products:
        offers = get_product_offers(db_product.id, access_token, offers_base_url)
        if offers is None:
            continue
        else:
            db_offers = [models.Offer(**offer.model_dump()) for offer in offers]
            db_product.offers = db_offers
            db.commit()
            db.refresh(db_product)
