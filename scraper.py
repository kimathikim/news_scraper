import requests
from bs4 import BeautifulSoup

# Define the URL of the BBC News homepage or a specific section
bbc_url = "https://www.bbc.com/news"

# Send a GET request to the webpage
response = requests.get(bbc_url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article links
    articles = soup.find_all('a', href=True)

    # Extract and clean URLs
    article_urls = []
    for article in articles:
        href = article['href']
        # Filter for URLs pointing to articles (typically start with /news/)
        if href.startswith('/news'):
            full_url = f"https://www.bbc.com{href}"
            article_urls.append(full_url)

    # Remove duplicates and print the article URLs
    article_urls = list(set(article_urls))
    print("BBC News Article URLs:")
    for url in article_urls:
        print(f"{articles}  {url}")
else:
    print(f"Failed to fetch the page. Status code: {response.status_code}")

