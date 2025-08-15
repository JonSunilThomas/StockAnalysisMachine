# frontend/app.py
import streamlit as st
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Import our modular components
from backend.main_handler import get_prediction_for_ticker
from ui_components.display_info import display_prediction_and_drivers
from ui_components.dashboard_plots import display_price_history_chart

# --- Page Configuration ---
st.set_page_config(page_title="AI Stock Analyst", page_icon="🤖", layout="wide")

# --- User Interface ---
st.title("🤖 Hybrid AI Stock Analyst")
st.markdown("This tool synthesizes fundamental, technical, and sentiment data to provide an evidence-based investment thesis.")

# --- Sidebar for User Input ---
with st.sidebar:
    st.header("Analysis Input")
    ticker_input = st.text_input("Enter Stock Ticker (e.g., AAPL)", "AAPL").upper()
    analyze_button = st.button("Analyze Stock", type="primary", use_container_width=True)

# --- Main Content Area ---
if analyze_button:
    if not ticker_input:
        st.warning("Please enter a stock ticker.")
    else:
        with st.spinner(f'Running analysis for **{ticker_input}**...'):
            results = get_prediction_for_ticker(ticker_input)

        st.header(f"Analysis for: {ticker_input}")

        col1, col2 = st.columns((1, 1))

        with col1:
            display_prediction_and_drivers(
                {"prediction": results['prediction'], "confidence": results['confidence']},
                results['explanation']
            )

        with col2:
            display_price_history_chart(ticker_input)
else:
    st.info("Enter a stock ticker in the sidebar and click 'Analyze Stock' to begin.")