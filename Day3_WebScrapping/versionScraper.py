from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
import re
import time

# Base Scraper
class WebScraper:
    def __init__(self, url):
        self.url = url
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.master_list = []

    def open_site(self):
        self.driver.get(self.url)
        time.sleep(2)

    def close(self):
        self.driver.quit()

    def save_csv(self, filename, headers=None):
        df = pd.DataFrame(self.master_list, columns=headers)
        print(" DataFrame Preview (First 10 rows):")
        print(df.head(10))  # print first 10 rows
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")

    def clean_text(self, text):
        text = text.strip()

        # Skip null or empty
        if text == "" or text.lower() == "null":
            return None

        # Version number append .x if pure digit or digit.digit
        if re.match(r'^\d+(\.\d+)?$', text):
            if not text.endswith('.x'):
                text = text + ".x"

        # Date formatting to dd-mm-yyyy
        try:
            text_mod = text.replace('.', '')
            parsed_date = datetime.strptime(text_mod, "%b %d, %Y")
            text = parsed_date.strftime("%d-%m-%Y")
        except:
            pass

        return text

# Version Scraper
class VersionScraper(WebScraper):
    def scrape_versions(self, row_xpath, col_xpath):
        rows = self.driver.find_elements(By.XPATH, row_xpath)
        for row in rows:
            cols = row.find_elements(By.XPATH, col_xpath)
            if len(cols) >= 2:
                version = self.clean_text(cols[0].text)
                date = self.clean_text(cols[1].text)
                if version and date:
                    self.master_list.append([version, date])

#Run Scraper 
if __name__ == "__main__":
    scraper = VersionScraper("https://www.python.org/downloads/")
    scraper.open_site()
    scraper.scrape_versions(
        "//ol[@class='list-row-container menu']/li",
        ".//span[@class='release-number']/a | .//span[@class='release-date']"
    )
    scraper.save_csv("python_versions.csv", headers=["Version", "Release Date"])
    scraper.close()
