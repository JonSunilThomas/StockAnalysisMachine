# backend/feature_engineering/build_technical_features.py
import pandas as pd
import pandas_ta as ta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

def build_technical_features(ticker: str):
    print("Building technical features...")
    raw_path = RAW_DATA_DIR / f"price_{ticker}.csv"
    df = pd.read_csv(raw_path, parse_dates=['date'])
    
    df.ta.rsi(length=14, append=True)
    df.ta.macd(fast=12, slow=26, signal=9, append=True)
    
    output_path = PROCESSED_DATA_DIR / f"technical_features_{ticker}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print("✅ Technical features built.")

if __name__ == '__main__':
    build_technical_features("AAPL")