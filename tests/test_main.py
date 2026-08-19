from fastapi.testclient import TestClient

from web_app.main import avila_app

client = TestClient(avila_app)

def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World Working on my first API Fast"}

def test_geocode_invalid_state():
    response = client.post("/geocode/Pittsburgh/XX")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid state. Use a two-letter U.S. state abbreviation"
    }

def test_geocode_valid_location():
    response = client.post("/geocode/Pittsburgh/PA")

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Pittsburgh"
    assert data["state"] == "PA"
    assert "latitude" in data
    assert "longitude" in data

def test_geocode_missing_city():
    response = client.post("/geocode/%20%20/PA")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "City is required"
    }

def test_geocode_missing_state():
    response = client.post("/geocode/Pittsburgh/%20%20")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "State is required"
    }

def test_geocode_location_not_found():
    response = client.post(
        "/geocode/ThisCityDoesNotExistAnywhere/PA"
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Location not found"
    }

    
