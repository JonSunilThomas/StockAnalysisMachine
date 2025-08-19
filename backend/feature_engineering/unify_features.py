# backend/feature_engineering/unify_features.py
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import PROCESSED_DATA_DIR

def unify_features(ticker: str):
    """
    Combines all feature sets into a single master dataset with robust handling of missing data.
    """
    print("Unifying all features...")
    
    # --- Load Data ---
    tech_df = pd.read_csv(PROCESSED_DATA_DIR / f"technical_features_{ticker}.csv", parse_dates=['date'])
    funda_df = pd.read_csv(PROCESSED_DATA_DIR / f"fundamental_features_{ticker}.csv", parse_dates=['fiscalDateEnding'])
    senti_df = pd.read_csv(PROCESSED_DATA_DIR / f"sentiment_features_{ticker}.csv", parse_dates=['published_at'])

    # --- Process and Merge Sentiment Data ---
    senti_df['date'] = pd.to_datetime(senti_df['published_at'].dt.date)
    daily_sentiment = senti_df.groupby('date')['sentiment_numeric'].mean().rename('avg_sentiment')
    
    master_df = pd.merge(tech_df, daily_sentiment, on='date', how='left')
    master_df['avg_sentiment'].fillna(0, inplace=True)
    master_df.dropna(subset=['date'], inplace=True)
    
    # --- Process and Merge Fundamental Data ---
    master_df = pd.merge_asof(
        master_df.sort_values('date'), 
        funda_df.sort_values('fiscalDateEnding'), 
        left_on='date', 
        right_on='fiscalDateEnding', 
        direction='backward'
    )
    
    funda_cols = ['reportedEPS', 'totalRevenue', 'netIncome', 'totalShareholderEquity', 'totalAssets', 'roe', 'roa']
    master_df[funda_cols] = master_df[funda_cols].ffill()

    # --- Create Prediction Target ---
    future_price_lookahead = 60
    gain_threshold = 1.05
    master_df['future_price'] = master_df['close'].shift(-future_price_lookahead)
    master_df['target'] = (master_df['future_price'] > master_df['close'] * gain_threshold).astype(int)
    
    # --- Final Cleanup ---
    # --- FIX: Ensure all expected columns exist before dropping NA ---
    # The model expects MACDh and MACDs from the technical features calculation
    expected_features = ['RSI_14', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9', 'roe', 'roa', 'avg_sentiment']
    for col in expected_features:
        if col not in master_df.columns:
            # If a column is missing (e.g., from pandas_ta), add it with a default value
            master_df[col] = 0 
            
    master_df.dropna(subset=expected_features + ['target'], inplace=True)

    output_path = PROCESSED_DATA_DIR / f"master_dataset_{ticker}.csv"
    master_df.to_csv(output_path, index=False)
    print(f"✅ Master dataset created with {len(master_df)} rows.")
    return master_df

if __name__ == '__main__':
    unify_features("AAPL")