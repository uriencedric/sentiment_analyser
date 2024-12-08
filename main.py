from lib.analysis.sentiment import get_sentiment_score


def process_tweet_input():
    """
    Fetch user input if script must include tweets
    :return: bool
    """
    _bool = False
    incl_tweets_input = input("Include tweets analysis (yes/no): ").lower()
    if not incl_tweets_input:
        print("No value provided. Will default to false")
        return False
    if incl_tweets_input.lower() not in ["yes", "no", "y", "n"]:
        print("Supported values (ignoring case): yes|no, y|n")
        exit(1)
    if incl_tweets_input.lower() == "yes" or incl_tweets_input.lower() == "y":
        _bool = True

    return _bool


# _usage
if __name__ == "__main__":
    include_tweets = process_tweet_input()
    market_type = input("Enter market type (crypto/legacy): ").lower()
    if market_type == "crypto":
        query = input("Enter the cryptocurrency (e.g., Bitcoin): ")
        if not query:
            print("Invalid instrument type or symbol. Please enter a valid cryptocurrency (e.g., Bitcoin)")
            exit(1)
        result = get_sentiment_score(query, market_type="crypto", include_tweets=include_tweets)

    elif market_type == "legacy":
        query = input("Enter the stock name (e.g., Apple): ")
        ticker = input("Enter the stock ticker (e.g., AAPL): ")
        if not query or not ticker:
            print("Invalid instrument type or ticker . Please enter a valid stock name (e.g., Apple)"
                  " or a valid stock ticker (e.g., AAPL).")
            exit(1)
        result = get_sentiment_score(query, market_type="legacy", ticker=ticker, include_tweets=include_tweets)

    else:
        print("Invalid market type. Please choose 'crypto' or 'legacy'.")
        exit(1)

    print("\n=== Sentiment Analysis Result ===")
    print(f"  Market Type: {result['market_type']}")
    print(f"  Asset: {result['query']}")
    print(f"  Overall Score: {result['overall_score']} / 10")
    print(f"  News Score: {result['news_score']} / 10")
    print(f"  Tweet Score: {result['tweet_score']} / 10")

    if result['market_type'] == "crypto" and result['price_trends']:
        print("\nPrice Trends:")
        print(f"  Start Price: ${result['price_trends']['start_price']}")
        print(f"  End Price: ${result['price_trends']['end_price']}")
        print(f"  Average Price: ${result['price_trends']['avg_price']}")
        print(f"  Price Change: {result['price_trends']['avg_change']}% ({result['price_trends']['trend_sentiment']})")

    elif result['market_type'] == "legacy" and result['price_trends']:
        print("\nPrice Trends:")
        print(f"  Ticker: {result['price_trends']['ticker']}")
        print(f"  Average change: ${result['price_trends']['avg_change']}")
        print(f"  Trend sentiment: {result['price_trends']['trend_sentiment']}")
    else:
        print("\nPrice Trends: not available")

    print(f"\nArticles Analyzed: {result['articles_analyzed']}")
    print(f"  Tweets Analyzed: {result['tweets_analyzed']}")
    print(f"\nNotes: ")
    print(
        f"  To visualize in your browser, run the following command in your terminal : streamlit run "
        f"sentiment_dashboard.py")
    print("\n=== Sentiment Analysis Result end ===")
