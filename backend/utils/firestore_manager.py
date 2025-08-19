# backend/utils/firestore_manager.py
import firebase_admin
from firebase_admin import credentials, firestore
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))

def initialize_firestore():
    """
    Initializes the Firestore client if not already initialized.
    """
    if not firebase_admin._apps:
        cred_path = Path(__file__).resolve().parents[1] / "config/firestore_credentials.json"
        if not cred_path.exists():
            raise FileNotFoundError("Firestore credentials file not found. Please follow setup instructions.")
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    return firestore.client()

def create_user(db, email, password):
    """
    Creates a new user document in the 'users' collection.
    Note: In a real app, you'd hash the password. This is simplified.
    """
    users_ref = db.collection('users')
    users_ref.document(email).set({
        'email': email,
        'password': password # WARNING: Storing plain text passwords is not secure
    })
    print(f"User {email} created successfully.")

def get_user(db, email):
    """
    Retrieves a user document from Firestore.
    """
    doc_ref = db.collection('users').document(email)
    return doc_ref.get()

def add_stock_to_portfolio(db, email, ticker, shares, purchase_price):
    """
    Adds a new stock to a user's portfolio subcollection.
    """
    portfolio_ref = db.collection('users').document(email).collection('portfolio')
    portfolio_ref.document(ticker).set({
        'ticker': ticker,
        'shares': shares,
        'purchase_price': purchase_price
    })
    print(f"Added {ticker} to {email}'s portfolio.")

def get_portfolio(db, email):
    """
    Retrieves all stocks from a user's portfolio.
    """
    portfolio_docs = db.collection('users').document(email).collection('portfolio').stream()
    return [doc.to_dict() for doc in portfolio_docs]

# Example usage
if __name__ == '__main__':
    db = initialize_firestore()
    # Test user creation
    # create_user(db, 'test@example.com', 'password123')
    
    # Test adding a stock
    # add_stock_to_portfolio(db, 'test@example.com', 'TSLA', 10, 250.0)
    
    # Test getting portfolio
    portfolio = get_portfolio(db, 'test@example.com')
    print("Test Portfolio:", portfolio)