# backend/main_pipeline.py
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import all the necessary modules
from backend.data_processing.get_fundamental_data import get_fundamental_data
from backend.data_processing.get_price_data import get_price_data
from backend.data_processing.get_news_data import fetch_news_articles
from backend.feature_engineering.build_fundamental_features import build_fundamental_features
from backend.feature_engineering.build_technical_features import build_technical_features
from backend.feature_engineering.build_sentiment_features import analyze_sentiment
from backend.feature_engineering.unify_features import unify_features
from backend.ml_models.train_model import train_model
from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR
from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, NEWS_API_KEY

def run_full_pipeline(tickers: list):
    """
    Executes the entire data collection, feature engineering, and model training pipeline.

    Args:
        tickers (list): A list of stock tickers to process.
    """
    print("--- Starting Main Pipeline ---")
    
    for ticker in tickers:
        print(f"\n--- Processing Ticker: {ticker} ---")
        
        # --- Phase 1: Data Collection ---
        get_fundamental_data(ticker, RAW_DATA_DIR / f"fundamentals_{ticker}.csv")
        get_price_data(ticker, RAW_DATA_DIR / f"price_{ticker}.csv")
        fetch_news_articles(NEWS_API_KEY, ticker, RAW_DATA_DIR / f"news_{ticker}.csv")
        
        # --- Phase 2: Feature Engineering ---
        build_fundamental_features(ticker)
        build_technical_features(ticker)
        analyze_sentiment(
            RAW_DATA_DIR / f"news_{ticker}.csv", 
            PROCESSED_DATA_DIR / f"sentiment_features_{ticker}.csv"
        )
        
        # --- Phase 3: Unification ---
        unify_features(ticker)

    # --- Phase 4: Model Training ---
    # In a more advanced setup, you might combine data from all tickers.
    # For this project, we'll train the model on the first ticker in the list.
    if tickers:
        print(f"\n--- Training Model on {tickers[0]} data ---")
        train_model(tickers[0])
    
    print("\n--- Main Pipeline Finished Successfully ---")

if __name__ == '__main__':
    # Define the list of stocks you want to keep updated.
    stocks_to_track = ["AAPL", "GOOGL", "MSFT"] 
    run_full_pipeline(stocks_to_track)