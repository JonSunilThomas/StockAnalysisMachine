import streamlit as st
import pandas as pd
import numpy as np
import sys
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Add project root to path (if needed)
sys.path.append(str(Path(__file__).resolve().parents[2]))

# Import data directories
from backend.config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR

# frontend/ui_components/dashboard_plots.py

# frontend/ui_components/dashboard_plots.py

def display_price_history_chart(ticker: str):
    """
    Displays a simple price history chart with a controlled height.
    """
    st.subheader(f"Recent Price History for {ticker}")
    
    sys.path.append(str(Path(__file__).resolve().parents[2]))
    from backend.config.settings import RAW_DATA_DIR
    
    price_path = RAW_DATA_DIR / f"price_{ticker}.csv"
    if price_path.exists():
        try:
            price_df = pd.read_csv(price_path, parse_dates=['date'])
            
            # --- FIX: Ensure the 'close' column is a numeric type ---
            price_df['close'] = pd.to_numeric(price_df['close'], errors='coerce')
            # ---
            
            price_df.set_index('date', inplace=True)
            st.line_chart(price_df['close'], height=300)

        except Exception as e:
            st.warning(f"Error loading price data: {e}")
    else:
        st.warning("Price history data not available.")
        
def plot_performance_with_matplotlib(ticker: str):
    """
    Plots historical performance using Matplotlib with improved aesthetics.
    """
    st.subheader("Historical Model Performance (Backtest)")

    price_path = RAW_DATA_DIR / f"price_{ticker}.csv"
    pred_path = PROCESSED_DATA_DIR / f"historical_predictions_{ticker}.csv"

    if not price_path.exists() or not pred_path.exists():
        st.warning("Historical performance data not available for this ticker yet.")
        return

    try:
        price_df = pd.read_csv(price_path, parse_dates=['date'])
        pred_df = pd.read_csv(pred_path, parse_dates=['date'])
    except Exception as e:
        st.warning(f"Error loading data: {e}")
        return

    price_df['low'] = pd.to_numeric(price_df['low'], errors='coerce')
    plot_df = pd.merge(price_df, pred_df, on='date', how='left')
    plot_df['buy_signal'] = np.where(plot_df['prediction'] == 1, plot_df['low'] * 0.98, np.nan)

    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(8, 5))  # Less elongated

    ax.plot(plot_df['date'], plot_df['close'], label='Close Price', color='#00BFFF', linewidth=1.5)
    ax.scatter(
        plot_df['date'],
        plot_df['buy_signal'],
        label='Buy Signal',
        marker='^',
        color='#00FF7F',
        s=150,
        edgecolors='black'
    )

    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    fig.autofmt_xdate()

    ax.set_title(f'Model Buy Signals vs. Actual Price for {ticker}', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (USD)', fontsize=12)
    ax.legend(loc='upper left')
    ax.grid(True, linestyle='--', alpha=0.3)

    ax.set_facecolor('#1E1E1E')
    fig.patch.set_facecolor('#0E1117')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.title.set_color('white')

    for spine in ax.spines.values():
        spine.set_edgecolor('#555555')

    st.pyplot(fig)