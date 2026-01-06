import requests
import os
import pandas as pd

os.makedirs("fca_raw", exist_ok=True)

SEARCH_URL = "https://www.fca.org.uk/search/site"
KEYWORDS = ["crypto", "cryptoasset", "blockchain", "stablecoin", "digital"]

records = []

headers = {
    "User-Agent": "Mozilla/5.0",
}

for keyword in KEYWORDS:
    print(f"Searching FCA for: {keyword}")

    for page in range(0, 10):
        params = {"keys": keyword, "page": page}
        r = requests.get(SEARCH_URL, params=params, headers=headers)
        
        if r.status_code != 200:
            continue

        from bs4 import BeautifulSoup
        soup = BeautifulSoup(r.text, "html.parser")

        results = soup.select("a")

        for a in results:
            href = a.get("href", "")
            if "/publication/consultation-papers/" in href:
                url = "https://www.fca.org.uk" + href
                
                print("Found:", url)
                
                doc = requests.get(url, headers=headers)
                
                records.append({
                    "keyword": keyword,
                    "url": url,
                    "html": doc.text
                })

df = pd.DataFrame(records)
df.to_csv("fca_raw/FCA analysis.xlsx", index=False)

print(f"\nDONE. Collected {len(df)} FCA documents.")
