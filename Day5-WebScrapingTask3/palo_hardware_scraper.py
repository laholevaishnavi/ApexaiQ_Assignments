from selenium.webdriver.common.by import By
from utils import format_date, save_to_csv
from setup_driver import get_driver

URL = "https://www.paloaltonetworks.com/services/support/end-of-life-announcements/hardware-end-of-life-dates"

def scrape_hardware():
    driver = get_driver()
    driver.get(URL)

    data = []
    # Grab the main table
    tables = driver.find_elements(By.XPATH, "//table")

    for table in tables:
        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        for row in rows:
            cols = row.find_elements(By.XPATH, ".//td")
            if len(cols) < 6:  
                continue

            vendor = "Palo Alto"
            product = cols[0].text.strip()
            eol_date = format_date(cols[2].text.strip())  # EOL date is 3rd column
            # take first resource link if multiple
            resource = cols[3].find_element(By.XPATH, ".//a").get_attribute("href") if cols[3].find_elements(By.XPATH, ".//a") else None
            replacement = cols[5].text.strip()

            data.append([vendor, product, eol_date, resource, replacement])

    driver.quit()

    save_to_csv(
        data,
        "palo_hardware.csv",
        ["vendor", "productName", "EOL Date", "resource", "Recommended replacement"]
    )

if __name__ == "__main__":
    scrape_hardware()


