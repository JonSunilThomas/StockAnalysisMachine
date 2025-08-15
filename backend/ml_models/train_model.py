# backend/ml_models/train_model.py
import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.config.settings import PROCESSED_DATA_DIR

def train_model(ticker: str):
    print("Training model...")
    master_df = pd.read_csv(PROCESSED_DATA_DIR / f"master_dataset_{ticker}.csv")
    
    features = ['RSI_14', 'MACD_12_26_9', 'roe', 'roa', 'avg_sentiment']
    X = master_df[features]
    y = master_df['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = xgb.XGBClassifier(objective='binary:logistic', eval_metric='logloss', use_label_encoder=False)
    model.fit(X_train, y_train)
    
    # Save the model
    model_path = Path(__file__).parent.parent / "saved_models/meta_model_v1.json"
    model_path.parent.mkdir(exist_ok=True)
    model.save_model(model_path)
    
    # Evaluate
    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"✅ Model trained with accuracy: {acc:.2%}")
    print(f"Model saved to {model_path}")
    return model

if __name__ == '__main__':
    # First, run all previous steps to generate data
    from backend.feature_engineering.unify_features import unify_features
    unify_features("AAPL")
    
    # Then train the model
    train_model("AAPL")