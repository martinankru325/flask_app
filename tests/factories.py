import factory
from factory.alchemy import SQLAlchemyModelFactory
from faker import Faker

from app import db
from app.models import Client, ClientParking, Parking  # noqa: F401

faker = Faker()


class ClientFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    name = factory.LazyAttribute(lambda _: faker.first_name())
    surname = factory.LazyAttribute(lambda _: faker.last_name())
    credit_card = factory.LazyAttribute(
        lambda _: faker.credit_card_number() if faker.boolean() else None
    )
    car_number = factory.LazyAttribute(
        lambda _: faker.bothify(text="???-####"))


class ParkingFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session
        sqlalchemy_session_persistence = "flush"

    address = factory.LazyAttribute(lambda _: faker.address())
    opened = factory.LazyAttribute(lambda _: faker.boolean())
    count_places = factory.LazyAttribute(
        lambda _: faker.random_int(min=1, max=100))
    count_available_places = factory.LazyAttribute(lambda o: o.count_places)


# Переписываем тетсты с фабриками
def test_create_client_with_factory(db):
    client = ClientFactory()
    db.session.commit()
    assert client.id is not None


def test_create_parking_with_factory(db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
