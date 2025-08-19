# backend/data_processing/get_fundamental_data.py
import pandas as pd
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR

def get_fundamental_data(ticker: str, output_path: Path):
    """
    Simulates fetching and saving more realistic fundamental data.
    """
    print(f"Simulating realistic fundamental data fetch for {ticker}...")
    
    dates = pd.to_datetime(['2024-06-30', '2024-03-31', '2023-12-31', '2023-09-30', '2023-06-30'])
    
    # Generate more realistic, non-zero financial numbers
    data = {
        'fiscalDateEnding': dates,
        'reportedEPS': np.random.uniform(1.0, 2.5, size=len(dates)).round(2),
        'totalRevenue': np.random.randint(50e9, 100e9, size=len(dates)),
        'netIncome': np.random.randint(10e9, 25e9, size=len(dates)),
        'totalShareholderEquity': np.random.randint(80e9, 120e9, size=len(dates)),
        'totalAssets': np.random.randint(200e9, 350e9, size=len(dates)),
    }
    fundamentals_df = pd.DataFrame(data)
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fundamentals_df.to_csv(output_path, index=False)
    print(f"✅ Realistic mock fundamental data for {ticker} saved to {output_path}")

if __name__ == '__main__':
    target_ticker = "AAPL"
    output_file = RAW_DATA_DIR / f"fundamentals_{target_ticker}.csv"
    get_fundamental_data(target_ticker, output_file)