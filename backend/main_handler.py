# backend/main_handler.py
import pandas as pd
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from backend.ml_models.predict import make_prediction
from backend.ml_models.explain import explain_prediction

# --- IMPORTANT ---
# This handler needs to generate the same features as the training script.
# This is a simplified version for demonstration.
def get_latest_features(ticker: str):
    print("Generating latest features for prediction...")
    # In a real scenario, this would fetch live data and calculate features.
    # For this simulation, we'll just take the last row from our master dataset.
    from backend.config.settings import PROCESSED_DATA_DIR
    df = pd.read_csv(PROCESSED_DATA_DIR / f"master_dataset_{ticker}.csv")
    return df.tail(1)

def get_prediction_for_ticker(ticker: str):
    print(f"--- Starting REAL analysis for {ticker} ---")
    
    unified_data = get_latest_features(ticker)
    
    prediction_result = make_prediction(unified_data)
    explanation_df = explain_prediction(unified_data)
    
    final_output = {
        "prediction": prediction_result['prediction'],
        "confidence": prediction_result['confidence'],
        "explanation": explanation_df
    }
    return final_output