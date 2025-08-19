# backend/download_model.py
from transformers import pipeline

def download_and_cache_model():
    """
    Initializes the FinBERT pipeline, which triggers a one-time
    download of the model to your local cache.
    """
    print("--- Starting FinBERT model download (this may take a few minutes)... ---")
    try:
        pipeline("sentiment-analysis", model="ProsusAI/finbert")
        print("✅ Model downloaded and cached successfully!")
    except Exception as e:
        print(f"❌ An error occurred during download: {e}")

if __name__ == '__main__':
    download_and_cache_model()