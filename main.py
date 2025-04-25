import requests
from bs4 import BeautifulSoup
import json
import time

BASE_URL = "https://diplomeo.com/search-school/results_paginated?page={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
}

results = []

for page in range(1000):
    url = BASE_URL.format(page)
    print(f"Fetching page {page}: {url}")

    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Failed to fetch page {page}: {e}")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.select('a.tw-text-heading-sm')

    for link in links:
        text = link.get_text(strip=True)
        if text:
            results.append(text)

    time.sleep(0.5)  # To be polite and avoid getting blocked

# Save to JSON
with open('diplomeo_links.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

print("Scraping completed. Data saved to diplomeo_links.json")
