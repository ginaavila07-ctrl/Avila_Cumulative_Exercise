from fastapi import FastAPI
avila_app = FastAPI()

@avila_app.get("/")
def home():
    return{"message": "Hello, World Working on my first API Fast"}

import requests

@avila_app.post("/geocode/{city}/{state}")
def geocode(city: str, state:str):
    return{
        "city": city,
        "state": state
    }

