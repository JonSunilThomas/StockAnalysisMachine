# backend/feature_engineering/unify_features.py
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import PROCESSED_DATA_DIR

def unify_features(ticker: str):
    print("Unifying all features...")
    tech_df = pd.read_csv(PROCESSED_DATA_DIR / f"technical_features_{ticker}.csv", parse_dates=['date'])
    funda_df = pd.read_csv(PROCESSED_DATA_DIR / f"fundamental_features_{ticker}.csv", parse_dates=['fiscalDateEnding'])
    senti_df = pd.read_csv(PROCESSED_DATA_DIR / f"sentiment_features_{ticker}.csv", parse_dates=['published_at'])

    # Aggregate sentiment to daily
    daily_sentiment = senti_df.groupby(senti_df['published_at'].dt.date)['sentiment_numeric'].mean().reset_index()
    daily_sentiment.rename(columns={'published_at': 'date', 'sentiment_numeric': 'avg_sentiment'}, inplace=True)
    daily_sentiment['date'] = pd.to_datetime(daily_sentiment['date'])

    # Merge data
    master_df = pd.merge(tech_df, daily_sentiment, on='date', how='left')
    master_df = pd.merge_asof(master_df.sort_values('date'), funda_df.sort_values('fiscalDateEnding'), left_on='date', right_on='fiscalDateEnding', direction='backward')
    
    # Create prediction target
    master_df['target'] = (master_df['close'].shift(-60) > master_df['close'] * 1.05).astype(int) # 5% gain in 60 trading days
    master_df.dropna(inplace=True)
    
    output_path = PROCESSED_DATA_DIR / f"master_dataset_{ticker}.csv"
    master_df.to_csv(output_path, index=False)
    print(f"✅ Master dataset created with {len(master_df)} rows.")
    return master_df

if __name__ == '__main__':
    unify_features("AAPL")