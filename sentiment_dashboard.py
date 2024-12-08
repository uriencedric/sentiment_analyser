from datetime import datetime

import streamlit as st
from matplotlib import pyplot as plt

# Import functions for data fetching and analysis
from lib.analysis.sentiment import get_sentiment_score  # Replace `your_script` with the filename

# Dashboard Title
st.title("Market Sentiment & Price Trend Analysis")
st.markdown("Analyze cryptocurrency and stock sentiment along with price trends.")

# User Inputs
market_type = st.selectbox("Select Market Type", options=["Crypto", "Legacy (Stocks)"])

if market_type == "Crypto":
    query = st.text_input("Enter Cryptocurrency Name (e.g., Bitcoin)", value="Bitcoin")
    #symbol = st.text_input("Enter Trading Pair (e.g., BTCUSDT)", value="BTCUSDT")
elif market_type == "Legacy (Stocks)":
    query = st.text_input("Enter Stock Name (e.g., Apple)", value="Apple")
    ticker = st.text_input("Enter Stock Ticker (e.g., AAPL)", value="AAPL")

if st.button("Analyze"):
    with st.spinner("Fetching data and analyzing sentiment..."):
        # Fetch sentiment and price data
        if market_type == "Crypto":
            result = get_sentiment_score(query, market_type="crypto")
        elif market_type == "Legacy (Stocks)":
            result = get_sentiment_score(query, market_type="legacy", ticker=ticker)

        # Display Results
        st.success("Analysis Complete!")
        st.subheader(f"Overall Score: {result['overall_score']} / 10")
        st.metric("Overall Sentiment Score", f"{result['overall_sentiment_score']} / 10")
        st.metric("Overall Score", f"{result['overall_score']} / 10")
        st.metric("News Sentiment", f"{result['news_score']} / 10")
        st.metric("Social Media Sentiment", f"{result['tweet_score']} / 10")
        st.metric("Articles Analyzed", f"{result['articles_analyzed']}")
        st.metric("Tweets Analyzed", f"{result['tweets_analyzed']}")

        # Display Price Trend
        st.subheader("Price Trend Analysis")
        price_trends = result["price_trends"]
        if market_type == "Crypto":
            print(price_trends)
            st.write(f"**Symbol:** {price_trends['crypto_id']}")
        else:
            st.write(f"**Ticker:** {price_trends['ticker']}")
        st.metric("Average Price Change (%)", f"{price_trends['avg_change']}%")
        st.write(f"**Trend Sentiment:** {price_trends['trend_sentiment'].capitalize()}")

        # Visualization
        st.subheader("Sentiment & Price Change Visualization")
        scores = [result["news_score"], result["tweet_score"], result["overall_sentiment_score"]]
        labels = ["News", "Social Media", "Overall Sentiment"]

        fig, ax = plt.subplots()
        ax.bar(labels, scores, color=["blue", "green", "orange"])
        ax.set_ylabel("Score")
        ax.set_title("Sentiment Analysis Scores")
        st.pyplot(fig)

        st.markdown(f"**Last Updated:** {result['last_updated']}")

# Footer
st.markdown("---")
st.markdown("Developed by uriencedric using Python and Streamlit")
