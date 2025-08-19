# backend/main_handler.py
import pandas as pd
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import all necessary functions for the on-demand pipeline
from backend.config.settings import PROCESSED_DATA_DIR, RAW_DATA_DIR, NEWS_API_KEY
from backend.data_processing.get_fundamental_data import get_fundamental_data
from backend.data_processing.get_price_data import get_price_data
from backend.data_processing.get_news_data import fetch_news_articles
from backend.feature_engineering.build_fundamental_features import build_fundamental_features
from backend.feature_engineering.build_technical_features import build_technical_features
from backend.feature_engineering.build_sentiment_features import analyze_sentiment
from backend.feature_engineering.unify_features import unify_features
from backend.ml_models.predict import make_prediction
from backend.ml_models.explain import explain_prediction

def generate_data_for_ticker(ticker: str):
    """
    Runs the full data pipeline for a single ticker on-demand.
    """
    print(f"--- On-demand data generation started for {ticker} ---")
    # Phase 1: Data Collection
    get_fundamental_data(ticker, RAW_DATA_DIR / f"fundamentals_{ticker}.csv")
    get_price_data(ticker, RAW_DATA_DIR / f"price_{ticker}.csv")
    fetch_news_articles(NEWS_API_KEY, ticker, RAW_DATA_DIR / f"news_{ticker}.csv")
    
    # Phase 2: Feature Engineering
    build_fundamental_features(ticker)
    build_technical_features(ticker)
    analyze_sentiment(
        RAW_DATA_DIR / f"news_{ticker}.csv", 
        PROCESSED_DATA_DIR / f"sentiment_features_{ticker}.csv"
    )
    
    # Phase 3: Unification
    unify_features(ticker)
    print(f"--- On-demand data generation finished for {ticker} ---")

def get_latest_features(ticker: str):
    """
    Loads the master dataset for a ticker. If it doesn't exist, it generates it.
    """
    master_dataset_path = PROCESSED_DATA_DIR / f"master_dataset_{ticker}.csv"
    
    # If the file doesn't exist, run the on-demand generation pipeline
    if not master_dataset_path.exists():
        print(f"Master dataset for {ticker} not found. Generating on-demand...")
        generate_data_for_ticker(ticker)

    if not master_dataset_path.exists():
         raise FileNotFoundError(f"Master dataset for {ticker} could not be created.")

    df = pd.read_csv(master_dataset_path, parse_dates=['date'])
    df.sort_values(by='date', inplace=True)
    return df.tail(1)

def get_prediction_for_ticker(ticker: str):
    """
    Orchestrates the prediction pipeline for a single ticker.
    """
    print(f"--- Starting analysis for {ticker} ---")
    
    try:
        unified_data = get_latest_features(ticker)
        if unified_data.empty:
            raise ValueError("Failed to retrieve latest features.")

        prediction_output = make_prediction(unified_data)
        explanation_df = explain_prediction(unified_data)
        
        final_output = {
            "prediction": prediction_output['prediction'],
            "confidence": prediction_output['confidence'],
            "explanation": explanation_df,
            "latest_features": unified_data
        }
        print("--- Analysis complete ---")
        return final_output
        
    except Exception as e:
        print(f"❌ An error occurred in the handler: {e}")
        return None