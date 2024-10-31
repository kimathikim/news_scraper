BOT_NAME = 'news_scraper'

SPIDER_MODULES = ['app.scraper.news_spider']
NEWSPIDER_MODULE = 'app.scraper.news_spider'

# Pipelines
ITEM_PIPELINES = {
    'app.scraper.pipelines.NewsScraperPipeline': 300,
}
