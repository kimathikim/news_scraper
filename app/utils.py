def filter_articles(articles, country=None, topic=None):
    """Filters articles based on country and topic."""
    filtered = []
    for article in articles:
        if country and country.lower() not in article.get('country', '').lower():
            continue
        if topic and topic.lower() not in article.get('topic', '').lower():
            continue
        filtered.append(article)
    return filtered

