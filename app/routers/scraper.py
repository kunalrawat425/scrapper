from fastapi import APIRouter, Depends, HTTPException, Header
from app.services.scraper import Scraper
from typing import Optional

from app.config import API_TOKEN

router = APIRouter()

# Dependency function for authentication
def authenticate(authorization: Optional[str] = Header(None)):
    if authorization != f"Bearer {API_TOKEN}":
        raise HTTPException(status_code=403, detail="Unauthorized")

@router.get("/scrape")
async def scrape(max_pages: int = 5, proxy: Optional[str] = None, authorization: str = Depends(authenticate)):
    scraper = Scraper(base_url="https://dentalstall.com/shop/", max_pages=max_pages, proxy=proxy)
    scraper.scrape()
    return {"message": "Scraping completed"}
