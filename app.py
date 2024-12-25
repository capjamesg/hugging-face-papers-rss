import json

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

BASE_URL = "https://huggingface.co/papers"

page = requests.get(BASE_URL)

soup = BeautifulSoup(page.content, "html.parser")

h3s = soup.find_all("h3")

papers = []


def extract_abstraction(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    abstract = soup.find("div", {"class": "pb-8 pr-4 md:pr-16"}).text

    time_element = soup.find("time")
    datetime_str = time_element.get("datetime") if time_element else None
    if datetime_str and not datetime_str.endswith("Z"):
        datetime_str = f"{datetime_str}Z"

    if abstract.startswith("Abstract\n"):
        abstract = abstract[len("Abstract\n") :]
    abstract = abstract.replace("\n", " ")
    return abstract, datetime_str


for h3 in tqdm(h3s):
    a = h3.find("a")
    title = a.text
    link = a["href"]
    url = f"https://huggingface.co{link}"
    try:
        abstract, datetime_str = extract_abstraction(url)
    except Exception as e:
        print(f"Failed to extract abstract for {url}: {e}")
        abstract, datetime_str = "", None

    papers.append({"title": title, "url": url, "abstract": abstract, "date_published": datetime_str})

feed = {
    "version": "https://jsonfeed.org/version/1",
    "title": "Hugging Face Papers",
    "home_page_url": BASE_URL,
    "feed_url": "https://example.org/feed.json",
    "items": [
        {
            "id": p["url"],
            "title": p["title"].strip(),
            "content_text": p["abstract"].strip(),
            "url": p["url"],
            **({"date_published": p["date_published"]} if p["date_published"] else {}),
        }
        for p in papers
    ],
}

with open("feed.json", "w") as f:
    json.dump(feed, f)
