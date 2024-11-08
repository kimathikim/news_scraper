from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .scraper.scraper import scrape_website
from .models import articles_collection, get_articles
import uuid
import datetime

main = Blueprint("main", __name__)


@main.route("/scrape", methods=["GET"])
@jwt_required()
def scrape_news():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "URL parameter is required"}), 400

    articles = scrape_website(url)
    if articles:
        return jsonify({"message": "Scraping completed", "data": articles}), 200
    else:
        return jsonify({"error": "Failed to scrape articles"}), 500


@main.route("/articles", methods=["GET"])
@jwt_required()
def get_news():
    country = request.args.get("country")
    topic = request.args.get("topic")
    author = request.args.get("author")
    pub_date = request.args.get("pub_date")
    keywords = request.args.get("keywords")

    filters = {}

    if country:
        filters["country"] = country
    if topic:
        filters["topic"] = topic
    if author:
        filters["author"] = author
    if pub_date:
        filters["pub_date"] = pub_date
    if keywords:
        filters["keywords"] = keywords

    articles = get_articles(filters)
    return jsonify(articles), 200
