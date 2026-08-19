from fastapi import FastAPI
avila_app = FastAPI()

@avila_app.get("/")
def home():
    return{"message": "Hello, World Working on my first API Fast"}
