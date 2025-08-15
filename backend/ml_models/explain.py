# backend/ml_models/explain.py
import pandas as pd
import xgboost as xgb
import shap
from pathlib import Path

def explain_prediction(processed_data: pd.DataFrame):
    print("DEBUG: `explain_prediction` (REAL) function was called.")
    model_path = Path(__file__).parent.parent / "saved_models/meta_model_v1.json"
    model = xgb.XGBClassifier()
    model.load_model(model_path)
    
    # --- FIX: Define and select only the feature columns ---
    features = ['RSI_14', 'MACD_12_26_9', 'roe', 'roa', 'avg_sentiment']
    data_for_explanation = processed_data[features]
    # ---
    
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(data_for_explanation)
    
    feature_names = data_for_explanation.columns
    contributions = shap_values[0]
    
    explanation_df = pd.DataFrame({
        'feature': feature_names,
        'contribution': contributions
    }).sort_values(by='contribution', ascending=False)
    
    return explanation_df