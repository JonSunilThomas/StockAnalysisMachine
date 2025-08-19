# backend/feature_engineering/build_technical_features.py
import pandas as pd
import pandas_ta as ta
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

def build_technical_features(ticker: str):
    """
    Calculates technical indicators and rolling stats from raw price data.
    """
    print(f"Building technical features for {ticker}...")
    raw_path = RAW_DATA_DIR / f"price_{ticker}.csv"
    if not raw_path.exists():
        print(f"Price data for {ticker} not found. Skipping.")
        return

    df = pd.read_csv(raw_path, parse_dates=['date'])
    
    # --- FIX: Ensure all price-related columns are numeric ---
    numeric_cols = ['open', 'high', 'low', 'close', 'volume']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    # ---

    df.set_index('date', inplace=True)
    
    # Calculate standard indicators using pandas_ta
    df.ta.rsi(length=14, append=True)
    df.ta.macd(fast=12, slow=26, signal=9, append=True)
    
    # Calculate Higher Highs / Lower Lows
    window = 252
    df['rolling_high_52wk'] = df['high'].rolling(window=window).max()
    df['rolling_low_52wk'] = df['low'].rolling(window=window).min()
    
    df.reset_index(inplace=True)
    output_path = PROCESSED_DATA_DIR / f"technical_features_{ticker}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Technical features built for {ticker}.")

if __name__ == '__main__':
    build_technical_features("AAPL")