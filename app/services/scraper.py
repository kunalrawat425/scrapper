import requests
from bs4 import BeautifulSoup
import json
import os
import time
from typing import List, Optional
from app.config import JSON_DB_PATH
from app.models.product import Product
from app.services.cache import Cache
from app.services.notifier import Notifier

class Scraper:
    def __init__(self, base_url: str, max_pages: int = 5, proxy: Optional[str] = None, retry_delay: int = 5):
        self.base_url = base_url
        self.max_pages = max_pages
        self.proxy = proxy
        self.retry_delay = retry_delay
        self.products: List[Product] = []
        self.cache = Cache()
        self.notifier = Notifier()

    def scrape(self):
        new_products = 0

        for page in range(1, self.max_pages + 1):
            url = f"{self.base_url}page/{page}"
            print(f"Scraping page: {page}")
            response = self._get(url)
            if response:
                new_products += self._parse(response.text)

        self.save_to_json()
        self.notifier.notify(len(self.products), new_products)

    def _get(self, url: str) -> Optional[requests.Response]:
        attempt = 0
        while attempt < 3:
            try:
                proxies = {"http": self.proxy, "https": self.proxy} if self.proxy else None
                response = requests.get(url, proxies=proxies)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                print(f"Error fetching {url}: {e}")
                attempt += 1
                time.sleep(self.retry_delay)
        return None

    def _parse(self, html: str) -> int:
        soup = BeautifulSoup(html, 'html.parser')
        products = soup.select('.product')
        print(f"Found {len(products)} products")

        new_products_count = 0

        for product in products:
            title_element = product.select_one('.woo-loop-product__title a')
            price_element = product.select_one('.woocommerce-Price-amount bdi')
            image_element = product.select_one('.attachment-woocommerce_thumbnail')

            title = title_element.get_text(strip=True) if title_element else "Title not found"
            price = float(price_element.get_text(strip=True).replace('₹', '').replace(',', '')) if price_element else 0
            image_url = image_element['data-lazy-src'] if image_element and 'data-lazy-src' in image_element.attrs else "Image URL not found"

            product_data = Product(product_title=title, product_price=price, path_to_image=image_url)
            
            cached_product = self.cache.get(product_data.product_title)
            if not cached_product or cached_product.product_price != product_data.product_price:
                self.cache.set(product_data.product_title, product_data)
                self.products.append(product_data)
                new_products_count += 1

        return new_products_count

    def save_to_json(self):
        with open(JSON_DB_PATH, 'w') as file:
            json.dump([product.dict() for product in self.products], file, indent=4)
        print(f"Data successfully saved to {JSON_DB_PATH}")
