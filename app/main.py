
# app/main.py
from fastapi import FastAPI
from app.routers import scraper

app = FastAPI()

# Include your router
app.include_router(scraper.router)
