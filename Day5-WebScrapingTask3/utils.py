from datetime import datetime
import pandas as pd

def format_date(date_str):
    """Convert dates like 'January 1, 2024' to '2024-01-01'"""
    try:
        return datetime.strptime(date_str.strip(), "%B %d, %Y").strftime("%Y-%m-%d")
    except:
        return date_str  # leave unchanged if parsing fails

def save_to_csv(data, filename, columns):
    df = pd.DataFrame(data, columns=columns)
    df.to_csv(filename, index=False)
    print(f"✅ Saved {filename}")
