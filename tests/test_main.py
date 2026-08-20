"""Tests for the FastAPI web application."""

from fastapi.testclient import TestClient

from web_app.main import avila_app

client = TestClient(avila_app)


def test_home():
    """Welcome message"""
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World Working on my first API Fast"}


def test_geocode_invalid_state():
    """validation check for stats input"""
    response = client.post("/geocode/Pittsburgh/XX")

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Invalid state. Use a two-letter U.S. state abbreviation"
    }


def test_geocode_valid_location():
    """Latutude and longitude validation input"""
    response = client.post("/geocode/Pittsburgh/PA")

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Pittsburgh"
    assert data["state"] == "PA"
    assert "latitude" in data
    assert "longitude" in data


def test_geocode_missing_city():
    """Validation for city input"""
    response = client.post("/geocode/%20%20/PA")

    assert response.status_code == 400
    assert response.json() == {"detail": "City is required"}


def test_geocode_missing_state():
    """Validation for state input to make sure no blank"""
    response = client.post("/geocode/Pittsburgh/%20%20")

    assert response.status_code == 400
    assert response.json() == {"detail": "State is required"}


def test_geocode_location_not_found():
    """Response for no city found"""
    response = client.post("/geocode/ThisCityDoesNotExistAnywhere/PA")

    assert response.status_code == 404
    assert response.json() == {"detail": "Location not found"}


def test_weather_valid_location():
    """Return weather information for a valid city and state."""
    response = client.post("/weather/Pittsburgh/PA")

    assert response.status_code == 200

    data = response.json()

    assert data["city"] == "Pittsburgh"
    assert data["state"] == "PA"
    assert "latitude" in data
    assert "longitude" in data
    assert "temperature" in data
