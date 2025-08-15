# frontend/ui_components/dashboard_plots.py
import streamlit as st
import pandas as pd
import numpy as np

def display_price_history_chart(ticker: str):
    """
    Generates a mock price history DataFrame and displays it as a line chart.
    In a real application, this function would fetch actual price data.
    
    Args:
        ticker (str): The stock ticker for which to display the chart.
    """
    st.subheader(f"Recent Price History for {ticker}")
    
    # --- Mock Data Generation ---
    dates = pd.date_range(start="2024-01-01", end="2025-08-15", freq='B')
    prices = np.random.randn(len(dates)).cumsum() + 150
    price_df = pd.DataFrame({'Date': dates, 'Close Price': prices}).set_index('Date')
    # ---
    
    st.line_chart(price_df)