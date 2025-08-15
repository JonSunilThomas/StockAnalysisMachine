# backend/data_processing/get_fundamental_data.py
import pandas as pd
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR

def get_fundamental_data(ticker: str, output_path: Path):
    """
    Simulates fetching and saving fundamental data (e.g., from Alpha Vantage).
    In a real scenario, this would make an API call. Here, we create mock data.
    """
    print(f"Simulating fundamental data fetch for {ticker}...")
    
    # Create a sample DataFrame that mimics a real income statement/balance sheet
    dates = pd.to_datetime(['2024-06-30', '2024-03-31', '2023-12-31', '2023-09-30', '2023-06-30'])
    data = {
        'fiscalDateEnding': dates,
        'reportedEPS': [1.5, 1.35, 1.8, 1.6, 1.4],
        'totalRevenue': np.random.randint(1e9, 2e9, size=len(dates)),
        'netIncome': np.random.randint(1e8, 5e8, size=len(dates)),
        'totalShareholderEquity': np.random.randint(5e9, 8e9, size=len(dates)),
        'totalAssets': np.random.randint(1e10, 2e10, size=len(dates)),
    }
    fundamentals_df = pd.DataFrame(data)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fundamentals_df.to_csv(output_path, index=False)
    print(f"✅ Mock fundamental data for {ticker} saved to {output_path}")

if __name__ == '__main__':
    target_ticker = "AAPL"
    output_file = RAW_DATA_DIR / f"fundamentals_{target_ticker}.csv"
    get_fundamental_data(target_ticker, output_file)