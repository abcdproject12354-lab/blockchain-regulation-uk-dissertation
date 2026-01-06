import requests
import pandas as pd
from tqdm import tqdm
from datetime import datetime

BASE = "https://hansard-api.parliament.uk/search.json"

KEYWORDS = ["crypto", "cryptocurrency", "blockchain", "digital currency", "stablecoin"]

all_records = []

for keyword in KEYWORDS:
    print(f"Collecting for: {keyword}")
    
    for page in range(1, 101):  # first 100 pages
        params = {
            "query": keyword,
            "startDate": "2015-01-01",
            "endDate": "2024-12-31",
            "page": page
        }

        r = requests.get(BASE, params=params)
        data = r.json()

        results = data.get("Results", [])
        if not results:
            break

        for item in tqdm(results):
            speech = item.get("Speech", {})
            member = item.get("Member", {})
            debate = item.get("Debate", {})

            all_records.append({
                "keyword": keyword,
                "date": item.get("Date"),
                "speaker": member.get("Name"),
                "party": member.get("Party"),
                "debate_title": debate.get("Title"),
                "text": speech.get("Text"),
                "url": item.get("Url")
            })

df = pd.DataFrame(all_records)
df.to_excel("Hansard.xlsx", index=False)


print(f"\nDONE. Saved {len(df)} records to hansard_raw/hansard_debates.csv")
