from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup

def search_company_info(query, max_results=5):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=max_results)
    return results

def scrape_url_text(url):
    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = " ".join(soup.get_text(separator=" ").split())
        return text[:5000]
    except Exception as e:
        return f"Error scraping: {e}"