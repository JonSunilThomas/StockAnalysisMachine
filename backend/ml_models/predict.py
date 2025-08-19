# backend/ml_models/predict.py
import xgboost as xgb
import pandas as pd
from pathlib import Path

def make_prediction(processed_data: pd.DataFrame):
    print("DEBUG: `make_prediction` (REAL) function was called.")
    model_path = Path(__file__).parent.parent / "saved_models/meta_model_v1.json"
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    # --- FIX: Define and select only the feature columns ---
    features = ['RSI_14', 'MACD_12_26_9', 'roe', 'roa', 'avg_sentiment']
    data_for_prediction = processed_data[features]
    # ---
    
    prediction_proba = model.predict_proba(data_for_prediction)
    
    confidence = prediction_proba[0][1]
    prediction = 'Bullish' if confidence > 0.5 else 'Bearish'
    
    # (in the make_prediction function)
# ...
    # --- USE THIS UPDATED FEATURE LIST ---
    features = ['RSI_14', 'MACD_12_26_9', 'MACDh_12_26_9', 'MACDs_12_26_9', 'roe', 'roa', 'avg_sentiment']
    data_for_prediction = processed_data[features]
# ...

    return {
        'prediction': prediction,
        'confidence': confidence,
        'model_version': 'v1.0-real'
    }