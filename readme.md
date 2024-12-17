# README

This script performs sentiment analysis for assets in cryptocurrency and legacy markets (e.g., stocks). It uses a proprietary library to fetch and calculate sentiment scores based on news articles and, optionally, tweets.

## Prerequisites

1. **Python 3.7 or higher**
   - Ensure you have Python installed on your system.

2. **Dependencies**
   - Install the necessary libraries listed in your project or environment setup. Example:
     ```bash
     pip install -r requirements.txt
     ```

3. **Proprietary Library**
   - The script uses the proprietary library `lib.analysis.sentiment`. Ensure you have the proper access and licensing to use this library in your environment.

## Features

- Analyzes sentiment for cryptocurrency or legacy market assets.
- Optionally includes tweet sentiment analysis.
- Outputs sentiment scores for:
  - News articles
  - Tweets (if enabled)
  - Overall sentiment
- Provides price trend analysis for selected assets.


### 1. **High-Level Architecture**
The system can be broken down into these components:
- **Data Collection**: Scrapes the internet for relevant financial news, social media posts, and forum discussions.
- **Sentiment Analysis**: Analyzes the sentiment of the collected text using natural language processing (NLP).
- **Scoring Mechanism**: Aggregates sentiment results into a bullish/bearish score.
- **Output**: Returns a score from 1 (most bearish) to 10 (most bullish) along with key supporting details.


### 2. **Technical Components**

#### A. **Data Collection**
- **APIs for Financial Data**:
    - Use APIs like Alpha Vantage, Binance, or Yahoo Finance for historical price and market trend data.
- **Web Scraping**:
    - Scrape news websites (e.g., Bloomberg, Reuters) for articles.
    - Monitor forums like Reddit (e.g., r/cryptocurrency) and platforms like Twitter/X.
    - Tools: Python libraries such as `BeautifulSoup`, `Scrapy`, or `Tweepy`.
- **Aggregation**:
    - Combine headlines, social media comments, and other relevant data into a single dataset.

#### B. **Sentiment Analysis**
- **Pretrained Models**:
    - Use models like OpenAI GPT for text classification.
    - Other tools: Hugging Face's Transformers library, pre-trained models like BERT or FinBERT (finance-specific sentiment model).
- **Custom Training**:
    - Fine-tune a model on finance-specific data (e.g., labeled news as bullish, bearish, or neutral).
- **Output Categories**:
    - Positive, Neutral, Negative.

#### C. **Market Sentiment Scoring**
- Create a weighted scoring system:
    - Assign weights to different sources (e.g., news may be weighted higher than social media chatter).
    - Combine sentiment scores into an overall score normalized to 1-10.
- Example:
  ```python
  overall_score = (0.5 * news_score) + (0.3 * social_media_score) + (0.2 * market_data_trend)
  ```
- Ensure the system accounts for volume (e.g., 100 positive tweets carry more weight than 10).

#### D. **Broad Market Analysis**
- Use sentiment scores to adjust based on:
    - Macro trends (e.g., S&P 500 movement).
    - Sector-specific events (e.g., tech rallies, Bitcoin halving).

#### E. **User Interface**
Run the Streamlit app using the following command:

```bash
  streamlit run sentiment_dashboard.py
  ```

This will start a local server, and you can access the app in your browser at http://localhost:8501.
- This dashboard will include :
    - The score (1-10).
    - Key positive/negative news snippets.
    - Charts of sentiment over time.

---




## How to Run the Script

1. **Start the Script**
   Run the script in your terminal:
   ```bash
   python script.py
   ```

2. **Input Parameters**
   - **Include Tweet Analysis**: You will be prompted to include tweets in the analysis. Enter `yes` or `no`.
   - **Market Type**: Choose between `crypto` or `legacy`.
     - For `crypto`, specify the cryptocurrency name (e.g., Bitcoin).
     - For `legacy`, specify both the stock name (e.g., Apple) and its ticker (e.g., AAPL).

3. **View Results**
   - Sentiment scores and price trends (if available) will be displayed in the terminal.

## Script Logic

1. **Tweet Analysis Toggle**
   - The script begins by asking if you want to include tweet sentiment analysis.
   - Input options:
     - `yes` or `y`: Includes tweets in the analysis.
     - `no` or `n`: Excludes tweets.

2. **Market Type Selection**
   - You must specify the type of market for analysis:
     - `crypto`: Analyze cryptocurrency sentiment.
     - `legacy`: Analyze stock sentiment.
   - Prompts for further details based on the chosen market type:
     - Cryptocurrency: Enter the name of the cryptocurrency (e.g., Bitcoin).
     - Legacy Market: Enter the stock name and ticker (e.g., Apple, AAPL).

3. **Sentiment Analysis Results**
   - Displays:
     - Market Type
     - Asset Name
     - Overall Sentiment Score (out of 10)
     - News Sentiment Score
     - Tweet Sentiment Score (if included)
     - Price Trends (if available): Includes start price, end price, average price, and trend sentiment.
   - Provides a summary of the number of articles and tweets analyzed.

4. **Visualization Note**
   - For visual representation, run:
     ```bash
     streamlit run sentiment_dashboard.py
     ```

## Example Output

```
=== Sentiment Analysis Result ===
  Market Type: crypto
  Asset: Bitcoin
  Overall Score: 8 / 10
  News Score: 7.5 / 10
  Tweet Score: 8.5 / 10

Price Trends:
  Start Price: $42,000
  End Price: $44,000
  Average Price: $43,000
  Price Change: 4.76% (Positive)

Articles Analyzed: 25
Tweets Analyzed: 150

Notes:
  To visualize in your browser, run the following command in your terminal: streamlit run sentiment_dashboard.py
=== Sentiment Analysis Result end ===
```

## Error Handling

- **Missing Inputs**: The script will prompt for valid inputs if any required parameter is missing or invalid.
- **Unsupported Inputs**: If an unsupported value is provided (e.g., invalid market type), the script exits with an error message.

## Limitations

1. **Proprietary Dependency**
   - The proprietary `get_sentiment_score` function is required to execute the analysis.
   - Ensure the library is properly installed and accessible.

2. **Data Availability**
   - Sentiment scores and price trends depend on the availability of news articles and tweets.

## Customization

- You can extend the script by modifying the `process_tweet_input` function to include additional input checks or defaults.
- Add new market types or analysis features by updating the conditional blocks in the main script.


- Ensure proper licensing for the proprietary library.
- Use the `streamlit` dashboard for enhanced visualization of results.

