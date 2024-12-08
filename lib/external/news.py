from datetime import datetime, timedelta

import requests

from config import NEWS_API_KEY
from config import NEWS_API_BASE_URL


def fetch_news(query, days=7):
    """
    Fetch news articles related to the given query using the NewsAPI.
    :param str query: The cryptocurrency or stock to analyze.
    :param int days: Number of past days to fetch news for. Default to 7
    :return list : A list of news headlines and descriptions.
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    url = (
        f"{NEWS_API_BASE_URL}/everything?q={query}&from={start_date.date()}"
        f"&to={end_date.date()}&sortBy=popularity&apiKey={NEWS_API_KEY}"
    )
    try:
        response = requests.get(url)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return [article["title"] + " " + article["description"] for article in articles
                    if article["title"] and article["description"]]
        else:
            print("Error fetching news:", response.json())
            return []
    except Exception as e:
        print("Exception while fetching news: " + e.__str__())
        pass
