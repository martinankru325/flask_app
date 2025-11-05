import pytest
from app.models import Client, Parking, ClientParking


@pytest.mark.parametrize("url", ["/clients", "/clients/1"])
def test_get_endpoints(client, url):
    response = client.get(url)
    assert response.status_code == 200


def test_create_client(client, db):
    response = client.post("/clients", json={"name": "Martin", "surname": "Ankru"})
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data


def test_create_parking(client):
    response = client.post(
        "/parkings", json={"address": "My Address", "count_places": 5}
    )
    assert response.status_code == 201


@pytest.mark.parking
def test_enter_parking(client, db):
    # Нужно использовать существующего клиента и парковку с доступными мпестами
    response = client.post("/client_parkings", json={"client_id": 1, "parking_id": 1})
    assert response.status_code == 201


@pytest.mark.parking
def test_exit_parking(client, db):
    response = client.delete("/client_parkings", json={"client_id": 1, "parking_id": 1})
    assert response.status_code == 200
