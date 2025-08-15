# backend/data_processing/get_price_data.py
import pandas as pd
import numpy as np
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR

def get_price_data(ticker: str, output_path: Path):
    """
    Simulates fetching and saving historical price data.
    """
    print(f"Simulating price data fetch for {ticker}...")
    
    # Create a sample DataFrame of historical prices
    dates = pd.date_range(start="2023-01-01", end="2025-08-15", freq='B')
    data_size = len(dates)
    
    price_data = {
        'date': dates,
        'open': np.random.uniform(150, 200, size=data_size).cumsum(),
        'high': lambda df: df['open'] + np.random.uniform(0, 5, size=data_size),
        'low': lambda df: df['open'] - np.random.uniform(0, 5, size=data_size),
        'close': lambda df: (df['open'] + df['high'] + df['low']) / 3,
        'volume': np.random.randint(1e6, 5e6, size=data_size)
    }
    
    price_df = pd.DataFrame({'date': dates})
    price_df['open'] = np.random.uniform(150, 160, size=data_size)
    price_df['high'] = price_df['open'] + np.random.uniform(0, 5, size=data_size)
    price_df['low'] = price_df['open'] - np.random.uniform(0, 5, size=data_size)
    price_df['close'] = (price_df['open'] + price_df['high'] + price_df['low']) / 3
    price_df['volume'] = np.random.randint(1e6, 5e6, size=data_size)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    price_df.to_csv(output_path, index=False)
    print(f"✅ Mock price data for {ticker} saved to {output_path}")

if __name__ == '__main__':
    target_ticker = "AAPL"
    output_file = RAW_DATA_DIR / f"price_{target_ticker}.csv"
    get_price_data(target_ticker, output_file)