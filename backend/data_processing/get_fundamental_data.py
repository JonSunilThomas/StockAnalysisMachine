# backend/data_processing/get_fundamental_data.py
import pandas as pd
from pathlib import Path
import sys
import yfinance as yf

# add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import RAW_DATA_DIR

def get_fundamental_data(ticker: str, output_path: Path):
    """
    Fetches and saves real fundamental financial data for a given ticker using yfinance.
    """
    print(f"📡 Fetching real fundamental data for {ticker}...")

    try:
        stock = yf.Ticker(ticker)
        
        # Fetch quarterly statements and transpose them
        income_stmt = stock.quarterly_financials.T
        balance_sheet = stock.quarterly_balance_sheet.T

        # --- FIX: Standardize column names ---
        # yfinance columns can have spaces and different cases. We need to clean them.
        income_stmt.columns = income_stmt.columns.str.replace(' ', '')
        balance_sheet.columns = balance_sheet.columns.str.replace(' ', '')
        
        # Combine the two statements
        fundamentals_df = pd.concat([income_stmt, balance_sheet], axis=1)
        
        # Select and rename the columns we need to a consistent format
        fundamentals_df = fundamentals_df.rename(columns={
            "TotalRevenue": "totalRevenue",
            "NetIncome": "netIncome",
            "TotalAssets": "totalAssets",
            "TotalStockholderEquity": "totalShareholderEquity",
            "ReportedEPS": "reportedEPS"
        })
        
        # Add the date column
        fundamentals_df["fiscalDateEnding"] = fundamentals_df.index
        
        # Keep only the columns our project uses
        required_cols = [
            'fiscalDateEnding', 'totalRevenue', 'netIncome', 
            'totalAssets', 'totalShareholderEquity', 'reportedEPS'
        ]
        
        # Filter for required columns, handling any that might be missing
        final_df = fundamentals_df[[col for col in required_cols if col in fundamentals_df.columns]]

        final_df.reset_index(drop=True, inplace=True)

        # Save to CSV
        output_path.parent.mkdir(parents=True, exist_ok=True)
        final_df.to_csv(output_path, index=False)

        print(f"✅ Saved real fundamentals for {ticker} to {output_path}")

    except Exception as e:
        print(f"❌ Could not fetch fundamental data for {ticker}. Error: {e}")


if __name__ == "__main__":
    target_ticker = "AAPL"
    output_file = RAW_DATA_DIR / f"fundamentals_{target_ticker}.csv"
    get_fundamental_data(target_ticker, output_file)