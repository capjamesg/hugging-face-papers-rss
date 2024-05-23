import json

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://huggingface.co/papers"

page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")

h3s = soup.find_all("h3")

papers = []

for h3 in h3s:
    a = h3.find("a")
    title = a.text
    link = a["href"]

    papers.append({"title": title, "url": link})

feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": f"Hugging Face Papers",
    "home_page_url": BASE_URL,
    "feed_url": "https://example.org/feed.json",
    "items": [
        {
            "id": "https://paperswithcode.com" + p["url"],
            "title": p["title"].strip(),
            "content_text": p["title"].strip(),
            "url": "https://paperswithcode.com" + p["url"],
        }
        for p in papers
    ],
}

with open("feed.json", "w") as f:
    json.dump(feed, f)
