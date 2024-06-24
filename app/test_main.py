from fastapi.testclient import TestClient
import pytest

from .main import app, get_settings
from .database import Base, get_engine


def get_test_settings():
    settings = get_settings()
    settings.is_testing = True
    return settings


app.dependency_overrides[get_settings] = get_test_settings

settings = get_test_settings()
engine = get_engine(settings.postgres_password)


@pytest.fixture
def test_client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with TestClient(app) as client:
        yield client

    Base.metadata.drop_all(bind=engine)


product_name = "Test Product"
product_description = "This is a test product"


def test_create_product(test_client):
    # Create a product
    response = test_client.post("/products/", json={"name": product_name, "description": product_description})
    assert response.status_code == 201
    assert response.json()["id"] is not None
    assert response.json()["name"] == product_name
    assert response.json()["description"] == product_description

    # Create the product again
    response = test_client.post("/products/", json={"name": product_name, "description": product_description})
    assert response.status_code == 400


def test_read_product(test_client):
    # Create a product
    response = test_client.post("/products/", json={"name": product_name, "description": product_description})
    assert response.status_code == 201
    product_id = response.json()["id"]

    # Read the product
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 200
    assert response.json()["name"] == product_name
    assert response.json()["description"] == product_description
    assert response.json()["id"] == product_id


def test_update_product(test_client):
    # Create a product
    response = test_client.post("/products/", json={"name": product_name, "description": product_description})
    assert response.status_code == 201
    product_id = response.json()["id"]

    # Update the product
    response = test_client.put(f"/products/{product_id}", json={"name": "Updated Product", "description": "After update"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Product"
    assert response.json()["description"] == "After update"
    assert response.json()["id"] == product_id


def test_delete_product(test_client):
    # Create a product
    response = test_client.post("/products/", json={"name": product_name, "description": product_description})
    assert response.status_code == 201
    product_id = response.json()["id"]

    # Delete the product
    response = test_client.delete(f"/products/{product_id}")
    assert response.status_code == 204

    # Read the product
    response = test_client.get(f"/products/{product_id}")
    assert response.status_code == 404


def test_create_wrong_product(test_client):
    # Create a wrong product
    response = test_client.post("/products/", json={"name": None, "description": product_description})
    assert response.status_code == 422


def test_read_product_offers(test_client):
    # Create a product
    response = test_client.post("/products/", json={"name": product_name, "description": product_description})
    assert response.status_code == 201
    product_id = response.json()["id"]

    # Read the product offers
    response = test_client.get(f"/products/{product_id}/offers")
    assert response.status_code == 200
    assert response.json() == []
