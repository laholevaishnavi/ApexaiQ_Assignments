# Troemner OIML Weight Sets scraper (Selenium + Python)
# Outputs: troemner_oiml_weight_sets.csv with columns:
# vendor, productName, model, description, productURL, cost

import csv
import time
import re
from dataclasses import dataclass, asdict
from urllib.parse import urljoin

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# If you don't use webdriver_manager, set your local chromedriver path here
try:
    from webdriver_manager.chrome import ChromeDriverManager
    CHROMEDRIVER = ChromeDriverManager().install()
except Exception:
    CHROMEDRIVER = None  # fallback if you manage chromedriver yourself

BASE_URL = "https://www.troemner.com"
CATEGORY_URL = "https://www.troemner.com/Calibration-Weights/Balance-Calibration-Weights/OIML-Calibration-Weight-Sets/c/3944"
EXPECTED_MODELS = 162  # as specified

@dataclass
class ProductRow:
    vendor: str
    productName: str
    model: str
    description: str
    productURL: str
    cost: str

class TroemnerOIMLScraper:
    def __init__(self, headless: bool = True, timeout: int = 20):
        chrome_opts = Options()
        if headless:
            chrome_opts.add_argument("--headless=new")
        chrome_opts.add_argument("--disable-gpu")
        chrome_opts.add_argument("--no-sandbox")
        chrome_opts.add_argument("--window-size=1400,900")
        chrome_opts.add_argument("--disable-dev-shm-usage")
        chrome_opts.add_argument("--start-maximized")
        chrome_opts.add_argument("--log-level=3")
        if CHROMEDRIVER:
            self.driver = webdriver.Chrome(service=Service(CHROMEDRIVER), options=chrome_opts)
        else:
            self.driver = webdriver.Chrome(options=chrome_opts)
        self.wait = WebDriverWait(self.driver, timeout)
        self.rows: list[ProductRow] = []

    def _dismiss_overlays(self):
        # Cookie/GDPR banners are site-dependent; this tries common patterns and ignores errors.
        candidates = [
            (By.XPATH, "//button[contains(., 'Accept') or contains(., 'I Agree')]"),
            (By.CSS_SELECTOR, "button#onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, "button[aria-label='Accept cookies']"),
        ]
        for by, sel in candidates:
            try:
                el = self.wait.until(EC.element_to_be_clickable((by, sel)))
                el.click()
                time.sleep(0.5)
                break
            except Exception:
                pass

    def open_category(self):
        self.driver.get(CATEGORY_URL)
        self._dismiss_overlays()
        # Wait until the listing is present
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul#resultsList")))
        # Small pause to ensure prices/descriptions load
        time.sleep(1.5)

    def _scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def _try_click_load_more(self) -> bool:
        """Click a 'Load More'/'Show More' style button if present. Return True if clicked."""
        selectors = [
            "button.load-more",
            "a.load-more",
            "button[aria-label*='Load more' i]",
            "button[aria-label*='Show more' i]",
            "a[aria-label*='Load more' i]",
        ]
        for sel in selectors:
            try:
                btn = self.driver.find_element(By.CSS_SELECTOR, sel)
                if btn.is_displayed() and btn.is_enabled():
                    self.driver.execute_script("arguments[0].click();", btn)
                    time.sleep(1.2)
                    return True
            except Exception:
                continue
        return False

    def _try_click_next(self) -> bool:
        """Click a 'Next' pagination control if present. Return True if clicked."""
        candidates = [
            (By.CSS_SELECTOR, "a[rel='next']"),
            (By.XPATH, "//a[contains(., 'Next') or contains(., 'next')]"),
            (By.CSS_SELECTOR, "li.next > a"),
        ]
        for by, sel in candidates:
            try:
                link = self.driver.find_element(by, sel)
                if link.is_displayed() and link.get_attribute("href"):
                    self.driver.execute_script("arguments[0].click();", link)
                    self.wait.until(EC.staleness_of(link))
                    self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ul#resultsList")))
                    time.sleep(1.0)
                    return True
            except Exception:
                continue
        return False

    def load_all_products(self):
        """Keep scrolling / loading until no new items appear, then try pagination 'Next' if any."""
        seen = 0
        stagnant_rounds = 0

        while True:
            # Scroll to bottom to trigger lazy loading (if used)
            self._scroll_to_bottom()
            time.sleep(0.8)

            # Try "Load more" button if present
            load_more_clicked = self._try_click_load_more()
            if load_more_clicked:
                stagnant_rounds = 0  # reset if we did load more
            else:
                stagnant_rounds += 1

            # Count items
            items = self.driver.find_elements(By.CSS_SELECTOR, "ul#resultsList > li.product-item")
            count = len(items)

            # If no growth after multiple attempts, break or try "Next"
            if count == seen:
                if stagnant_rounds >= 2:
                    # Try going to next page (if classic pagination exists)
                    next_clicked = self._try_click_next()
                    if next_clicked:
                        seen = 0
                        stagnant_rounds = 0
                        continue
                    else:
                        break
            else:
                seen = count
                stagnant_rounds = 0

        # Optional sanity log
        print(f"Discovered {seen} product tiles on listing pages.")

    def _text_or_none(self, root, by, sel):
        try:
            return root.find_element(by, sel).text.strip()
        except Exception:
            return None

    def _first_or_none(self, by, sel):
        try:
            return self.driver.find_element(by, sel)
        except Exception:
            return None

    def parse_products(self):
        cards = self.driver.find_elements(By.CSS_SELECTOR, "ul#resultsList > li.product-item")
        for li in cards:
            try:
                vendor = "troemner"

                # Model (blue) — take the SKU from the LI's data-code, with fallback to span.code "(12345)"
                model = li.get_attribute("data-code") or ""
                if not model:
                    code_text = self._text_or_none(li, By.CSS_SELECTOR, "span.code")
                    if code_text:
                        m = re.search(r"\(([^)]+)\)", code_text)
                        model = m.group(1) if m else code_text.strip()

                # Product Name (red)
                name_el = li.find_element(By.CSS_SELECTOR, "h3.title a")
                product_name = name_el.text.strip()
                href = name_el.get_attribute("href")
                product_url = urljoin(BASE_URL, href)

                # Description
                description = self._text_or_none(li, By.CSS_SELECTOR, "div.description.product-description") or ""

                # Cost: prefer the visible price value; fallback to the GTM prodinfo (contains price at end)
                cost = None
                price_span = self._first_or_none(By.CSS_SELECTOR,
                                                 f"div.price.product-item-{model} span.priceValue") \
                             or li.find_element(By.CSS_SELECTOR, "div.price span.priceValue") if \
                    len(li.find_elements(By.CSS_SELECTOR, "div.price span.priceValue")) else None
                if price_span:
                    try:
                        cost = price_span.text.strip()
                    except Exception:
                        pass

                if not cost:
                    # Fallback: button with prodinfo contains ":::USD:::3,150.00"
                    try:
                        atc_btn = li.find_element(By.CSS_SELECTOR, "button.product-btn-ATC")
                        prodinfo = atc_btn.get_attribute("prodinfo") or ""
                        m = re.search(r"USD:::(.+)$", prodinfo)
                        if m:
                            cost = m.group(1).strip()
                    except Exception:
                        cost = None

                self.rows.append(ProductRow(
                    vendor=vendor,
                    productName=product_name,
                    model=model,
                    description=description,
                    productURL=product_url,
                    cost=cost
                ))
            except Exception as e:
                # Don't crash the whole run for a single bad card
                print(f"[warn] could not parse a product card: {e}")

        print(f"Parsed {len(self.rows)} rows.")

    def save_csv(self, path: str = "troemner_oiml_weight_sets.csv"):
        fieldnames = ["vendor", "productName", "model", "description", "productURL", "cost"]
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in self.rows:
                writer.writerow(asdict(row))
        print(f"Saved {len(self.rows)} rows to {path}")

    def run(self):
        try:
            self.open_category()
            self.load_all_products()
            self.parse_products()

            # Soft assertion to help you confirm the internship deliverable
            if len(self.rows) != EXPECTED_MODELS:
                print(f"[note] Expected {EXPECTED_MODELS} models, got {len(self.rows)}. "
                      f"If fewer, the site may paginate differently today or hide OOS items.")

            self.save_csv()
        finally:
            self.driver.quit()


def main():
    # create scraper object
    scraper = TroemnerOIMLScraper(headless=True)
    scraper.run()

# standard Python entry point
if __name__ == "__main__":
    main()

