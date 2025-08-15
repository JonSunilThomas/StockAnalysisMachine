# backend/feature_engineering/build_fundamental_features.py
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

def build_fundamental_features(ticker: str):
    print("Building fundamental features...")
    raw_path = RAW_DATA_DIR / f"fundamentals_{ticker}.csv"
    df = pd.read_csv(raw_path, parse_dates=['fiscalDateEnding'])
    
    df['roe'] = df['netIncome'] / df['totalShareholderEquity']
    df['roa'] = df['netIncome'] / df['totalAssets']
    
    output_path = PROCESSED_DATA_DIR / f"fundamental_features_{ticker}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print("✅ Fundamental features built.")

if __name__ == '__main__':
    build_fundamental_features("AAPL")