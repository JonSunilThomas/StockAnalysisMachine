# backend/feature_engineering/unify_features.py
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import PROCESSED_DATA_DIR, RAW_DATA_DIR

def unify_features(ticker: str):
    """
    Combines all feature sets (including macro) into a single master dataset.
    """
    print("Unifying all features...")
    
    # --- Load Data ---
    tech_df = pd.read_csv(PROCESSED_DATA_DIR / f"technical_features_{ticker}.csv", parse_dates=['date'])
    funda_df = pd.read_csv(PROCESSED_DATA_DIR / f"fundamental_features_{ticker}.csv", parse_dates=['fiscalDateEnding'])
    senti_df = pd.read_csv(PROCESSED_DATA_DIR / f"sentiment_features_{ticker}.csv", parse_dates=['published_at'])
    macro_df = pd.read_csv(RAW_DATA_DIR / "macro_data.csv", parse_dates=['date'])

    # --- Process and Merge ---
    senti_df['date'] = pd.to_datetime(senti_df['published_at'].dt.date)
    daily_sentiment = senti_df.groupby('date')['sentiment_numeric'].mean().rename('avg_sentiment')
    
    master_df = pd.merge(tech_df, daily_sentiment, on='date', how='left')
    master_df['avg_sentiment'] = master_df['avg_sentiment'].fillna(0)
    master_df.dropna(subset=['date'], inplace=True)
    
    master_df = pd.merge_asof(
        master_df.sort_values('date'),
        macro_df.sort_values('date'),
        on='date',
        direction='backward'
    )
    
    master_df = pd.merge_asof(
        master_df.sort_values('date'), 
        funda_df.sort_values('fiscalDateEnding'), 
        left_on='date', 
        right_on='fiscalDateEnding', 
        direction='backward'
    )
    
    # --- FIX: Only forward-fill the fundamental columns that actually exist ---
    all_funda_cols = ['reportedEPS', 'totalRevenue', 'netIncome', 'totalShareholderEquity', 'totalAssets', 'roe', 'roa']
    existing_funda_cols = [col for col in all_funda_cols if col in master_df.columns]
    master_df[existing_funda_cols] = master_df[existing_funda_cols].ffill()
    # ---

    # --- Create Prediction Target ---
    master_df['target'] = (master_df['close'].shift(-60) > master_df['close'] * 1.05).astype(int)
    
    # --- Final Cleanup ---
    master_df.dropna(inplace=True)

    output_path = PROCESSED_DATA_DIR / f"master_dataset_{ticker}.csv"
    master_df.to_csv(output_path, index=False)
    print(f"✅ Master dataset created with {len(master_df)} rows, now including macro data.")
    return master_df

if __name__ == '__main__':
    unify_features("AAPL")