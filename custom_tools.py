from dotenv import load_dotenv
from langchain.tools import tool
from tavily import TavilyClient
from bs4 import BeautifulSoup
import os
import requests

load_dotenv()


API_KEY = os.getenv("TAVILY_API_KEY")

if not API_KEY:
    raise ValueError("TAVILY_API_KEY not found in .env file")

tavily = TavilyClient(api_key=API_KEY)


@tool
def web_search(query: str) -> str:
    """Search the web for recent reliable information."""
    try:
        results = tavily.search(query=query, max_results=5)

        output = []

        for r in results["results"]:
            output.append(
                f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}"
            )

        return "\n----\n".join(output)

    except Exception as e:
        return f"Search failed: {str(e)}"


@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(
            ["script", "style", "nav", "footer", "header", "aside", "noscript", "form"]
        ):
            tag.decompose()

        text = soup.get_text(separator=" ", strip=True)
        text = " ".join(text.split())
        return text[:3000]
    except Exception as e:
        return f"Could not scrape URL: {str(e)}"
