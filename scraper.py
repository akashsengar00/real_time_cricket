import requests
from bs4 import BeautifulSoup
import json
import time
from datetime import datetime

BASE_URL = "https://www.espncricinfo.com/live-cricket-score"
HEADERS = {
    'User-Agent': 'Mozilla/5.0'
}
DATA_FILE = 'data.json'

def get_match_details(div):
    try:
        # Match title & link
        link_tag = div.select_one("a.ds-no-tap-higlight")
        link = "https://www.espncricinfo.com" + link_tag.get("href", "")
        title = link_tag.get_text(strip=True)

        # Teams
        teams = [p.get_text(strip=True) for p in div.select("p.ds-text-tight-m.ds-font-bold")]

        # Scores
        scores = [s.get_text(strip=True) for s in div.select("strong.ds-text-typo.ds-text-compact-xs.ds-font-bold")]

        # Status
        status_tag = div.select_one("span.ds-text-tight-s")
        status = status_tag.get_text(strip=True) if status_tag else "N/A"

        # Venue
        venue = None
        for p in div.select("p.ds-text-tight-s.ds-font-regular.ds-truncate"):
            if "•" in p.text:
                venue = p.text.split("•")[-1].strip()
                break

        return {
            "title": title,
            "link": link,
            "teams": teams,
            "scores": scores,
            "status": status,
            "venue": venue
        }
    except Exception as e:
        print("Error:", e)
        return None

def scrape_matches():
    try:
        r = requests.get(BASE_URL, headers=HEADERS)
        soup = BeautifulSoup(r.text, 'html.parser')
        match_blocks = soup.select("div.ds-px-4.ds-py-3")

        matches = [get_match_details(div) for div in match_blocks if get_match_details(div)]

        with open(DATA_FILE, 'w') as f:
            json.dump({
                "last_updated": datetime.now().isoformat(),
                "matches": matches
            }, f, indent=2)

        print(f"[{datetime.now().strftime('%H:%M:%S')}] Scraped {len(matches)} matches.")
    except Exception as e:
        print("Scraping failed:", e)

def run(interval=60):
    while True:
        scrape_matches()
        time.sleep(interval)

if __name__ == "__main__":
    run()
