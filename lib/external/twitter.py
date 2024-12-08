import tweepy
from config import TWITTER_BEARER_TOKEN


def fetch_tweets(query, count=100):
    """
    Fetch recent tweets related to the given query using Tweepy.
    :param str query:
    :param int count:
    :return: A list of corresponding tweet, based on the query
    :rtype: list
    """
    client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN, wait_on_rate_limit=True)
    tweets = client.search_recent_tweets(query=query, max_results=count, tweet_fields=["text"])
    if tweets.data:
        return [tweet.text for tweet in tweets.data]
    else:
        print(f"No tweets found for query: {query}")
        return []