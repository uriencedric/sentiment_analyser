import yfinance as yf

# Binance API credentials (replace with your own or leave blank for public access)

import requests

from config import COINGECKO_BASE_URL
from lib.utils.trend_enum import Trend


def fetch_crypto_price_trend(crypto_id="bitcoin", days=7):
    """
    Fetch historical price data for a cryptocurrency from the CoinGecko API.
    :param str crypto_id: The ID of the cryptocurrency (e.g., 'bitcoin', 'ethereum').
    :param int days:  Number of past days to fetch price data for.
    :return: Price trend data, including percentage change and average price.
    :rtype: dict
    """
    try:
        # Fetch price data from CoinGecko
        url = f"{COINGECKO_BASE_URL}/market_chart"
        params = {"vs_currency": "usd", "days": days}
        response = requests.get(url, params=params)
        data = response.json()

        if "prices" in data:
            # Extract closing prices
            prices = [price[1] for price in data["prices"]]  # [timestamp, price]
            start_price = prices[0]
            end_price = prices[-1]
            avg_price = sum(prices) / len(prices)
            price_change = ((end_price - start_price) / start_price) * 100
            return {
                "crypto_id": crypto_id,
                "start_price": round(start_price, 2),
                "end_price": round(end_price, 2),
                "avg_price": round(avg_price, 2),
                "avg_change": round(price_change, 2),
                "trend_sentiment": ("%s" % Trend.BULLISH) if price_change > 0 else ("%s" % Trend.BEARISH),
            }

        else:
            print(f"Error fetching price data: {data}")
            return None
    except Exception as e:
        print(f"Error fetching price trends: {e}")
        return None


def fetch_stock_price_trend(ticker, lookback=5):
    """
    Fetch recent price trends for a stock from Yahoo Finance.
    :param str ticker: Stock ticker symbol (e.g., "AAPL").
    :param int lookback: Number of past days to fetch.
    :return: Price trend analysis with average change and sentiment.
    :rtype: dict
    """

    stock = yf.Ticker(ticker)
    hist = stock.history(period=f"{lookback}d")

    if hist.empty:
        return {"ticker": ticker, "avg_change": 0, "trend_sentiment": ("%s" % Trend.NEUTRAL)}

    changes = ((hist["Close"] - hist["Open"]) / hist["Open"] * 100).tolist()
    avg_change = sum(changes) / len(changes)
    trend_sentiment = Trend.BULLISH if avg_change > 0 else Trend.BEARISH
    return {
        "ticker": ticker,
        "avg_change": round(avg_change, 2),
        "trend_sentiment": trend_sentiment,
    }
