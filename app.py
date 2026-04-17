from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import os

import requests

API_KEY = "1579bdf9763142468b6bfb3e32c412f9"

app = Flask(__name__)
CORS(app)

# Correct path handling (important to avoid bugs)
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'news.json')

# Load news safely
def load_news():
    try:
        with open(DATA_PATH, 'r') as file:
            return json.load(file)
    except Exception as e:
        return {"error": str(e)}

# Route 1: Get all news
@app.route('/live-news', methods=['GET'])
def live_news():
    try:
        url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        articles = []

        for article in data.get("articles", []):
            articles.append({
                "title": article.get("title"),
                "description": article.get("description"),
                "category": "General"
            })

        return jsonify(articles)

    except Exception as e:
        return jsonify({"error": str(e)})

# Route 2: Recommendation
@app.route('/live-recommend', methods=['POST'])
def live_recommend():
    try:
        user_interest = request.json.get('interest', '')

        url = f"https://newsapi.org/v2/everything?q={user_interest}&apiKey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        articles = []

        for article in data.get("articles", []):
            articles.append({
            "title": article.get("title"),
            "description": article.get("description"),
            "category": user_interest,
            "image": article.get("urlToImage"),
            "url": article.get("url") or "#"
            })

        return jsonify(articles)

    except Exception as e:
        return jsonify({"error": str(e)})
    

@app.route('/')
def home():
    return "InsightAI Backend Running"

# Run server
if __name__ == '__main__':
    app.run(debug=True)