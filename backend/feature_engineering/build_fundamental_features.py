# backend/feature_engineering/build_fundamental_features.py
import pandas as pd
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

def build_fundamental_features(ticker: str):
    """
    Calculates financial ratios from raw fundamental data with error handling.
    """
    print("Building fundamental features...")
    raw_path = RAW_DATA_DIR / f"fundamentals_{ticker}.csv"
    if not raw_path.exists():
        print(f"Fundamental data for {ticker} not found. Skipping.")
        return

    df = pd.read_csv(raw_path, parse_dates=['fiscalDateEnding'])

    # --- FIX: Check for columns before doing calculations ---
    # Calculate Return on Equity (ROE)
    if 'netIncome' in df.columns and 'totalShareholderEquity' in df.columns:
        # Use np.where to avoid division by zero
        df['roe'] = np.where(df['totalShareholderEquity'] != 0, df['netIncome'] / df['totalShareholderEquity'], 0)
    else:
        df['roe'] = 0 # Default to 0 if columns are missing

    # Calculate Return on Assets (ROA)
    if 'netIncome' in df.columns and 'totalAssets' in df.columns:
        df['roa'] = np.where(df['totalAssets'] != 0, df['netIncome'] / df['totalAssets'], 0)
    else:
        df['roa'] = 0 # Default to 0 if columns are missing
    # ---

    output_path = PROCESSED_DATA_DIR / f"fundamental_features_{ticker}.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print("✅ Fundamental features built.")

if __name__ == '__main__':
    build_fundamental_features("AAPL")