# frontend/pages/2_💼_Portfolio.py
import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Add project root to path to allow importing backend modules
sys.path.append(str(Path(__file__).resolve().parents[2]))
from backend.utils.firestore_manager import initialize_firestore, get_portfolio, add_stock_to_portfolio

# --- Page Configuration and Authentication ---
st.set_page_config(page_title="Portfolio Management", layout="wide")

if not st.session_state.get('logged_in'):
    st.warning("Please log in to manage your portfolio.")
    st.stop()

st.title("💼 Portfolio Management")
st.write(f"Manage the stock portfolio for **{st.session_state['email']}**.")

# --- Firebase Initialization ---
try:
    db = initialize_firestore()
except FileNotFoundError:
    st.error("Firestore credentials not found.")
    st.stop()

# --- Add New Stock Form ---
st.header("Add a New Stock to Your Portfolio")
with st.form("add_stock_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.text_input("Stock Ticker", placeholder="e.g., AAPL").upper()
    with col2:
        shares = st.number_input("Number of Shares", min_value=0.01, step=0.01, format="%.2f")
    with col3:
        purchase_price = st.number_input("Purchase Price ($)", min_value=0.01, step=0.01, format="%.2f")
    
    submitted = st.form_submit_button("Add Stock")
    if submitted:
        if ticker and shares > 0 and purchase_price > 0:
            user_email = st.session_state['email']
            add_stock_to_portfolio(db, user_email, ticker, shares, purchase_price)
            st.success(f"Successfully added {shares} shares of {ticker} to your portfolio!")
        else:
            st.error("Please fill out all fields with valid values.")

# --- Display Current Portfolio ---
st.header("Your Current Holdings")
user_portfolio = get_portfolio(db, st.session_state['email'])

if not user_portfolio:
    st.info("Your portfolio is empty. Add a stock using the form above to get started.")
else:
    portfolio_df = pd.DataFrame(user_portfolio)
    
    # Calculate current value (using purchase price as a placeholder for live price)
    # In a real app, you'd fetch the live price for each stock here
    portfolio_df['current_value_usd'] = portfolio_df['shares'] * portfolio_df['purchase_price']
    
    # Reorder and format columns for better display
    display_df = portfolio_df[['ticker', 'shares', 'purchase_price', 'current_value_usd']]
    display_df = display_df.rename(columns={
        'ticker': 'Ticker',
        'shares': 'Shares',
        'purchase_price': 'Purchase Price ($)',
        'current_value_usd': 'Current Value ($)'
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    total_value = display_df['Current Value ($)'].sum()
    st.metric(label="Total Portfolio Value", value=f"${total_value:,.2f}")