import unittest
from app.scraper.news_spider import NewsSpider

class TestNewsSpider(unittest.TestCase):
    def test_scraper(self):
        spider = NewsSpider()
        self.assertIsNotNone(spider)
