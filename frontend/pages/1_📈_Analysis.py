import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.main_handler import get_prediction_for_ticker
from ui_components.display_info import display_prediction_and_drivers
from backend.trading_logic.generate_recommendation import get_trade_recommendation
from ui_components.dashboard_plots import (
    display_price_history_chart,
    plot_performance_with_matplotlib
)

# --- Page Configuration and Authentication ---
st.set_page_config(page_title="Analysis Dashboard", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please log in to access the analysis dashboard.")
    st.stop()

st.title("📈 Analysis Dashboard")
st.write(f"Welcome, {st.session_state.get('email', 'User')}!")

# --- Sidebar for User Input ---
with st.sidebar:
    st.header("Analysis Input")
    ticker_input = st.text_input("Enter Stock Ticker", "AAPL").upper()
    analyze_button = st.button("Analyze Stock", type="primary", use_container_width=True)

# --- Main Content Area ---
if analyze_button:
    if not ticker_input:
        st.warning("Please enter a stock ticker.")
    else:
        with st.spinner(f'Running full analysis for **{ticker_input}**...'):
            results = get_prediction_for_ticker(ticker_input)

        # --- Check if results are valid and contain required keys ---
        if results and all(k in results for k in ['prediction', 'confidence', 'latest_features', 'explanation']):
            st.header(f"Analysis for: {ticker_input}")

            prediction_data = {
                "prediction": results['prediction'],
                "confidence": results['confidence']
            }
            latest_features = results['latest_features']
            recommendation = get_trade_recommendation(prediction_data, latest_features)

            st.subheader("Trade Recommendation")
            action_color = (
                "green" if recommendation['action'] == "Buy"
                else "red" if recommendation['action'] == "Sell"
                else "orange"
            )
            st.markdown(
                f"### <span style='color:{action_color};'>{recommendation['action']}</span>",
                unsafe_allow_html=True
            )
            st.write(f"**Reasoning:** {recommendation.get('reasoning', 'N/A')}")
            st.write(f"**Suggestion:** {recommendation.get('quantity_suggestion', 'N/A')}")
            st.warning(f"**Disclaimer:** {recommendation.get('disclaimer', '')}", icon="⚠️")

            st.divider()

            col1, col2 = st.columns((1, 1))

            with col1:
                display_prediction_and_drivers(prediction_data, results['explanation'])

            with col2:
                display_price_history_chart(ticker_input)
                st.subheader("Key Statistics")
                if hasattr(latest_features, 'iloc') and not latest_features.empty:
                    latest_features_row = latest_features.iloc[0]
                    st.metric("52-Week High", f"${latest_features_row.get('rolling_high_52wk', float('nan')):.2f}")
                    st.metric("52-Week Low", f"${latest_features_row.get('rolling_low_52wk', float('nan')):.2f}")
                    st.metric("RSI", f"{latest_features_row.get('RSI_14', float('nan')):.2f}")
                    st.metric("Return on Equity (ROE)", f"{latest_features_row.get('roe', float('nan')):.2%}")
                    st.metric("Return on Assets (ROA)", f"{latest_features_row.get('roa', float('nan')):.2%}")
                else:
                    st.info("No feature data available for this ticker.")

            st.divider()
            plot_performance_with_matplotlib(ticker_input)

        else:
            st.error("Could not retrieve analysis. Please check the ticker or try again later.")
            st.info("Check the terminal for specific backend error messages.")
else:
    st.info("Enter a stock ticker in the sidebar and click 'Analyze Stock' to begin.")