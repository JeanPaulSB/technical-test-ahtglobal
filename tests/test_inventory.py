import pytest
from flask import Flask
from sqlalchemy.exc import IntegrityError
from app.inventory import bp
from app.models import Product
from app.database import db_session
from unittest.mock import patch, MagicMock


@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(bp)
    app.config["TESTING"] = True
    app.template_folder = "../app/templates"
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def mock_db_session():
    with patch("app.inventory.db_session") as mock:
        yield mock


@pytest.fixture
def mock_render_template():
    with patch("app.inventory.render_template") as mock:
        mock.return_value = ""
        yield mock


@pytest.fixture
def mock_product():
    product = MagicMock(spec=Product)
    product.name = "Test Product"
    product.price = 1000
    product.mac_address = "00:00:00:00:00:00"
    product.serial_number = "SN48952"
    product.manufacturer = "Teltonika"
    product.description = "A test router"
    return product


def test_home_route(client, mock_db_session, mock_product):
    # Arrange
    mock_db_session.query(Product).all.return_value = [mock_product]
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code == 200


def test_add_post_success(client, mock_db_session):
    test_data = {
        "name": "Test Product",
        "price": "1000",
        "mac_address": "00:00:00:00:00:00",
        "serial_number": "SN48952",
        "manufacturer": "Teltonika",
        "description": "A test router",
    }

    response = client.post("/add", data=test_data)
    assert response.status_code == 302
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()


def test_add_product_duplicate(client, mock_db_session):
    # Arrange
    test_data = {
        "name": "Test Product",
        "price": "100",
        "mac_address": "00:00:00:00:00:00",
        "serial_number": "123456",
        "manufacturer": "Test Manufacturer",
        "description": "Test Description",
    }

    mock_db_session.add.side_effect = IntegrityError("", "", "")
    # Act
    response = client.post("/add", data=test_data)
    # Assert
    assert response.status_code == 409


def test_delete_product_post(client):
    # Arrange
    product = Product(
        name="Test Product",
        price=1000,
        mac_address="00:00:00:00:00:00",
        serial_number="SN48952",
        manufacturer="Teltonika",
        description="A test router",
    )
    db_session.add(product)
    db_session.commit()

    # Act
    response = client.post(f"/delete/{product.id}")

    # Assert
    assert response.status_code == 302
    assert db_session.get(Product, product.id) is None

    # Cleanup
    db_session.rollback()


def test_delete_product_not_found(client):
    # Arrange
    product_id = 100
    # Act
    response = client.post(f"/delete/{product_id}")
    # Assert
    assert response.status_code == 404


def test_edit_product_post(client):
    # Arrange
    product = Product(
        name="Test Product",
        price=1000,
        mac_address="00:00:00:00:00:00",
        serial_number="SN48952",
        manufacturer="Teltonika",
        description="A test router",
    )
    db_session.add(product)
    db_session.commit()

    updated_data = {
        "name": "Updated Product",
        "price": "2000",
        "mac_address": "11:11:11:11:11:11",
        "serial_number": "SN48953",
        "manufacturer": "Updated Manufacturer",
        "description": "An updated router",
    }

    # Act
    response = client.post(f"/edit/{product.id}", data=updated_data)

    # Assert
    assert response.status_code == 302
    updated_product = db_session.get(Product, product.id)
    assert updated_product.name == "Updated Product"
    assert updated_product.price == 2000
    assert updated_product.mac_address == "11:11:11:11:11:11"
    assert updated_product.serial_number == "SN48953"
    assert updated_product.manufacturer == "Updated Manufacturer"
    assert updated_product.description == "An updated router"

    # Cleanup
    db_session.delete(updated_product)
    db_session.commit()
    db_session.rollback()


def test_edit_product_not_found(client):
    # Arrange
    product_id = 100
    # Act
    response = client.post(f"/edit/{product_id}")
    # Assert
    assert response.status_code == 404
