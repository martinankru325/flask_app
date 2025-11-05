from datetime import datetime, timedelta

import pytest

from app import create_app
from app import db as _db
from app.models import Client, ClientParking, Parking


@pytest.fixture(scope="module")
def app():
    app = create_app()
    app.config["TESTING"] = True
    with app.app_context():
        _db.create_all()
        # Сщздаем тестовые данные
        client = Client(
            name="Test",
            surname="User",
            credit_card="1234567890123456",
            car_number="A123BC",
        )
        parking = Parking(
            address="Test Address",
            opened=True,
            count_places=10,
            count_available_places=10,
        )
        _db.session.add_all([client, parking])
        _db.session.commit()

        # Лог заезда и выезда
        cp = ClientParking(
            client_id=client.id,
            parking_id=parking.id,
            time_in=datetime.now() - timedelta(hours=1),
            time_out=datetime.now(),
        )
        _db.session.add(cp)
        _db.session.commit()

        yield app

        with app.app_context():
            _db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db(app):
    return _db
