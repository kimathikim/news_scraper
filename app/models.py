from pymongo import MongoClient
from app import mongo
import uuid
from datetime import datetime
from . import mongo

users_collection = mongo.db.users
articles_collection = mongo.db.articles


def save_article(article_data):
    """Save an article to MongoDB if it doesn't already exist."""
    existing_article = mongo.db.articles.find_one(
        {"title": article_data["title"], "url": article_data["url"]}
    )

    if existing_article:
        print(f"Article already exists: {article_data['title']}")
        return None

    article_data["_id"] = str(uuid.uuid4())  # UUID4 for unique identifier
    mongo.db.articles.insert_one(article_data)
    print(f"Article saved: {article_data['title']}")
    return article_data


def get_articles(filters=None):
    """Fetch articles from MongoDB with optional filters."""
    query = {}

    if filters:
        if "country" in filters:
            query["country"] = {"$regex": filters["country"], "$options": "i"}

        if "topic" in filters:
            query["topic"] = {"$regex": filters["topic"], "$options": "i"}

        if "author" in filters:
            query["author"] = {"$regex": filters["author"], "$options": "i"}

        if "pub_date" in filters:
            try:
                date_range = filters["pub_date"].split("to")
                start_date = datetime.strptime(
                    date_range[0].strip(), "%Y-%m-%d")
                end_date = datetime.strptime(date_range[1].strip(), "%Y-%m-%d")
                query["pub_date"] = {"$gte": start_date, "$lte": end_date}
            except (ValueError, IndexError):
                pass

        if "keywords" in filters:
            keywords_regex = {"$regex": filters["keywords"], "$options": "i"}
            query["$or"] = [
                {"title": keywords_regex},
                {"summary": keywords_regex},
                {"content": keywords_regex},
            ]

    return list(mongo.db.articles.find(query).sort("created_at", -1))
