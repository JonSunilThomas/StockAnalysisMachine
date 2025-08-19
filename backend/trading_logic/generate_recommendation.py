# backend/trading_logic/generate_recommendation.py
import pandas as pd

def get_trade_recommendation(prediction_data: dict, latest_features: pd.DataFrame):
    """
    Generates a trade recommendation based on a set of rules.

    Args:
        prediction_data (dict): The output from the make_prediction function.
        latest_features (pd.DataFrame): A DataFrame row with the latest features.

    Returns:
        dict: A dictionary containing the recommendation and a disclaimer.
    """
    recommendation = {
        "action": "Hold",
        "reasoning": "The model's signal is not strong enough to warrant a trade.",
        "quantity_suggestion": "N/A",
        "disclaimer": "IMPORTANT: This is an AI-generated recommendation and not financial advice. All investment decisions should be made with the consultation of a qualified professional. Past performance is not indicative of future results."
    }

    confidence = prediction_data.get('confidence', 0)
    prediction = prediction_data.get('prediction', 'Bearish')
    
    # Rule-based logic for a "Buy" signal
    if prediction == 'Bullish' and confidence > 0.75:
        recommendation['action'] = "Buy"
        recommendation['reasoning'] = f"The model is highly confident ({confidence:.1%}) in a Bullish forecast. The underlying metrics suggest potential upward momentum."
        recommendation['quantity_suggestion'] = "Consider a small position (e.g., 1-2% of portfolio value) to start."

    # Rule-based logic for a "Sell" signal
    elif prediction == 'Bearish' and confidence > 0.75:
        recommendation['action'] = "Sell"
        recommendation['reasoning'] = f"The model is highly confident ({confidence:.1%}) in a Bearish forecast. This could indicate a potential downturn or overvaluation."
        recommendation['quantity_suggestion'] = "Consider trimming an existing position to take profits or limit downside risk."

    return recommendation

# Example Usage
if __name__ == '__main__':
    # Test a strong buy signal
    pred_buy = {'prediction': 'Bullish', 'confidence': 0.88}
    features_buy = pd.DataFrame([{'RSI_14': 55}])
    print("--- Strong Buy Test ---")
    print(get_trade_recommendation(pred_buy, features_buy))

    # Test a weak hold signal
    pred_hold = {'prediction': 'Bullish', 'confidence': 0.60}
    features_hold = pd.DataFrame([{'RSI_14': 65}])
    print("\n--- Weak Hold Test ---")
    print(get_trade_recommendation(pred_hold, features_hold))