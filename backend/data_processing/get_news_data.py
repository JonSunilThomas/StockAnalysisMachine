import pandas as pd
from newsapi import NewsApiClient
from pathlib import Path
import sys

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.config.settings import NEWS_API_KEY, RAW_DATA_DIR

def fetch_news_articles(api_key: str, query: str, output_path: Path, page_size: int = 100):
    """
    Fetches news articles for a specific query from NewsAPI and saves them to a CSV.

    Args:
        api_key (str): Your NewsAPI key.
        query (str): The search term (e.g., company name or ticker).
        output_path (Path): The path to save the output CSV file.
        page_size (int): Max number of results to return (100 is the max for developer plan).
    """
    try:
        newsapi = NewsApiClient(api_key=api_key)
        
        # Fetch the most recent and relevant articles
        all_articles = newsapi.get_everything(
            q=query,
            language='en',
            sort_by='publishedAt', # Use 'relevancy' or 'popularity' if preferred
            page_size=page_size
        )

        articles_list = []
        for article in all_articles['articles']:
            articles_list.append({
                'ticker': query,
                'published_at': article['publishedAt'],
                'title': article['title'],
                'description': article['description'],
                'source': article['source']['name']
            })

        df = pd.DataFrame(articles_list)
        # Convert publish time to a proper datetime format
        df['published_at'] = pd.to_datetime(df['published_at'])

        # Create the directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"✅ Successfully fetched {len(df)} articles for '{query}' and saved to {output_path}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    # You can change this to any company ticker or name you want to test
    target_ticker = "AAPL"

    # Define the output path for the raw news file
    output_file = RAW_DATA_DIR / f"news_{target_ticker}.csv"

    fetch_news_articles(api_key=NEWS_API_KEY, query=target_ticker, output_path=output_file)