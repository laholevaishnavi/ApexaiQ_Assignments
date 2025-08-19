from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

class QuotesScraper:
    def __init__(self, start_url):
        # Setup headless Chrome
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--window-size=1920,1080")
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.start_url = start_url
        self.quotes_list = []

    def scrape_quotes(self):
        url = self.start_url
        while url:
            self.driver.get(url)
            time.sleep(2)  # Allow page to load

            # Find all quote blocks via XPath
            quote_blocks = self.driver.find_elements(By.XPATH, "//div[@class='quote']")

            for qb in quote_blocks:
                text = qb.find_element(By.XPATH, ".//span[@class='text']").text
                author = qb.find_element(By.XPATH, ".//small[@class='author']").text
                tags = [tag.text for tag in qb.find_elements(By.XPATH, ".//div[@class='tags']/a[@class='tag']")]

                self.quotes_list.append({
                    "Quote": text,
                    "Author": author,
                    "Tags": ", ".join(tags)  # join tags into a string
                })

            # Look for 'Next' page link
            try:
                next_link = self.driver.find_element(By.XPATH, "//li[@class='next']/a")
                url = next_link.get_attribute("href")
            except:
                url = None  # No more pages

    def save_to_csv(self, filename="quotes.csv"):
        df = pd.DataFrame(self.quotes_list)
        df.to_csv(filename, index=False)
        print(df.head())  # Print first 5 rows

    def close(self):
        self.driver.quit()

# ------------------- Run the scraper -------------------
if __name__ == "__main__":
    scraper = QuotesScraper("http://quotes.toscrape.com/")
    scraper.scrape_quotes()
    scraper.save_to_csv()
    scraper.close()
