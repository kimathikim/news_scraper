import requests
from bs4 import BeautifulSoup
from app.models import save_article
import datetime


def scrape_website(url):
    """
    Scrapes the website and extracts headlines, summaries, authors, publication dates, and article URLs.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None

    soup = BeautifulSoup(html, "html.parser")
    headlines = soup.find_all("h2")  # Customize to match headline tags

    articles = []
    for headline in headlines:
        title = headline.get_text(strip=True)
        link = headline.find("a")["href"] if headline.find("a") else None
        article_url = (
            link if link and link.startswith(
                "http") else url + link if link else url
        )

        summary = (
            headline.find_next("p").get_text(strip=True)
            if headline.find_next("p")
            else "No summary available"
        )
        author = (
            headline.find_next("span", class_="author").get_text(strip=True)
            if headline.find_next("span", class_="author")
            else "Unknown author"
        )
        pub_date = (
            headline.find_next("time").get_text(strip=True)
            if headline.find_next("time")
            else "Unknown date"
        )

        if title:
            article = {
                "title": title,
                "summary": summary,
                "author": author,
                "pub_date": pub_date,
                "url": article_url,
                "created_at": datetime.datetime.utcnow(),  # Add timestamp
            }
            articles.append(save_article(article))
    return articles
