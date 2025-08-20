# backend/ml_models/train_model.py
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import PROCESSED_DATA_DIR

def train_model(ticker: str):
    """
    Trains a balanced model and saves it, then generates and saves historical predictions.
    """
    print(f"Training model for {ticker}...")
    master_df = pd.read_csv(PROCESSED_DATA_DIR / f"master_dataset_{ticker}.csv", parse_dates=['date'])
    
    # In all three files: train_model.py, predict.py, and explain.py

# --- USE THIS FINAL, COMPLETE FEATURE LIST ---
    features = [
        'RSI_14', 'MACD_12_26_9', 
        'roe', 'roa', 'avg_sentiment',
        'treasury_yield_10y', 'cpi' # <-- Add the new macro features
    ]
    master_df = master_df.dropna(subset=features)

    X = master_df[features]
    y = master_df['target']
    dates = master_df['date']
    
    X_train, X_test, y_train, y_test, dates_train, dates_test = train_test_split(
        X, y, dates, test_size=0.2, random_state=42, shuffle=False
    )
    
    # --- FIX: Handle imbalanced data by calculating scale_pos_weight ---
    # This tells the model how much more to weigh the minority class (usually '1's or 'Buy' signals)
    try:
        scale_pos_weight = np.sum(y_train == 0) / np.sum(y_train == 1)
    except ZeroDivisionError:
        scale_pos_weight = 1 # Default to 1 if there are no 'Buy' signals in the training set
        
    print(f"Class balance weight (scale_pos_weight): {scale_pos_weight:.2f}")

    # Pass the weight to the model
    model = xgb.XGBClassifier(
        objective='binary:logistic',
        eval_metric='logloss',
        use_label_encoder=False,
        scale_pos_weight=scale_pos_weight
    )
    # ---
    
    model.fit(X_train, y_train)
    
    model_path = Path(__file__).parent.parent / "saved_models/meta_model_v1.json"
    model_path.parent.mkdir(exist_ok=True)
    model.save_model(model_path)
    
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model trained with accuracy: {acc:.2%}")
    print(f"Model saved to {model_path}")

    historical_predictions_df = pd.DataFrame({'date': dates_test, 'prediction': y_pred})
    hist_pred_path = PROCESSED_DATA_DIR / f"historical_predictions_{ticker}.csv"
    historical_predictions_df.to_csv(hist_pred_path, index=False)
    print(f"✅ Historical predictions saved to {hist_pred_path}")

if __name__ == '__main__':
    from backend.feature_engineering.unify_features import unify_features
    unify_features("AAPL")
    train_model("AAPL")