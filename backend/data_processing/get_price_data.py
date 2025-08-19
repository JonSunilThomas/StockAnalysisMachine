# backend/data_processing/get_price_data.py
import pandas as pd
import yfinance as yf
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR

def get_price_data(ticker: str, output_path: Path, start_date="2020-01-01"):
    """
    Fetches real historical price data from Yahoo Finance and saves it to a CSV.
    
    Args:
        ticker (str): The stock ticker to fetch.
        output_path (Path): The path to save the output CSV file.
        start_date (str): The start date for the historical data in YYYY-MM-DD format.
    """
    print(f"Fetching real historical price data for {ticker} from Yahoo Finance...")
    
    try:
        # Download the data
        price_df = yf.download(ticker, start=start_date, auto_adjust=True)
        
        if price_df.empty:
            print(f"❌ No data found for ticker {ticker}. It may be delisted or invalid.")
            return

        # --- IMPORTANT: Standardize column names ---
        # yfinance returns columns like 'Open', 'High'. We need lowercase.
        price_df.reset_index(inplace=True)
        price_df.rename(columns={
            'Date': 'date',
            'Open': 'open',
            'High': 'high',
            'Low': 'low',
            'Close': 'close',
            'Volume': 'volume'
        }, inplace=True)
        # ---
        
        output_path.parent.mkdir(parents=True, exist_ok=True)
        price_df.to_csv(output_path, index=False)
        print(f"✅ Real historical price data for {ticker} saved to {output_path}")

    except Exception as e:
        print(f"❌ An error occurred while fetching price data for {ticker}: {e}")


if __name__ == '__main__':
    target_ticker = "AAPL"
    output_file = RAW_DATA_DIR / f"price_{target_ticker}.csv"
    get_price_data(target_ticker, output_file)