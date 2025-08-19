from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
from datetime import datetime

def format_date(text):
    """Convert dates like 'August 13, 2025' to yyyy-mm-dd. Return None if invalid/empty."""
    try:
        return datetime.strptime(text, "%B %d, %Y").strftime("%Y-%m-%d")
    except:
        return None

def scrape_software_debug():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary")
    driver.maximize_window()

    # ✅ Wait until at least one table cell is present
    WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.XPATH, "//table//tr//td"))
    )

    data = []
    tables = driver.find_elements(By.XPATH, "//table")
    time.sleep(3)

    print("Found tables:", len(tables))

    for idx, table in enumerate(tables, 1):
        # Try to detect software name above the table
        try:
            software_name = table.find_element(By.XPATH, ".//preceding::p[1]/b").text.strip()
        except:
            try:
                software_name = table.find_element(By.XPATH, ".//preceding::h2[1]").text.strip()
            except:
                software_name = f"Unknown-{idx}"
        time.sleep(3)

        print(f"\n=== Table {idx}: {software_name} ===")

        rows = table.find_elements(By.XPATH, ".//tbody/tr")
        time.sleep(3)

        print("   Rows found:", len(rows))

        for ridx, row in enumerate(rows, 1):
            cols = row.find_elements(By.TAG_NAME, "td")
            values = [c.text.strip() for c in cols]
            time.sleep(3)

            # Debug print
            print(f"Row {ridx} raw text:", row.text)
            print(f"Row {ridx} extracted:", values)

            if not values or all(v == "" for v in values):
                continue

            # Handle 2 or 3 column tables
            if len(values) == 3:
                version, release_date, eol_date = values
                release_date = format_date(release_date)
                eol_date = format_date(eol_date)
            elif len(values) == 2:
                version, eol_date = values
                release_date = None
                eol_date = format_date(eol_date)
            else:
                continue

            data.append([software_name, version, eol_date, release_date])

    driver.quit()

    # Save to CSV
    df = pd.DataFrame(data, columns=["Software Name", "version", "EOL Date", "Release Date"])
    df.to_csv("palo_software_debug.csv", index=False)
    print("\n✅ Saved palo_software_debug.csv with", len(df), "rows.")

if __name__ == "__main__":
    scrape_software_debug()






















# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# from datetime import datetime

# def format_date(text):
#     """Convert dates like 'August 13, 2025' to yyyy-mm-dd. Return None if empty."""
#     try:
#         return datetime.strptime(text, "%B %d, %Y").strftime("%Y-%m-%d")
#     except:
#         return None

# def scrape_software():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary")
#     driver.maximize_window()

#     data = []

#     # find all tables
#     tables = driver.find_elements(By.XPATH, "//table")
#     print("Found tables:", len(tables))

#     for idx, table in enumerate(tables, 1):
#         try:
#             # software name above the table
#             software_name = table.find_element(By.XPATH, ".//preceding::p[1]/b").text.strip()
#         except:
#             software_name = f"Unknown-{idx}"

#         print(f"\n[{idx}] Software: {software_name}")

#         rows = table.find_elements(By.XPATH, ".//tbody/tr")[1:]  # skip header
#         print("   Rows found:", len(rows))

#         for row in rows:
#             cols = row.find_elements(By.TAG_NAME, "td")
#             if len(cols) == 3:  # Version, Release Date, EOL
#                 version = cols[0].text.strip()
#                 release_date = format_date(cols[1].text.strip())
#                 eol_date = format_date(cols[2].text.strip())
#             elif len(cols) == 2:  # Version, EOL only
#                 version = cols[0].text.strip()
#                 release_date = None
#                 eol_date = format_date(cols[1].text.strip())
#             else:
#                 continue

#             data.append([software_name, version, eol_date, release_date])

#     driver.quit()

#     # save to CSV
#     df = pd.DataFrame(data, columns=["Software Name", "version", "EOL Date", "Release Date"])
#     df.to_csv("palo_software.csv", index=False)
#     print("\nSaved palo_software.csv with", len(df), "rows.")

# if __name__ == "__main__":
#     scrape_software()















# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.common.by import By
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# from datetime import datetime

# def format_date(text):
#     """Convert dates like 'August 13, 2025' to yyyy-mm-dd. Return None if invalid/empty."""
#     try:
#         return datetime.strptime(text, "%B %d, %Y").strftime("%Y-%m-%d")
#     except:
#         return None

# def scrape_software():
#     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#     driver.get("https://www.paloaltonetworks.com/services/support/end-of-life-announcements/end-of-life-summary")
#     driver.maximize_window()

#     data = []

#     tables = driver.find_elements(By.XPATH, "//table")
#     print("Found tables:", len(tables))

#     for idx, table in enumerate(tables, 1):
#         # Get software name
#         try:
#             software_name = table.find_element(By.XPATH, ".//preceding::p[1]/b").text.strip()
#         except:
#             software_name = f"Unknown-{idx}"

#         # Extract headers
#         headers = [h.text.strip() for h in table.find_elements(By.XPATH, ".//thead/tr/th")]
#         print(f"\n[{idx}] {software_name} | Headers: {headers}")

#         rows = table.find_elements(By.XPATH, ".//tbody/tr") if "Version" in headers or "Product" in headers else table.find_elements(By.XPATH, ".//tbody/tr")
#         print("   Rows found:", len(rows))

#         for row in rows:
#             cols = [c.text.strip() for c in row.find_elements(By.TAG_NAME, "td")]
#             if not cols:
#                 continue

#             # Create a mapping based on headers
#             row_data = {"Software Name": software_name, "version": None, "EOL Date": None, "Release Date": None}

#             for h, val in zip(headers, cols):
#                 if "Version" in h or "Product" in h:
#                     row_data["version"] = val
#                 elif "Release" in h:
#                     row_data["Release Date"] = format_date(val)
#                 elif "End-of-Life" in h or "EOL" in h:
#                     row_data["EOL Date"] = format_date(val)

#             data.append([row_data["Software Name"], row_data["version"], row_data["EOL Date"], row_data["Release Date"]])

#     driver.quit()

#     df = pd.DataFrame(data, columns=["Software Name", "version", "EOL Date", "Release Date"])
#     df.to_csv("palo_software.csv", index=False)
#     print("\nSaved palo_software.csv with", len(df), "rows.")

# if __name__ == "__main__":
#     scrape_software()
