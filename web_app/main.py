from fastapi import FastAPI, HTTPException

VALID_STATES = {
    "AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE",
    "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS",
    "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS",
    "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY",
    "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
    "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV",
    "WI", "WY"
}
avila_app = FastAPI()

@avila_app.get("/")
def home():
    return{"message": "Hello, World Working on my first API Fast"}

import requests

@avila_app.post("/geocode/{city}/{state}")
def geocode(city: str, state:str):

        if not city.strip():
              raise HTTPException(
                    status_code=400,
                    detail="City is required"
              )
        

        if not state.strip():
              raise HTTPException(
                    status_code=400,
                    detail="Stats is required"
              )

        state = state.strip().upper()

        if state not in VALID_STATES:
              raise HTTPException(
                    status_code=400,
                    details="Invaild state. Use a two-letter U.S. state abbreviation"
              )
        return{
        "city": city,
        "state": state

    }




