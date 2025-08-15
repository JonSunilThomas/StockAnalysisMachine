import pandas as pd
from transformers import pipeline
from pathlib import Path
import sys
import torch

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

def analyze_sentiment(input_path: Path, output_path: Path):
    """
    Loads raw news data, applies sentiment analysis using FinBERT, and saves the results.

    Args:
        input_path (Path): Path to the raw news CSV file.
        output_path (Path): Path to save the CSV file with sentiment scores.
    """
    if not input_path.exists():
        print(f"❌ Error: Input file not found at {input_path}")
        return

    print("Loading raw news data...")
    df = pd.read_csv(input_path)

    # Ensure title column is not empty and is of string type
    df.dropna(subset=['title'], inplace=True)
    df['title'] = df['title'].astype(str)
    
    # Check if there is any data to process
    if df.empty:
        print("⚠️ No articles with titles found to analyze. Skipping sentiment analysis.")
        return

    print("Initializing FinBERT sentiment analysis pipeline...")
    # This will download the model on the first run (it's a few hundred MB).
    # device=0 will use the GPU if available, otherwise it will use the CPU.
    device = 0 if torch.cuda.is_available() else -1
    sentiment_pipeline = pipeline("sentiment-analysis", model="ProsusAI/finbert", device=device)

    print(f"Analyzing sentiment for {len(df)} articles... This may take a moment.")
    results = sentiment_pipeline(df['title'].tolist())

    # Combine sentiment results back into the DataFrame
    df['sentiment_label'] = [result['label'] for result in results]
    df['sentiment_score'] = [result['score'] for result in results]

    # Convert label to a numerical value for easier modeling
    # We multiply the score by +1 for positive, -1 for negative, and 0 for neutral.
    label_map = {'positive': 1, 'negative': -1, 'neutral': 0}
    df['sentiment_numeric'] = df['sentiment_label'].map(label_map) * df['sentiment_score']
    
    # Create the directory if it doesn't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Sentiment analysis complete. Enriched data saved to {output_path}")

if __name__ == '__main__':
    target_ticker = "AAPL" # This must match the ticker from get_news_data.py

    # Define the input and output paths using our settings
    raw_news_file = RAW_DATA_DIR / f"news_{target_ticker}.csv"
    processed_sentiment_file = PROCESSED_DATA_DIR / f"sentiment_features_{target_ticker}.csv"

    analyze_sentiment(input_path=raw_news_file, output_path=processed_sentiment_file)