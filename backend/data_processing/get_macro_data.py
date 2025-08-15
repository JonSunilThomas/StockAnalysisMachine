import pandas as pd
from fredapi import Fred
from pathlib import Path
import sys

# This adds the project root to the Python path, allowing us to import the settings
sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.config.settings import FRED_API_KEY, RAW_DATA_DIR

def fetch_fred_data(api_key: str, series_ids: dict, output_path: Path):
    """
    Fetches specified macroeconomic series from FRED and saves them to a CSV file.

    Args:
        api_key (str): Your FRED API key.
        series_ids (dict): Maps series IDs to desired column names.
        output_path (Path): The path to save the output CSV file.
    """
    try:
        fred = Fred(api_key=api_key)
        data_frames = []
        for series_id, name in series_ids.items():
            # Fetch each series and give it a clear name
            series_data = fred.get_series(series_id).rename(name)
            data_frames.append(series_data)

        # Combine all data into a single DataFrame and forward-fill missing values
        macro_data = pd.concat(data_frames, axis=1).ffill().reset_index()
        macro_data.rename(columns={'index': 'date'}, inplace=True)

        # Create the directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)
        macro_data.to_csv(output_path, index=False)
        print(f"✅ Successfully fetched and saved macro data to {output_path}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == '__main__':
    # Define the economic series you want to fetch.
    # Examples: 10-Year Treasury Yield, Consumer Price Index, GDP.
    series_to_fetch = {
        'DGS10': 'treasury_yield_10y',
        'CPIAUCSL': 'cpi',
        'GDP': 'gdp'
    }

    # Define where the output file will be saved
    output_file = RAW_DATA_DIR / "macro_data.csv"

    fetch_fred_data(api_key=FRED_API_KEY, series_ids=series_to_fetch, output_path=output_file)