from datetime import datetime
from config import SENTIMENT_ANALYZER_BLANK, SENTIMENT_ANALYZER_NEWS
from lib.utils.constants import Y_M_D_H_M_S, DEFAULT_PRICE_SCORE, SENTIMENT_WEIGHT, PRICE_WEIGHT, TWITTER_WEIGHT
from lib.analysis.price_trends import fetch_crypto_price_trend, fetch_stock_price_trend
from lib.external.news import fetch_news
from lib.utils.trend_enum import Trend
from lib.external.twitter import fetch_tweets


def analyze_sentiment(texts, pipe):
    """
    Analyze the sentiment of the given texts using a pre-trained sentiment model.
    :param list texts:
    :param callable pipe: A callable (e.g : pipe(texts, truncation=True))
    :return: A sentiment score
    :rtype: int
    """

    """
    Analyze the sentiment of the given texts using a pre-trained sentiment model.
    Args:
        texts (list): List of texts to analyze.
        pipe (func): a user defined pipeline to analyze the sentiment.
    Returns:
        float: Average sentiment score from 1 (bearish) to 10 (bullish).
    """
    if not texts:
        return 5.0  # Neutral score if no data is available

    results = pipe(texts, truncation=True)
    scores = []
    for result in results:
        if result["label"] == "POSITIVE":
            scores.append(10 * result["score"])  # Scale positive scores to 10
        elif result["label"] == "NEGATIVE":
            scores.append(1 + (9 * (1 - result["score"])))  # Scale negative scores to 1
        else:
            scores.append(5)  # Neutral
    return sum(scores) / len(scores)


def get_sentiment_score(query, market_type=None, ticker=None, include_tweets=False):
    """
    Fetch news, analyze sentiment, and return an overall sentiment score.
    :param str query:  The cryptocurrency or stock to analyze.
    :param str market_type: "crypto" for cryptocurrencies, "legacy" for stocks.
    :param str ticker: Stock ticker symbol (e.g., "AAPL") for Yahoo Finance.
    :param bool include_tweets: Bool if true will analyze tweets based on the query
    :return: Sentiment score and related information.
    :rtype: dict
    """
    print(f"Fetching news for: {query}...")

    news = fetch_news(query)

    print(f"Analyzing sentiment for {len(news)} news articles...")
    news_score = analyze_sentiment(news, SENTIMENT_ANALYZER_NEWS)

    tweet_score = 0
    tweets = []

    if include_tweets:
        print(f"Fetching tweets for: {query}...")
        tweets = fetch_tweets(query)
        print(f"Analyzing sentiment for {len(tweets)} tweets...")
        tweet_score = analyze_sentiment(tweets, SENTIMENT_ANALYZER_BLANK)

    price_trends = {}

    # Price trends
    if market_type == "crypto":
        print(f"Fetching price trends for crypto: {query}...")
        price_trends = fetch_crypto_price_trend(str(query).lower())
    elif market_type == "legacy":
        print(f"Fetching price trends for stock: {ticker}...")
        price_trends = fetch_stock_price_trend(ticker)
    else:
        price_trends = {"avg_change": 0, "trend_sentiment": Trend.NEUTRAL}

    # Combine scores

    overall_sentiment_score = (SENTIMENT_WEIGHT * news_score) + (TWITTER_WEIGHT * tweet_score)
    price_score = DEFAULT_PRICE_SCORE if price_trends["trend_sentiment"] == Trend.BULLISH else 1
    overall_score = round((SENTIMENT_WEIGHT * overall_sentiment_score) + (PRICE_WEIGHT * price_score), 2)

    return {
        "market_type": market_type,
        "query": query,
        "overall_sentiment_score": overall_sentiment_score,
        "overall_score": overall_score,
        "news_score": round(news_score, 2),
        "tweet_score": round(tweet_score, 2),
        "articles_analyzed": len(news),
        "tweets_analyzed": len(tweets),
        "price_trends": price_trends,
        "last_updated": datetime.now().strftime(Y_M_D_H_M_S)
    }
