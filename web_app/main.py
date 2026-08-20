"""FastAPI application for geocoding city and state locations."""

from typing import Any
from fastapi import FastAPI, HTTPException
import requests

VALID_STATES = {
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
}
avila_app = FastAPI()


@avila_app.get("/")
def home():
    """Return welcom Message"""
    return {"message": "Hello, World Working on my first API Fast"}


def get_coordinates(city: str, state: str):
    """Get latitude and longitude"""
    url = "https://geocoding-api.open-meteo.com/v1/search"

    params: dict[str, Any] = {
        "name": f"{city},{state}",
        "count": 1,
        "language": "en",
        "format": "json",
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException:
        return None

    if not data.get("results"):
        return None

    location = data["results"][0]

    return {
        "latitude": location["latitude"],
        "longitude": location["longitude"],
    }


def get_weather(latitude: float, longitude: float):
    """Get wather for latitude and longitude."""
    url = "https://api.open-meteo.com/v1/forecast"

    params: dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m",
        "temperature_unit": "fahrenheit",
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

    except requests.exceptions.RequestException:
        return None

    current = data.get("current")

    if not current:
        return None

    return {
        "temperature": current["temperature_2m"],
    }


@avila_app.post("/geocode/{city}/{state}")
def geocode(city: str, state: str):
    "Validating code to make sure it meet requirements"

    city = city.strip()

    if not city.strip():
        raise HTTPException(status_code=400, detail="City is required")

    state = state.strip().upper()

    if not state:
        raise HTTPException(status_code=400, detail="State is required")

    if state not in VALID_STATES:
        raise HTTPException(
            status_code=400,
            detail="Invalid state. Use a two-letter U.S. state abbreviation",
        )
    coordinates = get_coordinates(city, state)

    if coordinates is None:
        raise HTTPException(status_code=404, detail="Location not found")

    return {
        "city": city,
        "state": state,
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
    }


@avila_app.post("/weather/{city}/{state}")
def weather(city: str, state: str):
    """Return current weather for a city and state."""

    city = city.strip()

    if not city:
        raise HTTPException(status_code=400, detail="City is required")

    state = state.strip().upper()

    if not state:
        raise HTTPException(status_code=400, detail="State is required")

    if state not in VALID_STATES:
        raise HTTPException(
            status_code=400,
            detail="Invalid state. Use a two-letter U.S. state abbreviation",
        )

    coordinates = get_coordinates(city, state)

    if coordinates is None:
        raise HTTPException(status_code=404, detail="Location not found")

    weather_data = get_weather(
        coordinates["latitude"],
        coordinates["longitude"],
    )

    if weather_data is None:
        raise HTTPException(status_code=503, detail="Weather service unavailable")

    return {
        "city": city,
        "state": state,
        "latitude": coordinates["latitude"],
        "longitude": coordinates["longitude"],
        "temperature": weather_data["temperature"],
    }
