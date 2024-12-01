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
    headlines = soup.find_all("h2")

    articles = []
    for headline in headlines:
        title = headline.get_text(strip=True)
        link = headline.find("a")["href"] if headline.find("a") else None
        article_url = (
            link if link and link.startswith("http") else url + link if link else url
        )

        # Filter out non-article URLs (customize this based on your website's URL patterns)
        if not article_url.startswith("http") or "article" not in article_url:
            continue

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
                "created_at": datetime.datetime.now(datetime.timezone.utc),  # Add timestamp
            }
            articles.append(save_article(article))
    return articles

def scrape_until_exhausted(initial_url):
    """
    Continues scraping until no new articles are found.
    """
    all_article_urls = set()
    article_urls = [initial_url]

    while article_urls:
        new_article_urls = []
        for url in article_urls:
            articles = scrape_website(url)
            if articles:
                for article in articles:
                    new_article_urls.append(article["url"])

        new_article_urls = set(new_article_urls)
        new_article_urls -= all_article_urls

        if not new_article_urls:
            break

        all_article_urls.update(new_article_urls)
        article_urls = list(new_article_urls)

    return all_article_urls

