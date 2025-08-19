# frontend/Login.py
import streamlit as st
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from backend.utils.firestore_manager import initialize_firestore, get_user, create_user

# --- Page Configuration ---
st.set_page_config(page_title="AI Analyst Login", page_icon="🤖", layout="centered")

# --- Firebase Initialization ---
try:
    db = initialize_firestore()
except FileNotFoundError:
    st.error("Firestore credentials not found. Please follow the setup instructions.")
    st.stop()

# --- Session State Initialization ---
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
if 'email' not in st.session_state:
    st.session_state['email'] = ""

# --- Main Login Logic ---
st.title("Welcome to the Hybrid AI Stock Analyst 🤖")

# If already logged in, show a welcome message
if st.session_state['logged_in']:
    st.success(f"Logged in as {st.session_state['email']}")
    st.write("Navigate to the **Analysis** or **Portfolio** page using the sidebar.")
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['email'] = ""
        st.rerun()
else:
    choice = st.selectbox("Login or Signup", ["Login", "Signup"])

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if choice == "Signup":
        if st.button("Create Account"):
            if email and password:
                user = get_user(db, email)
                if user.exists:
                    st.warning("Email already registered.")
                else:
                    create_user(db, email, password)
                    st.success("Account created! Please login.")
            else:
                st.warning("Please enter both email and password.")

    if choice == "Login":
        if st.button("Login"):
            if email and password:
                user_doc = get_user(db, email)
                if user_doc.exists and user_doc.to_dict().get('password') == password:
                    st.session_state['logged_in'] = True
                    st.session_state['email'] = email
                    st.success("Login successful!")
                    st.rerun() # Rerun the script to show the logged-in state
                else:
                    st.error("Invalid email or password.")
            else:
                st.warning("Please enter both email and password.")