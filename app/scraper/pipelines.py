from app.models import NewsArticle
from app import db

class NewsScraperPipeline:
    def process_item(self, item, spider):
        article = NewsArticle(
            title=item['title'],
            url=item['url'],
            source="Hacker News"
        )
        db.session.add(article)
        db.session.commit()
        return item
