"""
Troemner OIML Calibration Weight Sets Scraper
---------------------------------------------
This script extracts all products from the given category page.
Output: troemner_oiml_weight_sets.csv with columns:
vendor | productName | model | description | productURL | cost
"""

import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# -------- CONFIG -------- #
BASE_URL = "https://www.troemner.com"
CATEGORY_URL = "https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944"
EXPECTED_MODELS = 162   # as per requirement

class TroemnerScraper:
    def __init__(self, headless=True):
        options = Options()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.data = []

    def open_page(self):
        self.driver.get(CATEGORY_URL)
        time.sleep(3)   # let page load fully

    def load_all_products(self):
        """
        Scrolls / clicks until all products are visible.
        This site loads all 162 items on a single page after scrolling.
        """
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1.5)

            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:   # no more products loaded
                break
            last_height = new_height

    def scrape_products(self):
        """
        Extract product details from each product card
        """
        products = self.driver.find_elements(By.CSS_SELECTOR, "ul#resultsList > li.product-item")

        for p in products:
            try:
                vendor = "troemner"

                # Product Name (highlighted red)
                name_el = p.find_element(By.CSS_SELECTOR, "h3.title a")
                product_name = name_el.text.strip()
                product_url = name_el.get_attribute("href")

                # Model (highlighted blue)
                model = p.get_attribute("data-code")
                if not model:
                    # sometimes shown as "(12345)" → use regex to extract digits inside ()
                    code_text = p.find_element(By.CSS_SELECTOR, "span.code").text.strip()
                    match = re.search(r"\(([^)]+)\)", code_text)
                    model = match.group(1) if match else code_text

                # Description
                try:
                    description = p.find_element(By.CSS_SELECTOR, "div.description").text.strip()
                except:
                    description = ""

                # Cost (if available)
                try:
                    cost = p.find_element(By.CSS_SELECTOR, "div.price span.priceValue").text.strip()
                except:
                    cost = ""

                self.data.append([vendor, product_name, model, description, product_url, cost])

            except Exception as e:
                print("Error parsing product:", e)

    def save_csv(self, filename="troemner_oiml_weight_sets.csv"):
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["vendor", "productName", "model", "description", "productURL", "cost"])
            writer.writerows(self.data)
        print(f"Saved {len(self.data)} products to {filename}")

    def run(self):
        self.open_page()
        self.load_all_products()
        self.scrape_products()

        # sanity check
        if len(self.data) != EXPECTED_MODELS:
            print(f"⚠️ Expected {EXPECTED_MODELS} models, got {len(self.data)}")

        self.save_csv()
        self.driver.quit()


if __name__ == "__main__":
    scraper = TroemnerScraper(headless=False)  # set True if you don’t want browser window
    scraper.run()
