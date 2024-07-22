class Notifier:
    def notify(self, num_products: int, num_updated: int):
        print(f"Scraping completed. {num_products} products scraped, {num_updated} products updated.")
        # You can add other notification methods here (e.g., email, SMS)
